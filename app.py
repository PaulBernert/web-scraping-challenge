from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__, template_folder='LocalSite')

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsApp"
mongo = PyMongo(app)

@app.route("/")
def flaskIndex():
    data=mongo.db.collection.find_one()
    return render_template("index.html", data=data)

@app.route("/scrape")
def flaskScrape():
    data = mongo.db.collection
    marsData = scrape_mars.scrape()
    data.update({}, marsData, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
