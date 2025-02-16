import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template_string
from stateestimation import get_state_estimation_results

app = Flask(__name__)

@app.route('/')
def state_estimation():
    state_estimation_output = get_state_estimation_results()
    return render_template_string('''
        <h1>State Estimation</h1>
        <p>{{ state_estimation_output|safe }}</p>
        <p><a href="/">Back to Home</a></p>
    ''', state_estimation_output=state_estimation_output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
