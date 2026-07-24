document.addEventListener('DOMContentLoaded', () => {
    // Check for saved theme preference or respect OS preference
    const prefersDarkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');

    // Apply theme based on saved preference or OS preference
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
    } else if (savedTheme === 'dark') {
        document.body.classList.remove('light-mode');
    } else if (!prefersDarkTheme) {
        document.body.classList.add('light-mode');
    }

    // Theme toggle button functionality
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('click', (e) => {
        e.preventDefault();
        if (document.body.classList.contains('light-mode')) {
            document.body.classList.remove('light-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        }
    });

    // On page load, add "loaded" class to body for animation purposes
    document.body.classList.add('loaded');
    
    // Initialize the intersection observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, { threshold: 0.1 });
    
    // Observe all sections for scroll animations
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
    
    // Observe skill bars for filling animation
    document.querySelectorAll('.skill-bar-fill').forEach(skillBar => {
        observer.observe(skillBar.parentElement);
    });
});



// Active nav highlighting
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('[data-section]');

function highlightNavLink() {
    let scrollY = window.scrollY;
    
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        
        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if(link.getAttribute('data-section') === sectionId) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', highlightNavLink);

// Initialize skill bars
document.addEventListener('DOMContentLoaded', () => {
    const skillBars = document.querySelectorAll('.skill-bar');
    skillBars.forEach(bar => {
        const skill = bar.getAttribute('data-skill');
        const level = bar.getAttribute('data-level');
        
        bar.innerHTML = `
            <div class="flex justify-between mb-1 skill-bar-text">
                <span>${skill}</span>
                <span>${level}%</span>
            </div>
            <div class="h-2 bg-zinc-800 rounded-sm overflow-hidden">
                <div class="h-full bg-white skill-bar-fill" style="--percentage: ${level}%"></div>
            </div>
        `;
    });
});

// Add scroll animation to timeline items
document.addEventListener('DOMContentLoaded', () => {
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach((item, index) => {
        item.style.setProperty('--item-index', index + 1);
    });
});


// chatbot 
document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatToggle || !chatForm) return;

    chatToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        chatWindow.classList.toggle('flex');
    });

    function appendMessage(text, sender) {
        const wrapper = document.createElement('div');
        wrapper.className = sender === 'user'
            ? 'flex flex-col items-end ml-auto max-w-[75%]'
            : 'flex flex-col items-start mr-auto max-w-[75%]';

        const label = document.createElement('div');
        label.className = 'text-xs text-zinc-400 px-1 mb-0.5';
        label.textContent = sender === 'user' ? 'You' : 'Mukesh';

        const bubble = document.createElement('div');
        bubble.className = sender === 'user'
            ? 'bg-blue-600 text-white px-3 py-2 text-sm rounded-2xl rounded-br-md'
            : 'bg-zinc-600 text-white px-3 py-2 text-sm rounded-2xl rounded-bl-md';
        bubble.textContent = text;

        wrapper.appendChild(label);
        wrapper.appendChild(bubble);
        chatMessages.appendChild(wrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        chatInput.value = '';

        try {
            const res = await fetch(chatForm.dataset.apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });
            const data = await res.json();
            appendMessage(data.reply || data.error || "Something went wrong.", 'bot');
        } catch (err) {
            appendMessage("Failed to reach the server.", 'bot');
        }
    });
});



