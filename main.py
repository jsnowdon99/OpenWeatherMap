import requests
from flask import Flask, request, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}
    def post(self):
        return {"data":"HEYYYY"}

cities = []


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/city", methods=["POST"])
def search_city():
    API_KEY = "f6cd3294ce738e77794c48003b4cd6aa"
    city = request.form["cityname"]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'

    response = requests.get(url).json()
    clear = False


    if request.method == "POST":
        if "delete" in request.form and cities:
            cities.clear()
            clear = True
            return render_template("city.html", clear = clear)
            
    if response.get("cod") != 200:
        error = True
        if cities:
            return render_template("city.html", cities=cities, error = error)
        return render_template("city.html", error = error)
        # return "Please enter a valid city"
    else:
        
        print(response.get("weather"[0], {}).get("description"))
        temp = response.get("main", {}).get("temp")
        far = temp * (9/5) - 459.67
        humidity = response.get("main", {}).get("humidity")
        description = (response["weather"][0]["description"])
        description = description.capitalize()
        country = response.get("sys", {}).get("country")
        print(description)

        if [city.capitalize(), int(far), humidity, description, country] not in cities and len(cities) < 8:
            cities.append([city.capitalize(), int(far), humidity, description, country])
            print(len(cities))
            no_repeat = str("Add a new city below...")
            
            print(cities)
            return render_template("city.html", cities = cities, no_repeat = no_repeat)
        if [city.capitalize(), int(far), humidity, description, country] in cities:
            repeat = str("Please enter a new city")
            return render_template("city.html", cities = cities, repeat = repeat)
        # repeat = False
        

        if len(cities) >= 6:
            repeat = str("You can not add more than 6 cities for comparison")
            return render_template("city.html", cities = cities, repeat = repeat)
        
        # return render_template("city.html", country = country, 
        # city = city.capitalize(), temp = int(far), humidity = humidity, description = description.capitalize())

api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
    app.run(debug=True)

