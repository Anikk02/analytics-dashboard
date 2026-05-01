const API_BASE = 'http://127.0.0.1:8000/api';

// Fetch Helper
async function safeFetch(url, fallback = []) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(url + " failed");
        return await res.json();
    } catch (err) {
        console.error("API error:", url, err);
        return fallback;
    }
}

// Load Dashboard
async function loadDashboard() {
    try {
        const revenue = await safeFetch(`${API_BASE}/revenue`);
        const categories = await safeFetch(`${API_BASE}/categories`);
        const customers = await safeFetch(`${API_BASE}/top-customers`);
        const regions = await safeFetch(`${API_BASE}/regions`);

        console.log("RAW DATA CHECK:", { revenue, categories, customers, regions });

        if (!Array.isArray(revenue) || revenue.length === 0) {
            showError("Revenue data missing");
            return;
        }

        renderRevenueChart(revenue);
        renderCategoryChart(categories);
        renderCustomersTable(customers);

        document.getElementById('topCustomerCount').innerText = customers.length;
        document.getElementById('regionCount').innerText = regions.length;

    } catch (error) {
        console.error("Dashboard load failed:", error);
        showError("Failed to load dashboard data");
    }
}

// Simple UI error handler
function showError(msg) {
    const box = document.getElementById("errorBox");
    if (box) box.innerText = msg;
    console.error(msg);
}

// ========== CHARTS ==========

// destroy old chart if exists
let revenueChartInstance = null;
let categoryChartInstance = null;

function renderRevenueChart(data) {

    const labels = data.map(d => d.order_year_month);
    const values = data.map(d => Number(d.revenue || d.total_revenue || 0));

    if (revenueChartInstance) revenueChartInstance.destroy();

    revenueChartInstance = new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: "Revenue",
                data: values,
                borderColor: "#38bdf8",
                tension: 0.3
            }]
        }
    });
}

function renderCategoryChart(data) {

    const labels = data.map(d => d.category);
    const values = data.map(d => Number(d.total_revenue || d.revenue || 0));

    if (categoryChartInstance) categoryChartInstance.destroy();

    categoryChartInstance = new Chart(document.getElementById("categoryChart"), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: "Revenue by Category",
                data: values,
                backgroundColor: "#22c55e"
            }]
        }
    });
}

// ========== TABLE ==========

function renderCustomersTable(data) {
    const tbody = document.querySelector("#customersTable tbody");
    tbody.innerHTML = "";

    let totalRevenue = 0;

    data.forEach(c => {
        const spend = Number(c.total_spend || 0);
        totalRevenue += spend;

        const row = `
        <tr>
            <td>${c.name || ""}</td>
            <td>${c.region || ""}</td>
            <td>$${spend.toFixed(2)}</td>
            <td>${c.churned ? "⚠ Yes" : "No"}</td>
        </tr>`;

        tbody.innerHTML += row;
    });

    document.getElementById('totalRevenue').innerText =
        `$${totalRevenue.toFixed(2)}`;
}

// INIT
loadDashboard();