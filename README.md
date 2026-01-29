# Dev Assessment - Webhook Receiver
## Notes:
1.The UI is populated via backend APIs rather than directly querying MongoDB from the frontend.

2. The UI can be accessed at: /webhooks/ui

3. For demo purposes, I have not implemented deduplication to ensure that events appear only once in the feed.

As a proposed solution, this can be handled by filtering events with timestamp > (current_time - 15 seconds) or by enforcing idempotency at the database level.

4. Please configure the MongoDB connection URL in app/sample.ini as specified below before running the application.

```
[TEST]
DB_URI = mongodb+srv://<db_user>:<password>@cluster0.quxaezo.mongodb.net/github?appName=Cluster0
```

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************