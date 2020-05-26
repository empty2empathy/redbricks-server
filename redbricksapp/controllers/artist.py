from humps import camelize

from .base import Blueprint, Session, request
from ..models import Artist
from ..modules.pagination import Pagination


artist = Blueprint("artist", __name__)


@artist.route("/api/v1/artist/<int:artist_id>")
def _route_get_artist(artist_id: int):
    with Session() as session:
        item: Artist = session.query(Artist).get_or_404(artist_id)
        return camelize(item.to_dict())


@artist.route("/api/v1/artist")
def _route_list_artist():
    with Session() as session:
        page = request.args.get("page", default=1, type=int)
        page_unit = request.args.get("pageUnit", default=5, type=int)

        artists: Pagination = session.query(Artist).paginate(
            page=page, page_unit=page_unit
        )
        return camelize(artists.to_dict())
