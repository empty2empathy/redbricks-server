from sqlalchemy.orm import selectinload

from .base import Blueprint, Session, request
from ..models import Location, RelArtistEvent, Artist, Event
from ..modules.mapper import location_mapper
from ..modules.pagination import Pagination


location = Blueprint("location", __name__)


@location.route("/api/v1/location/<int:location_id>")
def _route_get_location(location_id: int):
    with Session() as session:
        item: Location = session.query(Location).get_or_404(location_id)
        events = (
            session.query(Event).filter(Event.location_id == item.location_id).all()
        )

        related_artists = (
            session.query(RelArtistEvent.artist_id)
            .join(Artist, RelArtistEvent.artist_id == Artist.artist_id)
            .filter(RelArtistEvent.event_id.in_(list(v.event_id for v in events)))
            .subquery()
        )

        artists = (
            session.query(Artist).filter(Artist.artist_id.in_(related_artists)).all()
        )
        item_map = item.to_dict(mapper=location_mapper)
        item_map["artists"] = list(v.serialize() for v in artists)
        item_map["events"] = list(v.serialize() for v in events)
        return item_map


@location.route("/api/v1/location")
def _route_list_location():
    with Session() as session:
        page = request.args.get("page", default=1, type=int)
        page_unit = request.args.get("pageUnit", default=5, type=int)

        events: Pagination = (
            session.query(Location)
            .options(selectinload(Location.events))
            .paginate(page=page, page_unit=page_unit)
        )

        return events.to_dict(mapper=location_mapper(load_event=True))
