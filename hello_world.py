
'''
data: 2019.07.05
name: Lee Eunsoo
'''

from flask import Flask

app = Flask(__name__)


@app.route('/')
def run():
    return 'hello world'


if __name__ == "__main__":
    app.run()


