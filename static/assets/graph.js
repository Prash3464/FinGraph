// plotly-home.js

document.addEventListener("DOMContentLoaded", () => {
    const chartContainer = document.getElementById('home-expense-chart');
    if (!chartContainer) return; // exit if chart div not found



    const data = [{
        x: labels,
        y: totals,
        type: 'bar',
        marker: {
            color: "#29ABE2",
        }
    }];

    const layout = {
        title: 'Monthly Expenses Overview',
        xaxis: {
            title: 'Month',
            tickangle: -45
        },
        yaxis: {
            title: 'Amount (₹)'
        },
        plot_bgcolor: "#1f1f1f",       // Chart plot area background
        paper_bgcolor: "#121212",      // Entire chart background
        font: {
            color: "white"             // Global font color
        },
        margin: {
            t: 50, b: 60, l: 60, r: 30
        },
        responsive: true
    };

    const config = {
        responsive: true,
        displayModeBar: false // hide plotly menu
    };

    Plotly.newPlot(chartContainer, data, layout, config);
});
