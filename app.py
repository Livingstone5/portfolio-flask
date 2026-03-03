from flask import session,redirect,url_for
import sqlite3
from flask import Flask, render_template, request

app= Flask(__name__)
app.secret_key="supersecretkey"

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/contact",methods=["POST"])
def contact():
    name=request.form.get("name")
    email=request.form.get("email")
    message=request.form.get("message")

    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO contacts (name,email,message) VALUES (?,?,?)",(name,email,message))
    conn.commit()
    conn.close()

    
    return "Message received successfully."


def init_db():
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT)""")
    conn.commit()
    conn.close()

init_db()


@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("login"))

  

    conn=sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    messages=cursor.fetchall()
    conn.close()

    print("MESSAGES :",messages)

    return render_template("admin.html",messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin",None)
    return redirect(url_for("login"))



@app.route("/delete/<int:id>")
def delete(id):

    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)