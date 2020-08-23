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
        col2 = db.votecomments
        results = []
        # maxid = 0
        # id = 0
        # for x in col.find():
        #     id = int(x["id"])
        #     maxid +=1
        # id = str(maxid+id)
        inc = 0

        for x in col.find():
            if x["id"] != request_json["claimid"]:
                continue
            if request_json["vote"] == "yes":
                inc = 1
            if request_json["vote"] == "no":
                inc = -1    
            
            vote = int(x["votes"])
            vote += inc
            col.update_one({"id":request_json["claimid"]},{"$set":{"votes":str(vote)}})

            
            # before = x["img"]
            # ovalue =  x["value"]
            # odescription = x["description"]
            break
        

        payload = {}
        # {"claimid":"112","vote":"yes",comments:"none"}
        # payload["id"] = id
        
        if "userid" in request_json:
            payload["userid"] = request_json['userid']
        else:
            payload["userid"] = "123"
        
        payload["claimid"] = request_json['claimid']
        
        payload["comments"] = str(request_json['comments'])
        payload["vote"] = str(request_json['vote'])
        # payload["after"] = request_json['after']
        # payload["originalvalue"] = ovalue
        # payload["before"] = before
        # payload["originaldescription"] = odescription
        # payload["votes"] = 0
        

        # payload['status'] = "open"
        
        result=col2.insert_one(payload)

        retjson = {}

        # retjson['dish'] = userid
        retjson['result'] = "successfully voted"
        retjson['claimid'] = request_json["claimid"]

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


