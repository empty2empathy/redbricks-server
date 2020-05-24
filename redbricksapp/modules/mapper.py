from typing import Callable, Any
from ..models import Event, Location


def event_mapper(
    load_artist: bool = False, load_location: bool = False
) -> Callable[[Any], dict]:
    def bind_method(obj: Event) -> dict:
        if hasattr(obj, "_asdict"):
            obj = obj.Event

        item_map = obj.serialize()
        if load_artist:
            item_map["artists"] = list(v.serialize() for v in obj.artists)
        if load_location:
            item_map["location"] = obj.location.serialize()
        return item_map

    return bind_method


def location_mapper(load_event: bool = False) -> Callable[[Any], dict]:
    def bind_method(obj: Location) -> dict:
        if hasattr(obj, "_asdict"):
            obj = obj.Location

        item_map = obj.serialize()
        if load_event:
            item_map["events"] = list(v.serialize() for v in obj.events)
        return item_map

    return bind_method


__all__ = [event_mapper, location_mapper]
