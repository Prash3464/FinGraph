function searchExpenses() {
    const title = document.getElementById("search-title").value;
    const date = document.getElementById("search-month").value;

    fetch(`/search/?title=${title}&date=${date}`)
        .then(response => {
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                return response.json();
            } else {
                throw new Error("Expected JSON, got something else");
            }
        })
        .then(data => {
            const container = document.getElementById("expense-results");
            container.innerHTML = ''; // Clear previous results

            if (data.success && data.expenses.length > 0) {
                data.expenses.forEach(exp => {
                    const wrapper = document.createElement("div");
                    wrapper.className = "expense-item";
                    wrapper.innerHTML = `
    <div class="summary" onclick="toggleDetail(${exp.id})">
        <strong>${exp.title}</strong><p class="amount"> ₹${exp.amount}</p><span class="date">${exp.date}</span>
    </div>
    <div class="details" id="detail-${exp.id}" style="display: none;">
        <form onsubmit="updateExpense(event, ${exp.id})">
            <div class="inline-group">
                <label>Title:</label>
                <input name="title" value="${exp.title}" readonly required>

                <label>Category:</label>
                <input name="category" value="${exp.category}" readonly required>

            </div>

            <div class="inline-group">
                <label>Amount:</label>
                <input name="amount" type="number" value="${exp.amount}" readonly required>
                <label>Date:</label>
                <input name="date" type="date" value="${exp.date}" readonly>
            </div>
            <div class="inline-group">
                <label>Description:</label>
                <textarea name="description" readonly>${exp.description || ''}</textarea>

                <label>Payment:</label>
                <select name="payment_method" disabled>
                    <option value="Cash" ${exp.payment_method === 'Cash' ? 'selected' : ''}>Cash</option>
                    <option value="Card" ${exp.payment_method === 'Card' ? 'selected' : ''}>Card</option>
                    <option value="UPI" ${exp.payment_method === 'UPI' ? 'selected' : ''}>UPI</option>
                </select>
            </div>

            <div class="inline-group">
                <button type="submit">Update</button>
                <button type="button" onclick=" ">Delete</button>
            </div>
        </form>
    </div>
`;

                    container.appendChild(wrapper);
                });
            } else {
                container.innerHTML = '<div>No matching expense found.</div>';
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
}

function toggleDetail(id) {
    // Close all other open detail sections
    const allDetails = document.querySelectorAll(".details");
    allDetails.forEach(div => {
        if (div.id !== `detail-${id}`) {
            div.style.display = "none";
        }
    });

    // Toggle the clicked one
    const currentDetail = document.getElementById(`detail-${id}`);
    if (currentDetail.style.display === "none" || currentDetail.style.display === "") {
        currentDetail.style.display = "block";
    } else {
        currentDetail.style.display = "none";
    }
}

function updateExpense(event, id) {
    event.preventDefault();
    const form = event.target;
    const isReadOnly = form.title.hasAttribute("readonly");

    if (isReadOnly) {
        // Make editable
        form.querySelectorAll("input, textarea").forEach(el => el.removeAttribute("readonly"));
        form.payment_method.removeAttribute("disabled");
        form.querySelector("button[type='submit']").innerText = "Save";
    } else {
        // Save the changes
        const formData = {
            title: form.title.value,
            category: form.category.value,
            amount: form.amount.value,
            date: form.date.value,
            description: form.description.value,
            payment_method: form.payment_method.value,
        };

        fetch(`/update-expense/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify(formData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Expense updated successfully!");

                    // After save, disable again
                    form.querySelectorAll("input, textarea").forEach(el => el.setAttribute("readonly", true));
                    form.payment_method.setAttribute("disabled", true);
                    form.querySelector("button[type='submit']").innerText = "Update";
                } else {
                    console.error("Failed to update: " + data.message);
                }
            })
            .catch(error => {
                console.error("Update error:", error);
                console.error("Error while updating.");
            });
    }
}

function getCSRFToken() {
    const cookie = document.cookie.match(/csrftoken=([\w-]+)/);
    return cookie ? cookie[1] : "";
}


// delet item in app
let deleteTargetId = null;

function deleteExpense(id) {
    deleteTargetId = id;
    document.getElementById("delete-confirm-modal").style.display = "flex";
}

function closeDeleteModal() {
    document.getElementById("delete-confirm-modal").style.display = "none";
    deleteTargetId = null;
}

document.getElementById("confirm-delete-btn").addEventListener("click", () => {
    if (!deleteTargetId) return;

    fetch(`/delete-expense/${deleteTargetId}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //            alert("Deleted successfully!");
                searchExpenses();
            } else {
                alert("Failed to delete: " + data.message);
            }
        })
        .catch(error => {
            console.error("Delete error:", error);
            alert("Error deleting expense.");
        })
        .finally(() => {
            closeDeleteModal();
        });
});



function handleCancel() {
    window.history.back();
    // Or:
    // document.querySelector('.expense-edit-form-container').style.display = 'none';
}
