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
        col = db.claims
        # col2 = db.properties
        # results = []
        maxid = 0
        id = 0
        items = []
        
        for x in col.find():
            if x["userid"] != request_json["id"]:
                continue
            payload = {}
            payload["id"] = x["id"]
            id = x["userid"]
            payload["userid"] = x["userid"]
            # payload["pid"] = x['pid']
            payload["description"] = x['description']
            payload["claimvalue"] = x['claimvalue']
            payload["after"] = x['after']
            payload["originalvalue"] = x["originalvalue"]
            payload["before"] = x["before"]
            payload["originaldescription"] = x["originaldescription"]
            payload["votes"] = x["votes"]
            items.append(payload)
            
        retjson = {}

        # retjson['dish'] = userid
        retjson["items"] = items
        retjson['userid'] = id

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



