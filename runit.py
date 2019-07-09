
from flask import Flask , render_template

app=Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/state/<button>')
def state(button):
    return render_template('state.html', btn_state=button)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)