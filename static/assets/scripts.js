document.addEventListener('DOMContentLoaded', () => {

    // ✅ Get auth status and URLs from body data attributes
    const isAuthenticated = document.body.dataset.authenticated === "true";
    const loginUrl = document.body.dataset.loginUrl;
    const registerUrl = document.body.dataset.registerUrl;
    const username = document.body.dataset.username || "Guest";

    // ✅ Username display update
    const usernameSpan = document.getElementById('username');
    if (isAuthenticated) {
        usernameSpan.textContent = `Hi, ${username}`;
    } else {
        usernameSpan.innerHTML = `
            <a href="${loginUrl}">Sign In</a> /
            <a href="${registerUrl}">Register</a>
        `;
    }

    // ✅ Highlight active nav
    // ✅ Auto-highlight current page nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.parentElement.classList.add('active');
        }
    });

    // ✅ Add Expense Button Handling
    const addExpenseBtn = document.getElementById('add-expense-btn');
    if (addExpenseBtn) {
        addExpenseBtn.addEventListener('click', (e) => {
            if (!isAuthenticated) {
                e.preventDefault();
                const modal = document.getElementById('loginModal');
                if (modal) {
                    modal.style.display = 'flex';
                } else {
                    alert('Please log in to add an expense.');
                }
            } else {
                // ✅ Only redirect if logged in
                window.location.href = "/add/";  // or {% url 'add_expense' %} rendered in template
            }
        });
    }

    // ✅ Block all protected actions if NOT logged in
    if (!isAuthenticated) {
        document.querySelectorAll('.protected').forEach(element => {
            element.addEventListener('click', (e) => {
                e.preventDefault();
                // Optional: Show modal instead of alert
                const modal = document.getElementById('loginModal');
                if (modal) {
                    modal.style.display = 'flex';
                } else {
                    alert('Please log in to access this section.');
                }
            });
        });
    }

    // ✅ Optional: Dismiss modal on outside click
    const modal = document.getElementById('loginModal');
    if (modal) {
        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

});
