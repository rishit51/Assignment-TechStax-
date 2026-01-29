from flask import Blueprint, render_template, request
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')




@webhook.route('/receiver', methods=["POST"])
def receiver():
    #Deserializing JSON
    payload = request.get_json(force=True)
    #Event type provided in headers
    event = request.headers.get("X-GitHub-Event")
    events = mongo.db.events  
    doc = None

    # For push events 
    if event == "push":
        author = payload["pusher"]["name"]
        # Gives branch name
        to_branch = payload["ref"].split("/")[-1]
        # The current commit hash
        after = payload['after']
        doc = {
            "request_id":after,
            "action": "PUSH",
            "author": author,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

    #For pull requests events
    
    elif event == "pull_request":
        action = payload["action"]

        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        # Request id as pr_id
        pr_id = str(payload["pull_request"]["number"])
        # Merged requests are those which were closed and merged successfully
        if action == "closed" and payload["pull_request"]["merged"]:
            doc = {
                "request_id":pr_id,
                "action": "MERGE",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow()
            }
        #Requests that were just opened
        elif action == "opened":
            doc = {
                "request_id":pr_id,
                "action": "PULL_REQUEST",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow()
            }

    if doc:
        events.insert_one(doc)


    return {}, 200
#Lists out the most recent 20 events captured.
#Can apply timebased filter for handling non duplicate events in refresh window
@webhook.route('/events', methods=['GET'])
def get_events():
    events = mongo.db.events
    data = list(events.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    return data, 200

#Handles the UI
@webhook.route('/ui', methods=['GET'])
def ui():
    return render_template("index.html")

@webhook.route('/', methods=['GET'])
def ping():
    return {"message": "Everything is good"}, 200
