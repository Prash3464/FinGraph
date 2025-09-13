// auth-modal.js

window.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('loginModal');

    // Example check: if user is not logged in
    const isLoggedIn = localStorage.getItem('username');

    // Show modal if NOT logged in
    if (!isLoggedIn) {
        modal.style.display = 'flex';
    }

    // Optional: close modal on outside click
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
});
