from flask import Flask, render_template
from flask_collect import Collect

app = Flask(__name__)

# static file collection
collect = Collect(app)

import canvas_resource.logging


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/greet')
def greeting():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)