from flask import Flask, render_template, request, redirect
import search
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/answer", methods = ["GET", "POST"])
def answer():
    if request.form.has_key("query") and request.form["query"] != "":
        query = request.form["query"]
        answer = search.getAnswer(query)
        return render_template("answer.html", query = query, answer = answer)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
