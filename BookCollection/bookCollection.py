from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bookcollectiondatabase"
)

cursor = db.cursor()

app = Flask(__name__)

@app.route("/")
def home():
    cursor.execute("SELECT id, title, author, genre, year FROM books")
    bookInfo = cursor.fetchall()
    return render_template("home.html", bookInfo = bookInfo)

@app.route("/addBook", methods=["GET", "POST"])
def addBookFunction():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        year = request.form.get("year")

        if all([title, author, genre, year]):
            sql = "INSERT INTO books (title, author, genre, year) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (title, author, genre, year))
            db.commit()
        return redirect(url_for("home"))

    cursor.execute("SELECT id, title, author, genre, year FROM books")
    bookInfo = cursor.fetchall()
    return render_template("addBook.html", bookInfo = bookInfo)

@app.route("/updateBook/<int:id>", methods=["GET", "POST"])
def updateBookFunction(id):
    if request.method == "POST":
        newTitle = request.form.get("title")
        newAuthor = request.form.get("author")
        newGenre = request.form.get("genre")
        newYear = request.form.get("year")
        sql = "UPDATE books SET title=%s, author=%s, genre=%s, year=%s WHERE id=%s"
        cursor.execute(sql, (newTitle, newAuthor, newGenre, newYear, id))
        db.commit()
        return redirect(url_for("home"))

    sql = "SELECT id, title, author, genre, year FROM books where id=%s"
    cursor.execute(sql, (id,))
    entry = cursor.fetchone()
    return render_template("updateBook.html", entry = entry)

@app.route("/delete/<int:id>")
def deleteBookFunction(id):
    sql = "DELETE FROM books WHERE id=%s"
    cursor.execute(sql, (id,))
    db.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug = True)