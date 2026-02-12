/**
 * Cleanmart Individual Kiosk - JavaScript
 * Handles PIN entry, attendance marking, and state management
 */

(function() {
    'use strict';
    
    console.log('[INDIVIDUAL_KIOSK] Script loaded');
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[INDIVIDUAL_KIOSK] DOM ready, initializing...');
        
        // Get employee data from template
        const employeeDataElement = document.getElementById('employee-data');
        if (!employeeDataElement) {
            console.error('[INDIVIDUAL_KIOSK] Employee data not found');
            return;
        }
        
        const employeeData = JSON.parse(employeeDataElement.textContent);
        console.log('[INDIVIDUAL_KIOSK] Employee data:', employeeData);
        
        // State management
        let currentState = 'initial'; // initial, pin, success
        let pinValue = '';
        
        // Get DOM elements
        const initialState = document.getElementById('initial-state');
        const pinState = document.getElementById('pin-state');
        const successState = document.getElementById('success-state');
        const btnAction = document.getElementById('btn-action');
        const btnCancel = document.getElementById('btn-cancel');
        const pinDisplay = document.getElementById('pin-display');
        const errorMessage = document.getElementById('error-message');
        const successMessage = document.getElementById('success-message');
        const keypadBtns = document.querySelectorAll('.keypad-btn');
        
        // State transition functions
        function showState(state) {
            initialState.style.display = 'none';
            pinState.style.display = 'none';
            successState.style.display = 'none';
            
            if (state === 'initial') {
                initialState.style.display = 'block';
            } else if (state === 'pin') {
                pinState.style.display = 'block';
            } else if (state === 'success') {
                successState.style.display = 'block';
            }
            
            currentState = state;
            console.log('[INDIVIDUAL_KIOSK] State changed to:', state);
        }
        
        // Update PIN display
        function updatePinDisplay() {
            const dots = '•'.repeat(pinValue.length);
            pinDisplay.querySelector('.pin-dots').textContent = dots || '―――';
        }
        
        // Show error
        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 3000);
        }
        
        // Clear PIN
        function clearPin() {
            pinValue = '';
            updatePinDisplay();
        }
        
        // Check PIN and mark attendance
        async function checkPinAndMarkAttendance() {
            if (pinValue.length === 0) {
                showError('Por favor, introduce tu PIN');
                return;
            }
            
            console.log('[INDIVIDUAL_KIOSK] Checking PIN...');
            
            try {
                // First, check PIN
                const checkResponse = await fetch('/kiosk/individual/check_pin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            employee_id: employeeData.id,
                            pin: pinValue
                        }
                    })
                });
                
                const checkData = await checkResponse.json();
                console.log('[INDIVIDUAL_KIOSK] PIN check response:', checkData);
                
                if (checkData.result && checkData.result.success) {
                    // PIN correct, now mark attendance
                    console.log('[INDIVIDUAL_KIOSK] PIN correct, marking attendance...');
                    
                    const attendanceResponse = await fetch('/kiosk/individual/mark_attendance', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            jsonrpc: '2.0',
                            method: 'call',
                            params: {
                                employee_id: employeeData.id
                            }
                        })
                    });
                    
                    const attendanceData = await attendanceResponse.json();
                    console.log('[INDIVIDUAL_KIOSK] Attendance response:', attendanceData);
                    
                    if (attendanceData.result && attendanceData.result.success) {
                        // Success!
                        successMessage.textContent = attendanceData.result.message || '¡Asistencia registrada!';
                        showState('success');
                        
                        // Reload page after 2 seconds
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    } else {
                        showError(attendanceData.result?.error || 'Error al registrar asistencia');
                        clearPin();
                    }
                } else {
                    // PIN incorrect
                    showError(checkData.result?.error || 'PIN incorrecto');
                    clearPin();
                }
            } catch (error) {
                console.error('[INDIVIDUAL_KIOSK] Error:', error);
                showError('Error de conexión. Por favor, intenta de nuevo.');
                clearPin();
            }
        }
        
        // Event listeners
        btnAction.addEventListener('click', function() {
            console.log('[INDIVIDUAL_KIOSK] Action button clicked');
            clearPin();
            showState('pin');
        });
        
        btnCancel.addEventListener('click', function() {
            console.log('[INDIVIDUAL_KIOSK] Cancel button clicked');
            clearPin();
            showState('initial');
        });
        
        // Keypad event listeners
        keypadBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                console.log('[INDIVIDUAL_KIOSK] Keypad button clicked:', value);
                
                if (value === 'backspace') {
                    pinValue = pinValue.slice(0, -1);
                    updatePinDisplay();
                } else if (value === 'ok') {
                    checkPinAndMarkAttendance();
                } else {
                    if (pinValue.length < 10) { // Limit PIN length
                        pinValue += value;
                        updatePinDisplay();
                    }
                }
            });
        });
        
        // Prevent back navigation on mobile
        window.history.pushState(null, '', window.location.href);
        window.addEventListener('popstate', function() {
            window.history.pushState(null, '', window.location.href);
        });
        
        console.log('[INDIVIDUAL_KIOSK] Initialization complete');
    });
    
})();
