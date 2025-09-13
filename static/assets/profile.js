function enableEdit() {
    const inputs = document.querySelectorAll('#profileForm input');
    inputs.forEach(input => input.disabled = false);

    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('saveBtn').style.display = 'inline-block';
}

document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('ul.messages li');
    messages.forEach(msg => {
        // Hide after 4 seconds (adjust as needed)
        setTimeout(() => {
            msg.classList.add('hidden');
            // Remove from DOM after fade out
            setTimeout(() => {
                msg.remove();
            }, 500); // match with CSS transition duration
        }, 4000); // 4 seconds visible
    });
});