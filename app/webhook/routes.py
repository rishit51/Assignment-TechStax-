from flask import Blueprint, render_template, request
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')




@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.get_json(force=True)
    event = request.headers.get("X-GitHub-Event")
    events = mongo.db.events  
    doc = None

    if event == "push":
        author = payload["pusher"]["name"]
        to_branch = payload["ref"].split("/")[-1]
        after = payload['after']
        doc = {
            "request_id":after,
            "action": "PUSH",
            "author": author,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

    elif event == "pull_request":
        action = payload["action"]

        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        pr_id = str(payload["pull_request"]["number"])
        if action == "closed" and payload["pull_request"]["merged"]:
            doc = {
                "request_id":pr_id,
                "action": "MERGE",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow()
            }

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
        print("Saved:", doc)

    return {}, 200

@webhook.route('/events', methods=['GET'])
def get_events():
    events = mongo.db.events
    data = list(events.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    return data, 200
@webhook.route('/ui', methods=['GET'])
def ui():
    return render_template("index.html")

@webhook.route('/', methods=['GET'])
def ping():
    return {"message": "Everything is good"}, 200
