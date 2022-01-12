from flask import Flask, render_template

STATIC_DIR = './static/'

app = Flask(__name__, static_folder=STATIC_DIR)


@app.route('/')
def root():
    return render_template('reader.html')


if __name__ == '__main__':
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    app.run(debug=True)
