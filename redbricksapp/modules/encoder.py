from datetime import datetime
from simplejson import JSONEncoder as BaseJSONEncoder
from .serializable import SerializableMixin
from .pagination import Pagination


class JSONEncoder(BaseJSONEncoder):
    __CUSTOM_OBJECT__ = (SerializableMixin, Pagination)

    def default(self, o):
        if isinstance(o, SerializableMixin):
            return o.serialize()
        elif isinstance(o, Pagination):
            return o.to_json()
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            super(JSONEncoder, self).default(o)
