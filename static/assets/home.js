document.getElementById("export-trigger-btn").addEventListener("click", () => {
  document.getElementById("export-modal").classList.remove("hidden");
});

document.querySelector(".cancel-btn").addEventListener("click", () => {
  document.getElementById("export-modal").classList.add("hidden");
});

// Enable/disable month input based on radio selection
document.querySelectorAll("input[name='export_option']").forEach(radio => {
  radio.addEventListener("change", () => {
    const monthInput = document.getElementById("export-month-input");
    if (radio.value === "month") {
      monthInput.disabled = false;
      monthInput.required = true;
    } else {
      monthInput.disabled = true;
      monthInput.required = false;
    }
  });
});
