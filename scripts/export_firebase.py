import os
import sys
import firebase_admin

from json import JSONEncoder
from firebase_admin import firestore, credentials
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.firestore import DocumentReference

cred_path = os.environ.get('GOOGLE_CLOUD_CREDENTIAL')
args = {'databaseURL': os.environ.get('FIREBASE_URL')}

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, args)
db = firestore.client()


class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DatetimeWithNanoseconds):
            return obj.rfc3339()
        elif isinstance(obj, DocumentReference):
            return obj.id
        return JSONEncoder.default(self, obj)


def export():
    data = dict()
    collections = {item.id: item.get() for item in db.collections()}
    for k, v in collections.items():
        data.setdefault(k, dict())
        for item in v:
            data[k].setdefault(item.id, item.to_dict())
    return data


if __name__ == '__main__':
    encoder = JsonEncoder(ensure_ascii=False)
    with open(sys.argv[1], 'w', encoding='utf8') as f:
        print(f.write(encoder.encode(export())))
