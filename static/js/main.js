// // Main JavaScript for AI Training Platform

// // Modal functionality
// const modal = document.getElementById('videoModal');
// const closeBtn = document.getElementsByClassName('close')[0];
// let currentWatchingVideo = null;

// function watchVideo(videoId) {
//     currentWatchingVideo = videoId;
//     const video = findVideoById(videoId);
    
//     if (video) {
//         document.getElementById('videoTitle').textContent = video.title;
//         modal.style.display = 'block';
        
//         // Simulate video playing
//         simulateVideoProgress();
//     }
// }

// function findVideoById(videoId) {
//     const topVideos = [
//         {id: 101, title: 'AI in 5 Minutes'},
//         {id: 102, title: 'Machine Learning Explained'},
//         {id: 103, title: 'Deep Learning Basics'},
//         {id: 104, title: 'Natural Language Processing'},
//         {id: 105, title: 'Computer Vision 101'},
//         {id: 106, title: 'AI vs ML vs DL'},
//         {id: 107, title: 'AI Applications Today'},
//         {id: 108, title: 'AI Ethics & Privacy'},
//         {id: 109, title: 'Chatbots & Virtual Assistants'},
//         {id: 110, title: 'AI Career Guide'}
//     ];
    
//     return topVideos.find(v => v.id === videoId);
// }

// function simulateVideoProgress() {
//     const placeholder = document.querySelector('.video-placeholder');
//     if (placeholder) {
//         placeholder.innerHTML = `
//             <div class="play-icon">▶️</div>
//             <p>Playing video...</p>
//             <div style="width: 80%; background: rgba(255,255,255,0.3); height: 4px; border-radius: 2px; margin: 20px auto;">
//                 <div style="width: 0%; background: white; height: 100%; animation: progress 3s linear forwards;"></div>
//             </div>
//         `;
//     }
// }

// async function markVideoWatched() {
//     if (!currentWatchingVideo) return;
    
//     try {
//         const response = await fetch('/complete_video', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({
//                 video_id: currentWatchingVideo
//             })
//         });
        
//         const data = await response.json();
        
//         if (data.success) {
//             modal.style.display = 'none';
//             location.reload();
//         }
//     } catch (error) {
//         console.error('Error marking video as watched:', error);
//         alert('Failed to update progress. Please try again.');
//     }
// }

// // Close modal
// if (closeBtn) {
//     closeBtn.onclick = function() {
//         modal.style.display = 'none';
//     }
// }

// window.onclick = function(event) {
//     if (event.target == modal) {
//         modal.style.display = 'none';
//     }
// }

// // Add CSS animation for video progress
// const style = document.createElement('style');
// style.textContent = `
//     @keyframes progress {
//         from { width: 0%; }
//         to { width: 100%; }
//     }
// `;
// document.head.appendChild(style);

// // Smooth scroll for navigation
// document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//     anchor.addEventListener('click', function (e) {
//         e.preventDefault();
//         const target = document.querySelector(this.getAttribute('href'));
//         if (target) {
//             target.scrollIntoView({
//                 behavior: 'smooth'
//             });
//         }
//     });
// });

// // Form validation
// const forms = document.querySelectorAll('form');
// forms.forEach(form => {
//     form.addEventListener('submit', function(e) {
//         const inputs = form.querySelectorAll('input[required]');
//         let isValid = true;
        
//         inputs.forEach(input => {
//             if (!input.value.trim()) {
//                 isValid = false;
//                 input.style.borderColor = '#ef4444';
//             } else {
//                 input.style.borderColor = '#e2e8f0';
//             }
//         });
        
//         if (!isValid) {
//             e.preventDefault();
//             alert('Please fill in all required fields');
//         }
//     });
// });

// // Initialize on page load
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('AI Training Platform initialized ✓');
// });

// ====================================
// ENHANCED MAIN.JS - AI TRAINING PLATFORM
// Modern Interactions & Animations
// ====================================

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 AI Training Platform initialized');
    initializeApp();
});

// ====================================
// INITIALIZATION
// ====================================

function initializeApp() {
    setupAnimations();
    setupModals();
    setupFormValidation();
    setupSmoothScroll();
    setupTooltips();
    addLoadingStates();
}

// ====================================
// MODAL FUNCTIONALITY
// ====================================

const modal = document.getElementById('videoModal');
const closeBtn = document.getElementsByClassName('close')[0];
let currentWatchingVideo = null;

function watchVideo(videoId) {
    currentWatchingVideo = videoId;
    const video = findVideoById(videoId);
    
    if (video) {
        document.getElementById('videoTitle').textContent = video.title;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scroll
        
        // Add entrance animation
        setTimeout(() => {
            modal.querySelector('.modal-content').style.animation = 
                'slideUp 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        }, 10);
        
        // Simulate video playing
        simulateVideoProgress();
    }
}

function findVideoById(videoId) {
    const topVideos = [
        {id: 101, title: 'AI in 5 Minutes', duration: '5:00'},
        {id: 102, title: 'Machine Learning Explained', duration: '8:30'},
        {id: 103, title: 'Deep Learning Basics', duration: '12:15'},
        {id: 104, title: 'Natural Language Processing', duration: '10:45'},
        {id: 105, title: 'Computer Vision 101', duration: '9:20'},
        {id: 106, title: 'AI vs ML vs DL', duration: '6:50'},
        {id: 107, title: 'AI Applications Today', duration: '11:00'},
        {id: 108, title: 'AI Ethics & Privacy', duration: '13:30'},
        {id: 109, title: 'Chatbots & Virtual Assistants', duration: '7:40'},
        {id: 110, title: 'AI Career Guide', duration: '15:20'}
    ];
    
    return topVideos.find(v => v.id === videoId);
}

function simulateVideoProgress() {
    const placeholder = document.querySelector('.video-placeholder');
    if (placeholder) {
        placeholder.innerHTML = `
            <div class="play-icon" style="animation: pulse 2s ease infinite;">▶️</div>
            <p style="font-size: 1.2rem; margin-bottom: 20px;">Playing video...</p>
            <div style="width: 80%; background: rgba(255,255,255,0.3); height: 6px; border-radius: 3px; margin: 20px auto; overflow: hidden;">
                <div style="width: 0%; background: white; height: 100%; box-shadow: 0 0 10px rgba(255,255,255,0.5); animation: videoProgress 8s ease-in-out forwards;"></div>
            </div>
            <p style="font-size: 0.9rem; opacity: 0.8;">Duration: ${findVideoById(currentWatchingVideo)?.duration || '0:00'}</p>
        `;
        
        // Add animation keyframe
        if (!document.getElementById('videoProgressAnimation')) {
            const style = document.createElement('style');
            style.id = 'videoProgressAnimation';
            style.textContent = `
                @keyframes videoProgress {
                    from { width: 0%; }
                    to { width: 100%; }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

async function markVideoWatched() {
    if (!currentWatchingVideo) return;
    
    const button = event.target;
    button.classList.add('loading');
    button.textContent = 'Saving...';
    
    try {
        const response = await fetch('/complete_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_id: currentWatchingVideo
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('✓ Video marked as watched!', 'success');
            
            setTimeout(() => {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
                location.reload();
            }, 1000);
        }
    } catch (error) {
        console.error('Error marking video as watched:', error);
        showNotification('❌ Failed to update progress', 'error');
        button.classList.remove('loading');
        button.textContent = 'Mark as Watched';
    }
}

// Close modal
function setupModals() {
    if (closeBtn) {
        closeBtn.onclick = function() {
            closeModal();
        }
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    }
    
    // ESC key to close modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal && modal.style.display === 'block') {
            closeModal();
        }
    });
}

function closeModal() {
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ====================================
// NOTIFICATIONS
// ====================================

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981, #059669)' : 'linear-gradient(135deg, #ef4444, #dc2626)'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        font-weight: 600;
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.4s ease-in';
        setTimeout(() => notification.remove(), 400);
    }, 3000);
    
    // Add animation keyframes if not exists
    if (!document.getElementById('notificationAnimations')) {
        const style = document.createElement('style');
        style.id = 'notificationAnimations';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// ====================================
// SMOOTH SCROLLING
// ====================================

function setupSmoothScroll() {
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
}

// ====================================
// FORM VALIDATION & ENHANCEMENT
// ====================================

function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('invalid')) {
                    validateInput(this);
                }
            });
        });
        
        // Form submission
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('❌ Please fill in all required fields correctly', 'error');
            } else {
                // Add loading state to submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.textContent = 'Processing...';
                }
            }
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    if (!value) {
        isValid = false;
        errorMessage = 'This field is required';
    } else if (input.type === 'email' && !isValidEmail(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
    } else if (input.type === 'password' && value.length < 6) {
        isValid = false;
        errorMessage = 'Password must be at least 6 characters';
    }
    
    if (isValid) {
        input.classList.remove('invalid');
        input.classList.add('valid');
        input.style.borderColor = '#10b981';
        removeErrorMessage(input);
    } else {
        input.classList.remove('valid');
        input.classList.add('invalid');
        input.style.borderColor = '#ef4444';
        showErrorMessage(input, errorMessage);
    }
    
    return isValid;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showErrorMessage(input, message) {
    removeErrorMessage(input);
    
    const error = document.createElement('div');
    error.className = 'error-message';
    error.textContent = message;
    error.style.cssText = `
        color: #ef4444;
        font-size: 0.85rem;
        margin-top: 5px;
        animation: fadeIn 0.3s ease;
    `;
    
    input.parentElement.appendChild(error);
}

function removeErrorMessage(input) {
    const existingError = input.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

// ====================================
// ANIMATIONS & EFFECTS
// ====================================

function setupAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe sections
    document.querySelectorAll('.section, .module-card, .video-card').forEach(el => {
        observer.observe(el);
    });
    
    // Add hover effects to cards
    addCardHoverEffects();
}

function addCardHoverEffects() {
    const cards = document.querySelectorAll('.module-card, .video-card, .resource-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// ====================================
// LOADING STATES
// ====================================

function addLoadingStates() {
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-success');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.onclick) {
                // Button will show loading state
            }
        });
    });
}

// ====================================
// TOOLTIPS
// ====================================

function setupTooltips() {
    const elementsWithTitle = document.querySelectorAll('[title]');
    
    elementsWithTitle.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            showTooltip(this, this.getAttribute('title'));
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(30, 41, 59, 0.95);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        z-index: 10000;
        pointer-events: none;
        animation: fadeIn 0.2s ease;
        backdrop-filter: blur(10px);
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// ====================================
// UTILITY FUNCTIONS
// ====================================

// Debounce function for performance
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

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// ====================================
// PERFORMANCE MONITORING
// ====================================

// Log page load performance
window.addEventListener('load', () => {
    const perfData = performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`📊 Page loaded in ${pageLoadTime}ms`);
});

// ====================================
// ACCESSIBILITY ENHANCEMENTS
// ====================================

// Tab navigation enhancement
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// Add keyboard navigation styles
const style = document.createElement('style');
style.textContent = `
    body.keyboard-navigation *:focus {
        outline: 3px solid #6366f1 !important;
        outline-offset: 2px;
    }
`;
document.head.appendChild(style);

// ====================================
// ERROR HANDLING
// ====================================

window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    // You could send this to your error tracking service
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You could send this to your error tracking service
});

// ====================================
// CONSOLE MESSAGE
// ====================================

console.log('%c🤖 AI Training Platform', 'color: #6366f1; font-size: 24px; font-weight: bold;');
console.log('%cWelcome! The platform is ready.', 'color: #10b981; font-size: 14px;');
console.log('%c💡 Tip: Check out the modern animations and interactions!', 'color: #8b5cf6; font-size: 12px;');

// ====================================
// EXPORT FUNCTIONS (if using modules)
// ====================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        watchVideo,
        markVideoWatched,
        showNotification
    };
}