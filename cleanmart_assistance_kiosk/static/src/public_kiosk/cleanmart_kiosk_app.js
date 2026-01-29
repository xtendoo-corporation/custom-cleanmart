import { registry } from "@web/core/registry";
import { Component, mount, whenReady, useState } from "@odoo/owl";

const KIOSK_CSS = `
.cleanmart-kiosk-container {
    max-width: 600px;
    margin: 40px auto;
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 2px 16px #0002;
    padding: 32px 24px 24px 24px;
    text-align: center;
}
.cleanmart-kiosk-employees {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    margin-bottom: 24px;
}
.cleanmart-kiosk-employee {
    width: 110px;
    cursor: pointer;
    border: 2px solid #eee;
    border-radius: 12px;
    padding: 8px;
    background: #f9f9f9;
    transition: border 0.2s;
}
.cleanmart-kiosk-employee.selected {
    border: 2px solid #007bff;
    background: #e6f0ff;
}
.cleanmart-kiosk-employee img {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 8px;
}
.cleanmart-kiosk-keypad {
    display: grid;
    grid-template-columns: repeat(3, 60px);
    gap: 12px;
    justify-content: center;
    margin: 24px 0 12px 0;
}
.cleanmart-kiosk-keypad button {
    font-size: 1.5em;
    padding: 16px 0;
    border-radius: 8px;
    border: 1px solid #ccc;
    background: #f5f5f5;
    cursor: pointer;
    transition: background 0.2s;
}
.cleanmart-kiosk-keypad button:active {
    background: #e0e0e0;
}
.cleanmart-kiosk-pin {
    font-size: 2em;
    letter-spacing: 0.5em;
    margin-bottom: 12px;
}
.cleanmart-kiosk-message {
    margin: 16px 0;
    font-weight: bold;
    color: #007bff;
}
.cleanmart-kiosk-error {
    color: #d9534f;
    font-weight: bold;
    margin: 16px 0;
}
`;

class CleanmartKioskApp extends Component {
    static template = "cleanmart_assistance_kiosk.cleanmart_kiosk_app";
    setup() {
        this.state = useState({
            loading: this.props.loading,
            loadError: this.props.loadError,
            employees: this.props.employees,
            departments: this.props.departments,
            step: "select_employee",
            selectedEmployee: null,
            pin: "",
            error: null,
            attendanceMessage: null,
        });
        // Inyectar CSS solo una vez
        if (!document.getElementById("cleanmart-kiosk-css")) {
            const style = document.createElement("style");
            style.id = "cleanmart-kiosk-css";
            style.innerHTML = KIOSK_CSS;
            document.head.appendChild(style);
        }
    }
    selectEmployee(employee) {
        this.state.selectedEmployee = employee;
        this.state.step = "enter_pin";
        this.state.pin = "";
        this.state.error = null;
        this.state.attendanceMessage = null;
    }
    handleKeypad(num) {
        if (this.state.pin.length < 6) {
            this.state.pin += num;
        }
    }
    handleBackspace() {
        this.state.pin = this.state.pin.slice(0, -1);
    }
    async checkPin() {
        if (!this.state.selectedEmployee) return;
        const employee_id = this.state.selectedEmployee.id;
        const pin = this.state.pin;
        try {
            const response = await fetch("/cleanmart_assistance_kiosk/check_pin", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ employee_id, pin }),
            });
            const result = await response.json();
            if (result.success) {
                await this.markAttendance(employee_id);
            } else {
                this.state.error = result.error || "PIN incorrecto";
                this.state.pin = "";
            }
        } catch (e) {
            this.state.error = "Error de conexión";
        }
    }
    async markAttendance(employee_id) {
        try {
            const response = await fetch("/cleanmart_assistance_kiosk/mark_attendance", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ employee_id }),
            });
            const result = await response.json();
            if (result.success) {
                this.state.step = "success";
                this.state.attendanceMessage = result.message || "¡Asistencia registrada!";
                this.state.error = null;
                setTimeout(() => {
                    this.state.step = "select_employee";
                    this.state.selectedEmployee = null;
                    this.state.pin = "";
                    this.state.attendanceMessage = null;
                }, 2000);
            } else {
                this.state.error = result.error || "Error al registrar asistencia";
            }
        } catch (e) {
            this.state.error = "Error de conexión";
        }
    }
    renderEmployeeGrid() {
        return (
            <div class="cleanmart-kiosk-employees">
                {this.state.employees.map(emp => (
                    <div
                        class={"cleanmart-kiosk-employee" + (this.state.selectedEmployee && this.state.selectedEmployee.id === emp.id ? " selected" : "")}
                        key={emp.id}
                        onClick={() => this.selectEmployee(emp)}
                    >
                        <img src={emp.image_128 || "/web/static/src/img/placeholder.png"} alt={emp.display_name || emp.name}/>
                        <div>{emp.display_name || emp.name}</div>
                    </div>
                ))}
            </div>
        );
    }
    renderKeypad() {
        const nums = [1,2,3,4,5,6,7,8,9,0];
        return (
            <div class="cleanmart-kiosk-keypad">
                {nums.slice(0,9).map(n => <button key={n} onClick={() => this.handleKeypad(n)}>{n}</button>)}
                <button onClick={() => this.handleBackspace()}>&larr;</button>
                <button onClick={() => this.handleKeypad(0)}>0</button>
                <button onClick={() => this.checkPin()}>OK</button>
            </div>
        );
    }
    static components = {};
    static props = {};
    render() {
        if (this.state.loading) {
            return <div class="cleanmart-kiosk-container"><div class="o_cleanmart_kiosk_loader">Cargando...</div></div>;
        }
        if (this.state.loadError) {
            return <div class="cleanmart-kiosk-container"><div class="o_cleanmart_kiosk_error">Error al cargar datos. Intenta recargar la página.</div></div>;
        }
        if (this.state.step === "select_employee") {
            return (
                <div class="cleanmart-kiosk-container">
                    <h2>Selecciona tu usuario</h2>
                    {this.renderEmployeeGrid()}
                </div>
            );
        }
        if (this.state.step === "enter_pin") {
            return (
                <div class="cleanmart-kiosk-container">
                    <h2>Introduce tu PIN</h2>
                    <div class="cleanmart-kiosk-pin">{this.state.pin.replace(/./g, "•")}</div>
                    {this.renderKeypad()}
                    {this.state.error && <div class="cleanmart-kiosk-error">{this.state.error}</div>}
                    <button style="margin-top:12px" onClick={() => {this.state.step = 'select_employee'; this.state.selectedEmployee = null; this.state.pin = ''; this.state.error = null;}}>Volver</button>
                </div>
            );
        }
        if (this.state.step === "success") {
            return (
                <div class="cleanmart-kiosk-container">
                    <div class="cleanmart-kiosk-message">{this.state.attendanceMessage || "¡Asistencia registrada!"}</div>
                </div>
            );
        }
        return null;
    }
}

registry.category("actions").add("cleanmart_assistance_kiosk.kiosk_mode", {
    async setup(env, { action }) {
        const root = document.getElementById("o_cleanmart_assistance_kiosk_mode");
        let employees = [];
        let departments = [];
        let loading = true;
        let loadError = false;
        try {
            const response = await fetch("/cleanmart_assistance_kiosk/data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });
            const result = await response.json();
            employees = result.employees || [];
            departments = result.departments || [];
            loading = false;
        } catch (e) {
            loading = false;
            loadError = true;
        }
        mount(CleanmartKioskApp, root, {
            employees,
            departments,
            loading,
            loadError,
        });
    }
});

