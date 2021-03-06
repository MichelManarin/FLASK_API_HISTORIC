import os
from flask import Flask, request, url_for, render_template, jsonify, json, abort
from flask_cors import CORS
import db_controls as dbc

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route("/historic", methods = ['GET'])
def get_historics():
    data = dbc.get_historic()
    return data

@app.route("/inserthistoric", methods = ['POST'])
def add_historics():
    days = request.json
    
    if (days == 0):
        abort(500)

    data = dbc.insert_historic(days)
    return jsonify(data)



@app.errorhandler(404)
def not_found_error(e):
    return "URL Not Found", 404

@app.errorhandler(500)
def not_found_error(e):
    return "Error", 500

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
