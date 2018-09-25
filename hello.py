from flask import Flask, render_template
import cf_deployment_tracker
import os
import json

# Sterujemy instalacją 
cf_deployment_tracker.track()

app = Flask(__name__)


# W IBM Cloud, bierzemy numer portu ze zmiennych środowiskowych PORT
# lokalnie ustawiamy 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
