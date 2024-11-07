# app.py (Hauptprogramm)
from flask import Flask
from main import main_bp

app = Flask(__name__)
app.config["APP_NAME"] = "Simulation Risikomatrix-Klassifikation"
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
