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
    
    // Cambiar tema al hacer clic con animación suave
    themeToggle.addEventListener('click', function() {
        const isDark = html.getAttribute('data-theme') === 'dark';
        
        // Agregar transición suave
        html.style.transition = 'all 0.3s ease';
        
        html.setAttribute('data-theme', isDark ? 'light' : 'dark');
        localStorage.setItem('theme', isDark ? 'light' : 'dark');
        
        // Efecto de rotación en el botón
        this.style.transform = 'rotate(180deg)';
        setTimeout(() => {
            this.style.transform = 'rotate(0deg)';
        }, 300);
    });
    
    // Escuchar cambios en la preferencia del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const newScheme = e.matches ? 'dark' : 'light';
        html.style.transition = 'all 0.3s ease';
        html.setAttribute('data-theme', newScheme);
        localStorage.setItem('theme', newScheme);
    });
    
    // Animación de scroll suave para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Efecto de aparición al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observar elementos para animación
    document.querySelectorAll('.link-card, .hero-content, .hero-image').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
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
    
    // Efecto de hover mejorado para las tarjetas
    document.querySelectorAll('.link-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Efecto de parallax suave para el hero
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        if (hero) {
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        }
    });
    
    // Funcionalidad del modal de PDF
    const pdfModal = document.getElementById('pdf-modal');
    const pdfIframe = document.getElementById('pdf-iframe');
    const pdfDownloadBtn = document.getElementById('pdf-download-btn');
    const pdfCloseBtn = document.getElementById('pdf-close-btn');
    const pdfViewerBtns = document.querySelectorAll('.pdf-viewer-btn');
    
    let currentPdfUrl = '';
    
    // Abrir modal de PDF
    pdfViewerBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const pdfUrl = this.getAttribute('data-pdf-url');
            currentPdfUrl = pdfUrl;
            
            // Configurar el iframe
            pdfIframe.src = pdfUrl;
            
            // Mostrar el modal
            pdfModal.classList.add('show');
            document.body.style.overflow = 'hidden'; // Prevenir scroll del body
            
            // Efecto de entrada
            setTimeout(() => {
                pdfModal.style.opacity = '1';
            }, 10);
        });
    });
    
    // Cerrar modal
    function closePdfModal() {
        pdfModal.classList.remove('show');
        document.body.style.overflow = ''; // Restaurar scroll del body
        pdfIframe.src = ''; // Limpiar el iframe
        currentPdfUrl = '';
    }
    
    // Eventos para cerrar el modal
    pdfCloseBtn.addEventListener('click', closePdfModal);
    
    // Cerrar con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && pdfModal.classList.contains('show')) {
            closePdfModal();
        }
    });
    
    // Cerrar haciendo clic fuera del modal
    pdfModal.addEventListener('click', function(e) {
        if (e.target === pdfModal) {
            closePdfModal();
        }
    });
    
    // Descargar PDF
    pdfDownloadBtn.addEventListener('click', function() {
        if (currentPdfUrl) {
            // Crear un enlace temporal para descargar
            const link = document.createElement('a');
            link.href = currentPdfUrl;
            link.download = 'cv_alejandro_cortes.pdf';
            link.target = '_blank';
            
            // Agregar al DOM, hacer clic y remover
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Efecto visual de descarga
            this.style.transform = 'scale(0.8)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 200);
        }
    });


});