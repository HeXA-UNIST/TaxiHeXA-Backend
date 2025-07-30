from flask import Flask
from src.middleware import create_app
from src.resource import router
from src.middleware import admin
from config import config


app, socketio = create_app(config)

app.register_blueprint(router)

@app.route("/ping")
def ping():
    return "pong"

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 5000, debug=True)
