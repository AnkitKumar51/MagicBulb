from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def command_history():
    conn = sqlite3.connect("commands.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM light_commands ORDER BY timestamp DESC")
    commands = cursor.fetchall()
    conn.close()
    return render_template("command_history.html", commands=commands)

if __name__ == "__main__":
    app.run(debug=True)
