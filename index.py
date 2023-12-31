import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime,timezone, timedelta

import requests, json
from bs4 import BeautifulSoup

import openai
import os

db = firestore.client()
collection_ref = db.collection("Mcdonald")
docs = collection_ref.get()

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>楊子青Python網頁2023-12-11</h1>"
    return homepage

@app.route("/webhook5", methods=["POST"])
def webhook5():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    if (action == "Order"):
        order =  req["queryResult"]["parameters"]["Category"]
        info = "您選擇的分類是：" +order+ "\n"
        
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if order in dict["category"]:
                result += "餐點：" + dict["name"] + "\n"
                result += "價格：" + dict["price"] + "\n\n"
        info += result

    elif (action == "Meal"):
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "你選擇的是：" + keyword + "以下是他的資訊。\n"
        for doc in docs:
            dict = doc.to_dict()
            if keyword in dict["name"]:
                found = True 
                info += "餐點：" + dict["name"] + "\n"
                info += "價格：" + dict["price"] + "\n"
                info += "分類：" + dict["category"] + "\n"
                info += "ID：" + dict["id"] + " \n"
                info += "細項：" + dict["list"] + "\n\n" 
        if not found:
            info += "你要不要看看你在寫甚麼咚咚"
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run(debug=True)
