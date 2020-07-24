from operator import itemgetter

from sqlalchemy import func
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
        return item.to_dict(mapper=event_mapper(load_artist=True, load_location=True))


@event.route("/api/v1/event")
def _route_list_event():
    with Session() as session:
        page = request.args.get("page", default=1, type=int)
        page_unit = request.args.get("pageUnit", default=5, type=int)

        query: Pagination = (
            session.query(
                func.date_format(Event.end_at, "%Y-%m-%d").label("event_date"), Event
            )
            .options(selectinload(Event.artists), selectinload(Event.location))
            .order_by(func.date_format(Event.end_at, "%Y-%m-%d").desc())
            .paginate(page=page, page_unit=page_unit)
        )

        events = query.to_dict()
        event_group = dict()
        for date, event in events["items"]:
            event_group.setdefault(date, list()).append(event)
        result = list(
            dict(dategroup=date, events=events) for date, events in event_group.items()
        )
        result = sorted(result, key=itemgetter("dategroup"), reverse=True)
        return result
