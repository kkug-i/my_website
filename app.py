from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("database.db")   
print("Opened database successfully")
conn.execute("CREATE TABLE IF NOT EXISTS Board(name TEXT, context TEXT)")  
print("TABLE Created Successfully")
name = [
    ["Elice", 15],
    ["Dodo", 16],
    ["checher", 17],
    ["Queen", 18]
]
for i in range(len(name)):
    conn.execute(f"INSERT INTO Board(name,context) VALUES('{name[i][0]}', '{name[i][1]}')")  # Board DB에 데이터 삽입
conn.commit()   
conn.close()    

# ================= 여기서부터는 다시 Flask 영역 ==========================

@app.route('/board')
def board():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Board")
    rows = cur.fetchall()

    print("DB: ")
    for i in range(len(rows)):
        print(rows[i][0] + ':' + rows[i][1])
    return render_template("board1.html", rows = rows)

@app.route('/')
def home():
    return render_template("main.html")


@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        name = request.form["name"] 
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Board WHERE name='{name}'")
        rows = cur.fetchall()
        print("DB : ")
        for i in range(len(rows)):
            print(rows[i][0] + ':' + rows[i][1])
        return render_template("search.html", rows=rows)
    else:
        return render_template("search.html")

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        try:
            name = request.form["name"]
            context = request.form["context"]

            
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Board(name,context) VALUES('{name}','{context}')")
                con.commit()
        except:
            con.rollback()  #
        finally:
            return redirect(url_for("board"))
    else:
        return render_template("add.html")


if __name__ == '__main__':
    app.run()