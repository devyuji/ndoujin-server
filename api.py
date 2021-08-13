from flask import Flask, request
from app import nhentai
from flask_cors import CORS
from decouple import config

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": config('CORS_ORIGIN')}})

@app.route('/', methods=['GET'])
def home():
    return {"goto" : "https://ndoujin.netlify.app"}

@app.route('/api', methods=['POST'])
def main():
    try:
        id = request.get_json(silent=True)['id']
        res = nhentai(id)
        if res["error"]:
            return {"message" : "Something went wrong!"},404
        return res

    except Exception as err:
        print('error = ', err)
        return {},500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port= 5001)