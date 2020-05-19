from simplejson import JSONEncoder as BaseJSONEncoder
from .serializable import SerializableMixin


class JSONEncoder(BaseJSONEncoder):
    __CUSTOM_OBJECT__ = (SerializableMixin, )

    def default(self, o):
        if isinstance(o, SerializableMixin):
            return o.serialize()
        else:
            super(JSONEncoder, self).default(o)
