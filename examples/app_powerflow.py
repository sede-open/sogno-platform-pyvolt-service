import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template_string
from powerflow import get_powerflow_results

app = Flask(__name__)

@app.route('/')
def powerflow():
    powerflow_output, _, _ = get_powerflow_results()
    return render_template_string('''
        <h1>Power Flow Analysis</h1>
        <p>{{ powerflow_output|safe }}</p>
        <p><a href="/">Back to Home</a></p>
    ''', powerflow_output=powerflow_output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
