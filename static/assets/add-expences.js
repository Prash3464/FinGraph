// Auto-fill today’s date if left blank
document.getElementById("expense-form").addEventListener("submit", function (e) {
    const dateInput = document.getElementById("date");
    if (!dateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }
});


function handleCancel() {
    // Go back in browser history OR remove/hide form dynamically
    console.log("Cancel button clicked");
    window.history.back();  // Use this if form opened as page
    // OR you can do something like:
    // document.querySelector('.expense-form-container').style.display = 'none';
}

