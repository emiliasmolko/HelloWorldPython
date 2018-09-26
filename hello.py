from flask import Flask, render_template
import cf_deployment_tracker
import os
import json

# deployment tracking
cf_deployment_tracker.track()

app = Flask(__name__)


# for IBM Cloud port is taken from os.getenv()
# for local installation 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
