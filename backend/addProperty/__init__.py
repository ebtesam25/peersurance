import logging

import azure.functions as func
from pymongo import MongoClient
from pymongo.collection import ObjectId
import bcrypt
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def initdb():

    client = MongoClient("mongodb+srv://user:password3142@cluster0.dyrpk.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")

    db = client.get_database("peersurance")

    return client, db



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    
    client, db = initdb()
    
    if req.get_json():


        request_json = req.get_json()
        col = db.properties
        results = []
        maxid = 0
        id = 0
        for x in col.find():
            id = int(x["id"])
            maxid +=1
        id = str(maxid+id)

        payload = {}
        # {"phone":"123456","name":"Zoey","description":"Can't afford medication", "email":"someone@someone.com"}
        payload["id"] = id
        if "userid" in request_json:
            payload["userid"] = request_json['userid']
        else:
            payload["userid"] = "123"
        payload["description"] = request_json['description']
        payload["value"] = request_json['value']
        payload["img"] = request_json['img']

        # payload['status'] = "open"
        
        result=col.insert_one(payload)

        retjson = {}

        # retjson['dish'] = userid
        retjson['result'] = "successfully added"
        retjson['id'] = id

        ret = json.dumps(retjson)

        return  func.HttpResponse(
             ret,
             mimetype="application/json",
             status_code=200
        )


    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

