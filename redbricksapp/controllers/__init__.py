from . import artist
from . import event
from . import location

BLUEPRINTS = [artist.artist, event.event, location.location]


def RegisterBlurprint(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
    return app
