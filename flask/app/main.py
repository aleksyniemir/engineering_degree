from flask import jsonify

from app import create_app

app = create_app()

@app.route("/", methods = ['GET'])
def hello_world():
    return jsonify({"Hello":"World!"})

if __name__ == "__main__":
    app.run()

