import * as KioskApp from "@hr_attendance/public_kiosk/public_kiosk_app";

const originalCreate = KioskApp.createPublicKioskAttendance;

KioskApp.createPublicKioskAttendance = async function(document, kiosk_backend_info) {
    if (kiosk_backend_info && kiosk_backend_info.departments) {
        kiosk_backend_info.departments = kiosk_backend_info.departments.filter(dep =>
            dep.name && dep.name.toLowerCase() !== "all"
        );
        console.log("[Cleanmart] Departamentos filtrados:", kiosk_backend_info.departments.map(d => d.name));
    }
    const result = await originalCreate(document, kiosk_backend_info);
    // Eliminar la opción "All" del DOM después de renderizar
    setTimeout(() => {
        document.querySelectorAll('div,li,option').forEach(opt => {
            if (opt.textContent && opt.textContent.trim().toLowerCase() === 'all') {
                console.log('[Cleanmart] Eliminando opción ALL del DOM');
                opt.remove();
            }
        });
    }, 500);
    return result;
};
