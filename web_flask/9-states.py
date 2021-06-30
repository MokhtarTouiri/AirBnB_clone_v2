#!/usr/bin/python3
"""
flask framework
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
storage.all()


@app.teardown_appcontext
def teardown_data(self):
    """
       teardown data
    """
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_id(id=None):
    """
        states by id
    """
    info = []
    states = storage.all(State)
    if id is None:
        for k in states:
            info.append(states[k])
    else:
        id = 'State.' + id
        info = states.get(id)
    return render_template('9-states.html', states=info, id=id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
