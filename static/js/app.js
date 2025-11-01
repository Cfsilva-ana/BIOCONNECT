// BioConnect Modern JavaScript
class BioConnect {
    constructor() {
        this.currentUser = null;
        this.refreshInterval = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupScrollEffects();
        this.updateForms();
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            // Form listeners
            document.getElementById('userType')?.addEventListener('change', () => this.updateLoginForm());
            document.getElementById('regUserType')?.addEventListener('change', () => this.updateRegisterForm());
            document.getElementById('loginForm')?.addEventListener('submit', (e) => this.handleLogin(e));
            document.getElementById('registerForm')?.addEventListener('submit', (e) => this.handleRegister(e));

            // Modal listeners
            window.onclick = (event) => {
                const loginModal = document.getElementById('loginModal');
                const registerModal = document.getElementById('registerModal');
                if (event.target === loginModal || event.target === registerModal) {
                    this.closeModals();
                }
            };

            // Keyboard listeners
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeModals();
                }
            });
        });
    }

    setupScrollEffects() {
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar?.classList.add('scrolled');
            } else {
                navbar?.classList.remove('scrolled');
            }
        });
    }

    // Modal Management
    showLoginModal() {
        const modal = document.getElementById('loginModal');
        modal.style.display = 'block';
        modal.classList.add('animate-fade-in');
        document.body.style.overflow = 'hidden';
    }

    showRegisterModal() {
        const modal = document.getElementById('registerModal');
        modal.style.display = 'block';
        modal.classList.add('animate-fade-in');
        document.body.style.overflow = 'hidden';
    }

    closeModals() {
        document.getElementById('loginModal').style.display = 'none';
        document.getElementById('registerModal').style.display = 'none';
        document.body.style.overflow = 'auto';
        this.clearAlerts();
    }

    switchToRegister() {
        this.closeModals();
        setTimeout(() => this.showRegisterModal(), 100);
    }

    switchToLogin() {
        this.closeModals();
        setTimeout(() => this.showLoginModal(), 100);
    }

    // Form Management
    updateForms() {
        this.updateLoginForm();
        this.updateRegisterForm();
    }

    updateLoginForm() {
        const userType = document.getElementById('userType')?.value;
        const emailLabel = document.getElementById('emailLabel');
        const emailInput = document.getElementById('email');
        const passwordGroup = document.getElementById('passwordGroup');
        const passwordInput = document.getElementById('password');

        if (userType === 'patient') {
            emailLabel.textContent = 'Device ID';
            emailInput.placeholder = 'ESP32_001';
            passwordGroup.style.display = 'none';
            passwordInput.required = false;
        } else {
            emailLabel.textContent = 'Email';
            emailInput.placeholder = 'medico@teste.com';
            passwordGroup.style.display = 'block';
            passwordInput.required = true;
        }
    }

    updateRegisterForm() {
        const userType = document.getElementById('regUserType')?.value;
        const emailLabel = document.getElementById('regEmailLabel');
        const emailInput = document.getElementById('regEmail');
        const passwordGroup = document.getElementById('regPasswordGroup');
        const passwordInput = document.getElementById('regPassword');

        if (userType === 'patient') {
            emailLabel.textContent = 'Device ID';
            emailInput.placeholder = 'ESP32_XXX';
            passwordGroup.style.display = 'none';
            passwordInput.required = false;
        } else {
            emailLabel.textContent = 'Email';
            emailInput.placeholder = 'seu@email.com';
            passwordGroup.style.display = 'block';
            passwordInput.required = true;
        }
    }

    // Alert Management
    showAlert(message, type = 'error', container = 'loginAlertContainer') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} animate-fade-in`;
        
        const icon = type === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-check-circle';
        alertDiv.innerHTML = `<i class="${icon}"></i> ${message}`;

        const alertContainer = document.getElementById(container);
        alertContainer.innerHTML = '';
        alertContainer.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    clearAlerts() {
        document.querySelectorAll('.alert').forEach(alert => alert.remove());
    }

    // Authentication
    async handleLogin(e) {
        e.preventDefault();
        
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Loading state
        submitBtn.textContent = 'Entrando...';
        submitBtn.disabled = true;
        form.classList.add('loading');

        try {
            const userType = document.getElementById('userType').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/api/v1/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    user_type: userType
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentUser = data.user;
                this.showAlert('Login realizado com sucesso!', 'success', 'loginAlertContainer');
                setTimeout(() => {
                    this.showDashboard();
                }, 1000);
            } else {
                this.showAlert(data.detail || 'Erro no login', 'error', 'loginAlertContainer');
            }
        } catch (error) {
            this.showAlert('Erro de conexão. Verifique sua internet.', 'error', 'loginAlertContainer');
        } finally {
            // Reset loading state
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            form.classList.remove('loading');
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        
        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Loading state
        submitBtn.textContent = 'Cadastrando...';
        submitBtn.disabled = true;
        form.classList.add('loading');

        try {
            const userType = document.getElementById('regUserType').value;
            const name = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;

            const response = await fetch('/api/v1/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password,
                    user_type: userType
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showAlert('Cadastro realizado com sucesso!', 'success', 'registerAlertContainer');
                setTimeout(() => {
                    this.switchToLogin();
                }, 2000);
            } else {
                this.showAlert(data.detail || 'Erro no cadastro', 'error', 'registerAlertContainer');
            }
        } catch (error) {
            this.showAlert('Erro de conexão. Verifique sua internet.', 'error', 'registerAlertContainer');
        } finally {
            // Reset loading state
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            form.classList.remove('loading');
        }
    }

    // Dashboard Management
    showDashboard() {
        document.getElementById('landingPage').classList.add('hidden');
        this.closeModals();
        
        const dashboardPage = document.getElementById('dashboardPage');
        dashboardPage.classList.remove('hidden');
        dashboardPage.classList.add('animate-fade-in');

        document.getElementById('welcomeMessage').textContent = `Bem-vindo, ${this.currentUser.name}!`;
        document.getElementById('userInfo').textContent = `${this.currentUser.type === 'doctor' ? 'Médico' : 'Paciente'} - ${this.currentUser.email}`;

        if (this.currentUser.type === 'doctor') {
            document.getElementById('doctorDashboard').classList.remove('hidden');
            this.loadDoctorDashboard();
            this.startAutoRefresh();
        } else {
            document.getElementById('patientDashboard').classList.remove('hidden');
            this.loadPatientDashboard();
            this.startAutoRefresh();
        }
    }

    async loadDoctorDashboard() {
        try {
            const response = await fetch('/api/v1/patients');
            const data = await response.json();

            const patients = data.patients || [];
            const onlinePatients = patients.filter(p => p.status === 'online').length;
            const criticalAlerts = patients.filter(p => p.vital_status === 'critical').length;
            const totalReadings = patients.reduce((sum, p) => sum + p.total_readings, 0);

            // Update stats with animation
            this.animateCounter('totalPatients', patients.length);
            this.animateCounter('onlinePatients', onlinePatients);
            this.animateCounter('criticalAlerts', criticalAlerts);
            this.animateCounter('totalReadings', totalReadings);

            this.renderPatients(patients);
        } catch (error) {
            console.error('Erro ao carregar dashboard do médico:', error);
            this.showAlert('Erro ao carregar dados dos pacientes', 'error');
        }
    }

    async loadPatientDashboard() {
        try {
            const response = await fetch(`/api/v1/readings/${this.currentUser.email}`);
            const data = await response.json();

            const readings = data.readings || [];

            if (readings.length > 0) {
                const latest = readings[0];
                this.animateCounter('currentBPM', latest.bpm);
                this.animateCounter('currentTemp', latest.temperature, 1);
                document.getElementById('deviceStatus').textContent = 'Online';
            } else {
                document.getElementById('deviceStatus').textContent = 'Offline';
            }

            this.animateCounter('patientTotalReadings', readings.length);
            this.renderPatientReadings(readings);
        } catch (error) {
            console.error('Erro ao carregar dashboard do paciente:', error);
            this.showAlert('Erro ao carregar suas leituras', 'error');
        }
    }

    // Rendering Methods
    renderPatients(patients) {
        const patientsGrid = document.getElementById('patientsGrid');
        patientsGrid.innerHTML = '';

        patients.forEach((patient, index) => {
            const patientCard = document.createElement('div');
            patientCard.className = 'patient-card animate-fade-in';
            patientCard.style.animationDelay = `${index * 0.1}s`;
            
            patientCard.innerHTML = `
                <div class="patient-header">
                    <div class="patient-name">${patient.name}</div>
                    <span class="status-badge status-${patient.vital_status}">${patient.vital_status}</span>
                </div>
                <div class="patient-vitals">
                    <div class="vital">
                        <div class="vital-value">${patient.bpm}</div>
                        <div class="vital-label">BPM</div>
                    </div>
                    <div class="vital">
                        <div class="vital-value">${patient.temperature}</div>
                        <div class="vital-label">TEMP °C</div>
                    </div>
                </div>
                <div class="patient-info">
                    <span><i class="fas fa-microchip"></i> ${patient.device_id}</span>
                    <span><i class="fas fa-user"></i> ${patient.age} anos</span>
                    <span><i class="fas fa-stethoscope"></i> ${patient.condition}</span>
                </div>
            `;
            
            patientsGrid.appendChild(patientCard);
        });
    }

    renderPatientReadings(readings) {
        const readingsContainer = document.getElementById('patientReadings');
        readingsContainer.innerHTML = '';

        readings.slice(0, 10).forEach((reading, index) => {
            const readingCard = document.createElement('div');
            readingCard.className = 'patient-card animate-fade-in';
            readingCard.style.marginBottom = '1rem';
            readingCard.style.animationDelay = `${index * 0.1}s`;
            
            const timestamp = new Date(reading.timestamp).toLocaleString('pt-BR');
            
            readingCard.innerHTML = `
                <div class="patient-header">
                    <div class="patient-name">Leitura</div>
                    <span class="status-badge status-${reading.status}">${reading.status}</span>
                </div>
                <div class="patient-vitals">
                    <div class="vital">
                        <div class="vital-value">${reading.bpm}</div>
                        <div class="vital-label">BPM</div>
                    </div>
                    <div class="vital">
                        <div class="vital-value">${reading.temperature}</div>
                        <div class="vital-label">TEMP °C</div>
                    </div>
                </div>
                <div class="patient-info">
                    <span><i class="fas fa-clock"></i> ${timestamp}</span>
                </div>
            `;
            
            readingsContainer.appendChild(readingCard);
        });
    }

    // Utility Methods
    animateCounter(elementId, targetValue, decimals = 0) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const startValue = 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = startValue + (targetValue - startValue) * this.easeOutQuart(progress);
            element.textContent = decimals > 0 ? currentValue.toFixed(decimals) : Math.floor(currentValue);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    scrollToFeatures() {
        document.getElementById('features')?.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        this.refreshInterval = setInterval(() => {
            if (this.currentUser && !document.getElementById('dashboardPage').classList.contains('hidden')) {
                if (this.currentUser.type === 'doctor') {
                    this.loadDoctorDashboard();
                } else {
                    this.loadPatientDashboard();
                }
            }
        }, 30000); // Refresh every 30 seconds
    }

    logout() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        this.currentUser = null;
        document.getElementById('dashboardPage').classList.add('hidden');
        document.getElementById('doctorDashboard').classList.add('hidden');
        document.getElementById('patientDashboard').classList.add('hidden');
        document.getElementById('landingPage').classList.remove('hidden');

        // Clear forms
        document.getElementById('loginForm')?.reset();
        document.getElementById('registerForm')?.reset();
        
        this.clearAlerts();
    }
}

// Initialize the application
const bioConnect = new BioConnect();

// Global functions for HTML onclick events
window.showLoginModal = () => bioConnect.showLoginModal();
window.showRegisterModal = () => bioConnect.showRegisterModal();
window.closeModals = () => bioConnect.closeModals();
window.switchToRegister = () => bioConnect.switchToRegister();
window.switchToLogin = () => bioConnect.switchToLogin();
window.scrollToFeatures = () => bioConnect.scrollToFeatures();
window.logout = () => bioConnect.logout();