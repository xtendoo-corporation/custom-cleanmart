/**
 * Cleanmart Department Kiosk - JavaScript
 */

(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        // State
        let currentEmployee = null;
        let pinValue = '';
        
        // DOM Elements
        const selectionState = document.getElementById('selection-state');
        const pinState = document.getElementById('pin-state');
        const successState = document.getElementById('success-state');
        
        const employeeItems = document.querySelectorAll('.employee-item');
        const btnCancel = document.getElementById('btn-cancel');
        const pinDisplay = document.getElementById('pin-display');
        const errorMessage = document.getElementById('error-message');
        const successMessage = document.getElementById('success-message');
        const keypadBtns = document.querySelectorAll('.keypad-btn');
        
        const selectedEmpName = document.getElementById('selected-employee-name');
        const selectedEmpAvatar = document.getElementById('selected-employee-avatar');
        
        // Functions
        function showState(state) {
            selectionState.style.display = 'none';
            pinState.style.display = 'none';
            successState.style.display = 'none';
            
            if (state === 'selection') {
                selectionState.style.display = 'block';
            } else if (state === 'pin') {
                pinState.style.display = 'block';
            } else if (state === 'success') {
                successState.style.display = 'block';
            }
        }
        
        function updatePinDisplay() {
            const dots = '•'.repeat(pinValue.length);
            pinDisplay.querySelector('.pin-dots').textContent = dots || '―――';
        }
        
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 3000);
        }
        
        async function checkPinAndMark() {
            if (pinValue.length === 0) {
                showError('Introduce tu PIN');
                return;
            }
            
            try {
                // Check PIN
                const checkResponse = await fetch('/kiosk/department/check_pin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { employee_id: currentEmployee.id, pin: pinValue }
                    })
                });
                
                const checkData = await checkResponse.json();
                
                if (checkData.result && checkData.result.success) {
                    // Mark Attendance
                    const attendanceResponse = await fetch('/kiosk/department/mark_attendance', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            jsonrpc: '2.0',
                            method: 'call',
                            params: { employee_id: currentEmployee.id }
                        })
                    });
                    
                    const attendanceData = await attendanceResponse.json();
                    
                    if (attendanceData.result && attendanceData.result.success) {
                        successMessage.textContent = attendanceData.result.message;
                        showState('success');
                        setTimeout(() => window.location.reload(), 2000);
                    } else {
                        showError(attendanceData.result?.error || 'Error de registro');
                        pinValue = '';
                        updatePinDisplay();
                    }
                } else {
                    showError(checkData.result?.error || 'PIN incorrecto');
                    pinValue = '';
                    updatePinDisplay();
                }
            } catch (error) {
                showError('Error de conexión');
                pinValue = '';
                updatePinDisplay();
            }
        }
        
        // Event Listeners
        employeeItems.forEach(item => {
            item.addEventListener('click', function() {
                currentEmployee = {
                    id: this.getAttribute('data-employee-id'),
                    name: this.getAttribute('data-employee-name'),
                    avatar: this.querySelector('.employee-avatar').innerHTML
                };
                
                selectedEmpName.textContent = currentEmployee.name;
                selectedEmpAvatar.innerHTML = currentEmployee.avatar;
                
                pinValue = '';
                updatePinDisplay();
                showState('pin');
            });
        });
        
        btnCancel.addEventListener('click', () => showState('selection'));
        
        keypadBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const val = this.getAttribute('data-value');
                if (val === 'backspace') {
                    pinValue = pinValue.slice(0, -1);
                    updatePinDisplay();
                } else if (val === 'ok') {
                    checkPinAndMark();
                } else {
                    if (pinValue.length < 10) {
                        pinValue += val;
                        updatePinDisplay();
                    }
                }
            });
        });
        
        // Initial state
        showState('selection');
    });
})();
