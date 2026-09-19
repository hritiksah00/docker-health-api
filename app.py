from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return {
        "service": "docker-health-api",
        "message": "My first container project"
    }


@app.get("/health")
def health():
    return {"status": "ok"}, 200