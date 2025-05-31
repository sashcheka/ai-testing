// Store expenses in an array
let expenses = [];

// DOM Elements
const expenseForm = document.getElementById('expenseForm');
const expenseTableBody = document.getElementById('expenseTableBody');
const calculateBtn = document.getElementById('calculateBtn');
const totalExpensesElement = document.getElementById('totalExpenses');
const averageDailyElement = document.getElementById('averageDaily');
const topExpensesElement = document.getElementById('topExpenses');

// Format currency
const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
};

// Add new expense
const addExpense = (category, amount) => {
    const expense = {
        id: Date.now(),
        category,
        amount: parseFloat(amount)
    };
    expenses.push(expense);
    updateExpenseTable();
    // Remove automatic calculation
};

// Delete expense
const deleteExpense = (id) => {
    expenses = expenses.filter(expense => expense.id !== id);
    updateExpenseTable();
    // Remove automatic calculation
};

// Update expense table
const updateExpenseTable = () => {
    expenseTableBody.innerHTML = '';
    
    if (expenses.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="3" style="text-align: center;">No expenses added yet</td>
        `;
        expenseTableBody.appendChild(row);
        return;
    }

    expenses.forEach(expense => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${expense.category}</td>
            <td>${formatCurrency(expense.amount)}</td>
            <td>
                <button class="delete-btn" onclick="deleteExpense(${expense.id})">
                    Delete
                </button>
            </td>
        `;
        expenseTableBody.appendChild(row);
    });
};

// Calculate and update results
const updateResults = () => {
    if (expenses.length === 0) {
        totalExpensesElement.textContent = formatCurrency(0);
        averageDailyElement.textContent = formatCurrency(0);
        topExpensesElement.innerHTML = '<li>No expenses added yet</li>';
        return;
    }

    // Calculate total expenses
    const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
    totalExpensesElement.textContent = formatCurrency(total);

    // Calculate average daily expense (assuming 30 days)
    const averageDaily = total / 30;
    averageDailyElement.textContent = formatCurrency(averageDaily);

    // Get top 3 expenses
    const topExpenses = [...expenses]
        .sort((a, b) => b.amount - a.amount)
        .slice(0, 3);

    topExpensesElement.innerHTML = topExpenses
        .map(expense => `
            <li>
                ${expense.category}: ${formatCurrency(expense.amount)}
            </li>
        `)
        .join('');
};

// Event Listeners
expenseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const category = document.getElementById('category').value.trim();
    const amount = document.getElementById('amount').value;

    if (category && amount) {
        addExpense(category, amount);
        expenseForm.reset();
    }
});

// Add click event listener for calculate button
calculateBtn.addEventListener('click', updateResults);

// Initialize the table
updateExpenseTable();
// Initialize results with zeros
updateResults(); 