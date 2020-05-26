from humps import camelize
from sqlalchemy.orm import selectinload

from .base import Blueprint, Session, request
from ..models import Event
from ..modules.mapper import event_mapper
from ..modules.pagination import Pagination


event = Blueprint("event", __name__)


@event.route("/api/v1/event/<int:event_id>")
def _route_get_event(event_id: int):
    with Session() as session:
        item: Event = (
            session.query(Event)
            .options(selectinload(Event.artists), selectinload(Event.location))
            .get_or_404(event_id)
        )
        return camelize(
            item.to_dict(mapper=event_mapper(load_artist=True, load_location=True))
        )


@event.route("/api/v1/event")
def _route_list_event():
    with Session() as session:
        page = request.args.get("page", default=1, type=int)
        page_unit = request.args.get("pageUnit", default=5, type=int)

        events: Pagination = (
            session.query(Event)
            .options(selectinload(Event.artists), selectinload(Event.location))
            .paginate(page=page, page_unit=page_unit)
        )

        return camelize(
            events.to_dict(mapper=event_mapper(load_artist=True, load_location=True))
        )
