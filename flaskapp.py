from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return("This is the home page.")

@app.route("/tmp")
def tmp():
    return("This is a temporary page.")

if __name__ == '__main__':
    app.run(debug=True)
