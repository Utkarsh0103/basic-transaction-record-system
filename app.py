from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
data = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions = data)

# Create operation
@app.route("/add", methods = ["GET", "POST"])
def add_transaction():
    if (request.method == "GET"):
        return render_template("form.html")
    if (request.method == "POST"):
        transation = {
              'id': len(data)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
             }
        data.append(transation)
        return redirect(url_for("get_transactions"))

# Update operation
@app.route("/edit/<int:transaction_id>", methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        # Extract the updated values from the form fields
        date = request.form["date"]
        amount = request.form["amount"]

        # Find the transaction with the matching ID and update its values
        for transact in data:
            if transact['id'] == transaction_id:
                transact['date'] = date
                transact['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transact in data:
        if transact['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction = transact)
    
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove from list
    for transact in data:
        if transact['id'] == transaction_id:
            data.remove(transact)
            break

     # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)