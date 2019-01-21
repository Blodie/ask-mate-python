from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route('/')
def route_index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )