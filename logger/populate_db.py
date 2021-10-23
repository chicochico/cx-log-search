import json

from logger.app import create_app
from logger.extensions import db
from logger.models.logs import Log

app = create_app()
app.app_context().push()

print("recreating DB tables")
db.drop_all()
db.create_all()

print("adding dummy data")

data = json.loads(open("logger/data.json").read())

for d in data:
    db.session.add(Log(**d))

db.session.commit()
