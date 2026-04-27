from flask import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/properties')
def estate():
    return render_template('properties.html')

@app.route('/invest')
def investment():
    return render_template('investment.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)