from flask import Flask, request, jsonify
from pydantic import EmailStr, BaseModel, ValidationError
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL
        )
                     """)

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

init_db()

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        with get_db() as conn:
            data = conn.execute("""select * from users""").fetchall()
            users = []
            for user in data:
                users.append(User(**user).model_dump())
            return jsonify(users)
    if request.method == "POST":
        try:
            user = User(**request.get_json(silent=True) or {})
        except ValidationError as e:
            return jsonify({"error": "wrong user data"}), 400

        with get_db() as conn:
            conn.execute("""
            insert into users (name, age, email) values (?, ?, ?)
            """, (
                user.name,
                user.age,
                user.email
            )
            )

            conn.commit()
            return jsonify({"message": "User created"}), 201

if __name__ == "__main__":
    app.run(debug=True)
