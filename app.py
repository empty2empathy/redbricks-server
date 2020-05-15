from redbricksapp.entry import create_app
from redbricksapp.config import ENV

if ENV == 'production':
    config_object = object
else:
    config_object = object

app = create_app(
    config_object=config_object,
    serve_api=True
)
