// Portal Attendance JavaScript - Vanilla JS (no Odoo modules needed)

document.addEventListener('DOMContentLoaded', function() {
    const attendanceBtn = document.getElementById('attendanceActionBtn');
    const messageDiv = document.getElementById('attendanceMessage');
    
    if (!attendanceBtn) return;
    
    attendanceBtn.addEventListener('click', async function() {
        // Deshabilitar botón y mostrar loading
        attendanceBtn.disabled = true;
        const originalHTML = attendanceBtn.innerHTML;
        attendanceBtn.innerHTML = '<span class="o_attendance_loading"></span> Procesando...';
        
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
            
            const data = await response.json();
            const result = data.result || data;
            
            if (result.success) {
                // Mostrar mensaje de éxito
                messageDiv.className = 'mt-3 success';
                messageDiv.innerHTML = `<i class="fa fa-check-circle"></i> ${result.message}`;
                
                // Actualizar la UI después de 1 segundo
                setTimeout(() => {
                    location.reload();
                }, 1500);
                
            } else {
                // Mostrar error
                messageDiv.className = 'mt-3 error';
                messageDiv.innerHTML = `<i class="fa fa-exclamation-circle"></i> ${result.error}`;
                
                // Re-habilitar botón
                attendanceBtn.disabled = false;
                attendanceBtn.innerHTML = originalHTML;
            }
            
        } catch (error) {
            console.error('Error:', error);
            messageDiv.className = 'mt-3 error';
            messageDiv.innerHTML = '<i class="fa fa-exclamation-circle"></i> Error de conexión';
            
            // Re-habilitar botón
            attendanceBtn.disabled = false;
            attendanceBtn.innerHTML = originalHTML;
        }
    });
    
    // Actualizar horas en tiempo real (cada 30 segundos)
    setInterval(updateHours, 30000);
    
    function updateHours() {
        const hoursTodayElement = document.getElementById('hoursTodayValue');
        const lastAttendanceElement = document.getElementById('lastAttendanceValue');
        
        if (!hoursTodayElement) return;
        
        // Aquí podrías hacer una llamada AJAX para obtener los datos actualizados
        // Por ahora, solo añadimos un efecto visual
        hoursTodayElement.style.animation = 'pulse 0.5s ease';
        setTimeout(() => {
            hoursTodayElement.style.animation = '';
        }, 500);
    }
});
