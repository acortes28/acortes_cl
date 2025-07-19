document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Verificar preferencia del usuario
    const userPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = localStorage.getItem('theme');
    
    // Aplicar tema guardado o preferencia del sistema
    if (currentTheme === 'dark' || (!currentTheme && userPrefersDark)) {
        html.setAttribute('data-theme', 'dark');
    }
    
    // Cambiar tema al hacer clic
    themeToggle.addEventListener('click', function() {
        const isDark = html.getAttribute('data-theme') === 'dark';
        html.setAttribute('data-theme', isDark ? 'light' : 'dark');
        localStorage.setItem('theme', isDark ? 'light' : 'dark');
    });
    
    // Escuchar cambios en la preferencia del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const newScheme = e.matches ? 'dark' : 'light';
        html.setAttribute('data-theme', newScheme);
        localStorage.setItem('theme', newScheme);
    });
    
    // Funcionalidad de pestañas en la página de experiencia
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                
                // Remover clase active de todos los botones y contenidos
                tabBtns.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Agregar clase active al botón y contenido seleccionado
                this.classList.add('active');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }
});