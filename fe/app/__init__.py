from flask import Flask
from app.routes import routes
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
