from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
FILE_NAME = "expenses.json"

# Load and save expenses
def load_expenses():
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILE_NAME, 'w') as file:
        json.dump(expenses, file, indent=4)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add Expense route
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date'] if request.form['date'] else datetime.today().strftime('%Y-%m-%d')

        expense = {
            'amount': amount,
            'category': category,
            'date': date
        }

        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)
        return redirect(url_for('index'))
    return render_template('add_expense.html')

# Summary route
@app.route('/summary')
def summary():
    expenses = load_expenses()
    total_spending = sum(exp['amount'] for exp in expenses)
    categories = {}
    for exp in expenses:
        category = exp['category']
        categories[category] = categories.get(category, 0) + exp['amount']

    return render_template('summary.html', total_spending=total_spending, categories=categories)

# Modify Expense route
@app.route('/modify', methods=['GET', 'POST'])
def modify_expense():
    expenses = load_expenses()
    if request.method == 'POST':
        index = int(request.form['index']) - 1
        action = request.form['action']
        if action == 'delete':
            expenses.pop(index)
        elif action == 'edit':
            expenses[index]['amount'] = float(request.form['amount'])
            expenses[index]['category'] = request.form['category']
            expenses[index]['date'] = request.form['date']
        save_expenses(expenses)
        return redirect(url_for('summary'))

    return render_template('modify.html', expenses=expenses)

# Plot route
@app.route('/plot')
def plot():
    expenses = load_expenses()
    categories = {}
    for exp in expenses:
        category = exp['category']
        categories[category] = categories.get(category, 0) + exp['amount']
    
    plt.bar(categories.keys(), categories.values())
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Spending')
    plt.savefig('static/plot.png')  # Save plot as an image
    plt.close()
    return render_template('plot.html')

if __name__ == '__main__':
    app.run(debug=True)
