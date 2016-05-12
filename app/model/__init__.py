import json
from datetime import datetime

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    """
    Class which will use in order to enconde the ObjectId (Mongodb ID) and serialize to JSON
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

    def date_time(self, o):
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)