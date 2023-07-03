from flask import Flask, json
from router.attendance import route as create_record
from utils.json_encoder import DataclassJSONEncoder

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
json.provider.DefaultJSONProvider.sort_keys = False
app.json_encoder = DataclassJSONEncoder

app.register_blueprint(create_record, url_prefix="/api/v1")
