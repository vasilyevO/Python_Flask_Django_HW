from flask import Flask

app = Flask(__name__)

@app.route("/")
def index() -> str:
    """Возвращает приветствие на корневом маршруте."""
    return "Hello, Flask!"

@app.route("/user/<name>")
def user(name: str) -> str:
    """
    Возвращает персональное приветствие с именем.

    Args:
        name: имя пользователя из URL.
    """
    return f"Hallo, {name.upper()}!"

if __name__ == "__main__":
    app.run(debug=True)