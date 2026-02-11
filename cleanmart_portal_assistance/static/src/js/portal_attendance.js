// Portal Attendance JavaScript - Vanilla JS (no Odoo modules needed)

console.log('[ATTENDANCE] Script loaded - START');

document.addEventListener('DOMContentLoaded', function() {
    console.log('[ATTENDANCE] DOMContentLoaded event fired');
    
    const attendanceBtn = document.getElementById('attendanceActionBtn');
    const messageDiv = document.getElementById('attendanceMessage');
    
    console.log('[ATTENDANCE] Button element:', attendanceBtn);
    console.log('[ATTENDANCE] Message div element:', messageDiv);
    
    if (!attendanceBtn) {
        console.warn('[ATTENDANCE] Attendance button not found - script will not attach event handlers');
        return;
    }
    
    console.log('[ATTENDANCE] Attaching click event to attendance button');
    
    attendanceBtn.addEventListener('click', async function() {
        console.log('[ATTENDANCE] Button clicked!');
        
        // Deshabilitar botón y mostrar loading
        attendanceBtn.disabled = true;
        const originalHTML = attendanceBtn.innerHTML;
        attendanceBtn.innerHTML = '<span class="o_attendance_loading"></span> Procesando...';
        
        console.log('[ATTENDANCE] Making fetch request to /my/attendance/action');
        
        try {
            const response = await fetch('/my/attendance/action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {},
                }),
            });
            
            console.log('[ATTENDANCE] Response received:', response.status, response.statusText);
            
            const data = await response.json();
            console.log('[ATTENDANCE] Response data:', data);
            
            const result = data.result || data;
            console.log('[ATTENDANCE] Result:', result);
            
            if (result.success) {
                console.log('[ATTENDANCE] Success!');
                // Mostrar mensaje de éxito
                messageDiv.className = 'mt-3 success';
                messageDiv.innerHTML = `<i class="fa fa-check-circle"></i> ${result.message}`;
                
                // Actualizar la UI después de 1 segundo
                setTimeout(() => {
                    console.log('[ATTENDANCE] Reloading page...');
                    location.reload();
                }, 1500);
                
            } else {
                console.error('[ATTENDANCE] Error from server:', result.error);
                // Mostrar error
                messageDiv.className = 'mt-3 error';
                messageDiv.innerHTML = `<i class="fa fa-exclamation-circle"></i> ${result.error}`;
                
                // Re-habilitar botón
                attendanceBtn.disabled = false;
                attendanceBtn.innerHTML = originalHTML;
            }
            
        } catch (error) {
            console.error('[ATTENDANCE] Fetch error:', error);
            messageDiv.className = 'mt-3 error';
            messageDiv.innerHTML = '<i class="fa fa-exclamation-circle"></i> Error de conexión';
            
            // Re-habilitar botón
            attendanceBtn.disabled = false;
            attendanceBtn.innerHTML = originalHTML;
        }
    });
    
    console.log('[ATTENDANCE] Event listener attached successfully');
    
    // Actualizar horas en tiempo real (cada 30 segundos)
    setInterval(updateHours, 30000);
    
    function updateHours() {
        const hoursTodayElement = document.getElementById('hoursTodayValue');
        const lastAttendanceElement = document.getElementById('lastAttendanceValue');
        
        if (!hoursTodayElement) return;
        
        console.log('[ATTENDANCE] Updating hours display...');
        
        // Aquí podrías hacer una llamada AJAX para obtener los datos actualizados
        // Por ahora, solo añadimos un efecto visual
        hoursTodayElement.style.animation = 'pulse 0.5s ease';
        setTimeout(() => {
            hoursTodayElement.style.animation = '';
        }, 500);
    }
});

console.log('[ATTENDANCE] Script loaded - END');
