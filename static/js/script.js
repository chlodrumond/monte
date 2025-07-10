// Menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeBtn = document.getElementById('closeBtn');
    const offcanvasMenu = document.getElementById('offcanvasMenu');
    const overlay = document.getElementById('overlay');

    // Open menu function
    function openMenu() {
        offcanvasMenu.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        closeBtn.focus();
    }

    // Close menu function
    function closeMenu() {
        offcanvasMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Return focus to hamburger button
        if (hamburgerBtn) {
            hamburgerBtn.focus();
        }
    }

    // Event listeners
    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', openMenu);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeMenu);
    }

    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && offcanvasMenu && offcanvasMenu.classList.contains('active')) {
            closeMenu();
        }
    });

    // Login form validation
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            let isValid = true;

            // Reset previous validation states
            [emailInput, passwordInput].forEach(input => {
                if (input) {
                    input.classList.remove('is-invalid');
                }
            });

            // Email validation
            if (emailInput) {
                const emailValue = emailInput.value.trim();
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                
                if (!emailValue || !emailRegex.test(emailValue)) {
                    emailInput.classList.add('is-invalid');
                    isValid = false;
                }
            }

            // Password validation
            if (passwordInput) {
                const passwordValue = passwordInput.value.trim();
                
                if (!passwordValue || passwordValue.length < 1) {
                    passwordInput.classList.add('is-invalid');
                    isValid = false;
                }
            }

            // Prevent form submission if validation fails
            if (!isValid) {
                e.preventDefault();
                
                // Focus on first invalid field
                const firstInvalid = loginForm.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
        });

        // Real-time validation
        const inputs = loginForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateSingleField(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateSingleField(this);
                }
            });
        });
    }

    // Single field validation function
    function validateSingleField(field) {
        const fieldType = field.type;
        const fieldValue = field.value.trim();

        field.classList.remove('is-invalid');

        if (fieldType === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!fieldValue || !emailRegex.test(fieldValue)) {
                field.classList.add('is-invalid');
            }
        } else if (fieldType === 'password') {
            if (!fieldValue || fieldValue.length < 1) {
                field.classList.add('is-invalid');
            }
        }
    }

    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message && message.parentNode) {
                const bsAlert = new bootstrap.Alert(message);
                bsAlert.close();
            }
        }, 5000); // Hide after 5 seconds
    });

    // Smooth scrolling for anchor links
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

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...';
                submitBtn.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
});

// Utility functions for enhanced UX
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced responsive behavior
function handleResize() {
    const offcanvasMenu = document.getElementById('offcanvasMenu');
    const overlay = document.getElementById('overlay');
    
    // Close menu on resize to prevent layout issues
    if (window.innerWidth > 768 && offcanvasMenu && offcanvasMenu.classList.contains('active')) {
        offcanvasMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Add resize listener with debouncing
window.addEventListener('resize', debounce(handleResize, 250));

// Preload images for better performance
function preloadImages() {
    const imageUrls = [
        '/static/img/logo-monte.png'
    ];
    
    imageUrls.forEach(url => {
        const img = new Image();
        img.src = url;
    });
}

// Initialize preloading
preloadImages();
