document.addEventListener("DOMContentLoaded", function () {
  // 🔁 Month Change → Reload Page with Params
  const monthInput = document.getElementById("analytics-month");
  if (monthInput) {
    monthInput.addEventListener("change", () => {
      const month = monthInput.value;
      const view = document.getElementById("analytics-view-toggle")?.value || 'daily';
      window.location.href = `/analytics/?month=${month}&view=${view}`;
    });
  }

  // 🔁 View Toggle Change (daily/monthly)
  const viewToggle = document.getElementById("analytics-view-toggle");
  if (viewToggle) {
    viewToggle.addEventListener("change", () => {
      const month = document.getElementById("analytics-month").value;
      const view = viewToggle.value;
      window.location.href = `/analytics/?month=${month}&view_type=${view}`;
    });
  };

  // 📊 Render Plotly Chart
  // Check if chart div and data exist
  const chart = document.getElementById("analytics-chart");
  if (!chart || !window.analyticsLabels || !window.analyticsTotals) return;

  // Extract just the day from full date string for x-axis
  const days = analyticsLabels.map(date => {
    const d = new Date(date);
    return d.getDate().toString().padStart(2, '0');
  });

  // Prepare Plotly chart data
  const trace = {
    x: days,
    y: analyticsTotals,
    type: "bar",
    marker: {
      color: "#29ABE2",
    }
  };

  const layout = {
    title: "Daily Expenses",
    paper_bgcolor: "#1e1e2f",
    plot_bgcolor: "#1e1e2f",
    font: { color: "#fff" },
    xaxis: { title: "Day", tickfont: { color: "#fff" }, titlefont: { color: "#fff" } },
    yaxis: { title: "₹ Amount", tickfont: { color: "#fff" }, titlefont: { color: "#fff" } },
    margin: {
      t: 87, b: 60, l: 40, r: 30
    }
  };

  Plotly.newPlot(chart, [trace], layout, { responsive: true });


  // Month picker change → reload page with selected month
  document.getElementById("analytics-month").addEventListener("change", (e) => {
    const month = e.target.value;
    window.location.href = `/analytics/?month=${month}`;
  });

  // ➕ Add Button → Redirect to Add Page
  const addBtn = document.getElementById("add-expense-btn");
  if (addBtn) {
    addBtn.addEventListener("click", () => {
      window.location.href = "/add/";
    });
  }





});

function getCSRFToken() {
  const cookie = document.cookie.match(/csrftoken=([\w-]+)/);
  return cookie ? cookie[1] : "";
}

// delete expences
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
        console.log("Deleted successfully!");
        location.reload(true)

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
