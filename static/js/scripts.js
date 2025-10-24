// Navigation Toggle for Mobile (robust guards)
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');
const navLinks = document.querySelectorAll('.nav-links li');
const navLinkAnchors = document.querySelectorAll('.nav-links a');

if (burger && nav) {
    burger.addEventListener('click', () => {
        // Toggle Nav
        nav.classList.toggle('active');
        burger.classList.toggle('active');
        
        // Animate Links (optional)
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.08}s`;
            }
        });
    });
}

// Close mobile nav when a link is clicked (improves UX)
if (nav && navLinkAnchors && burger) {
    navLinkAnchors.forEach(a => {
        a.addEventListener('click', () => {
            if (nav.classList.contains('active')) {
                nav.classList.remove('active');
                burger.classList.remove('active');
            }
        });
    });
}

// NOTE: floating-object interaction removed — no .floating-object elements present in current pages

// Scroll Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe timeline items
document.addEventListener('DOMContentLoaded', () => {
    const timelineItems = document.querySelectorAll('.timeline-content');
    const resumeSections = document.querySelectorAll('.resume-section');
    const animItems = document.querySelectorAll('.animate-on-scroll');

    timelineItems.forEach(item => observer.observe(item));
    resumeSections.forEach(section => observer.observe(section));
    animItems.forEach(el => observer.observe(el));
});

// Form Validation
const contactForm = document.getElementById('contact-form');

if (contactForm) {
    const firstName = document.getElementById('first-name');
    const lastName = document.getElementById('last-name');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    
    const firstNameError = document.getElementById('first-name-error');
    const lastNameError = document.getElementById('last-name-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const confirmPasswordError = document.getElementById('confirm-password-error');
    
    function validateFirstName() {
        if (firstName.value.trim() === '') {
            showError(firstName, firstNameError, 'Please enter your first name');
            return false;
        } else {
            hideError(firstName, firstNameError);
            return true;
        }
    }
    
    function validateLastName() {
        if (lastName.value.trim() === '') {
            showError(lastName, lastNameError, 'Please enter your last name');
            return false;
        } else {
            hideError(lastName, lastNameError);
            return true;
        }
    }
    
    function validateEmail() {
        const emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
        if (email.value.trim() === '') {
            showError(email, emailError, 'Please enter your email address');
            return false;
        } else if (!emailRegex.test(email.value)) {
            showError(email, emailError, 'Please enter a valid email address');
            return false;
        } else {
            hideError(email, emailError);
            return true;
        }
    }
    
    function validatePassword() {
        if (password.value === '') {
            showError(password, passwordError, 'Please enter a password');
            return false;
        } else if (password.value.length < 8) {
            showError(password, passwordError, 'Password must be at least 8 characters');
            return false;
        } else {
            hideError(password, passwordError);
            return true;
        }
    }
    
    function validateConfirmPassword() {
        if (confirmPassword.value === '') {
            showError(confirmPassword, confirmPasswordError, 'Please confirm your password');
            return false;
        } else if (confirmPassword.value !== password.value) {
            showError(confirmPassword, confirmPasswordError, 'Passwords do not match');
            return false;
        } else {
            hideError(confirmPassword, confirmPasswordError);
            return true;
        }
    }
    
    function showError(input, errorElement, message) {
        input.parentElement.classList.add('error');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    function hideError(input, errorElement) {
        input.parentElement.classList.remove('error');
        errorElement.style.display = 'none';
    }
    
    // Real-time validation
    firstName.addEventListener('blur', validateFirstName);
    lastName.addEventListener('blur', validateLastName);
    email.addEventListener('blur', validateEmail);
    password.addEventListener('blur', validatePassword);
    confirmPassword.addEventListener('blur', validateConfirmPassword);
    
    // Form submission
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const isFirstNameValid = validateFirstName();
        const isLastNameValid = validateLastName();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();
        
        if (isFirstNameValid && isLastNameValid && isEmailValid && 
            isPasswordValid && isConfirmPasswordValid) {
            // Form is valid, submit it
            contactForm.submit();
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});