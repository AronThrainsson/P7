import random

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    number = random.randint(1, 10)
    return render_template("index.html", number=number)

@app.route("/expert")
def expert():
    return render_template("expert.html")

@app.route("/common")
def common():
    return render_template("common.html")

@app.route("/toxins")
def toxins():
    return render_template("toxins.html")

#search function
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the search query from the URL
    if query:
        # Replace with your search logic, e.g., database lookup or API call
        return f"Results for '{query}'"
    return "No query entered."

if __name__ == '__main__':
    app.run(debug=True)