from functions import search, driver
from flask_restful import Api, Resource
from flask import Flask, jsonify, request

# __________________ Start API ___________________
app = Flask(__name__)
api = Api(app)

@app.route("/", methods=["POST"])

class Data(Resource):
    def post(self):
        creteria = request.get_json()

        user = creteria["user"]
        search_term = creteria["search_term"]
        until = creteria["until"]
        since = creteria["since"]
        count = creteria["count"]

        data = search(user, search_term, until, since, count)

        return jsonify({
            "data":data
        })

api.add_resource(Data, "/get_data/")

if __name__ == "__main__":
    app.run(debug=True)
    driver.quit()