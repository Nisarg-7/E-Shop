const token = localStorage.getItem("token");
const transactionList = document.getElementById("transaction-list");
const totalSpent = document.getElementById("total-spent");
const lastTransaction = document.getElementById("last-transaction");
const transactionCount = document.getElementById("transaction-count");
const simulateBtn = document.getElementById("simulate-payment");

// Fetch transactions
async function loadTransactions() {
  try {
    const response = await fetch("http://127.0.0.1:8000/transaction/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    const transactions = await response.json();

    if (Array.isArray(transactions)) {
      displayTransactions(transactions);
      calculateSummary(transactions);
    } else {
      transactionList.innerHTML = "<p>No transactions found.</p>";
    }
  } catch (error) {
    console.error("Error loading transactions:", error);
  }
}

// Display transactions
function displayTransactions(transactions) {
  transactionList.innerHTML = transactions
    .map(
      (t) => `
      <div class="transaction-card">
        <div class="transaction-header">
          <span><strong>ID:</strong> ${t.id}</span>
          <span><strong>Date:</strong> ${new Date(t.date).toLocaleString()}</span>
        </div>
        <p><strong>Amount:</strong> $${t.amount}</p>
        <p><strong>Status:</strong> ${t.status || "Completed"}</p>
        <p><strong>Payment Method:</strong> ${t.payment_method || "Online"}</p>
      </div>
    `
    )
    .join("");
}

// Calculate total spent and stats
function calculateSummary(transactions) {
  const total = transactions.reduce((sum, t) => sum + (t.amount || 0), 0);
  totalSpent.textContent = `$${total}`;
  transactionCount.textContent = transactions.length;
  if (transactions.length > 0) {
    const latest = transactions[transactions.length - 1];
    lastTransaction.textContent = new Date(latest.date).toLocaleString();
  }
}

// Simulate payment
simulateBtn.addEventListener("click", async () => {
  try {
    const data = {
      amount: Math.floor(Math.random() * 1000) + 500,
      status: "Completed",
      payment_method: "Online",
    };

    const res = await fetch("http://127.0.0.1:8000/transaction/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      alert("Payment simulated successfully!");
      loadTransactions();
    } else {
      alert("Failed to simulate payment.");
    }
  } catch (error) {
    console.error("Error simulating payment:", error);
  }
});

loadTransactions();
