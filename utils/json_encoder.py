from enum import Enum
from datetime import datetime
from dataclasses import is_dataclass, asdict
from json import JSONEncoder
from peewee import Model
from playhouse.shortcuts import model_to_dict


class DataclassJSONEncoder(JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        elif isinstance(o, Model):
            return model_to_dict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Enum):
            return str(o)
        return super().default(o)
