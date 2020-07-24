# https://github.com/cysnake4713/sqlalchemy-json/blob/master/sqlalchemy_json/track.py
import itertools

try:
    import simplejson as json
except ImportError:
    import json

from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.ext.mutable import Mutable


class TrackedObject(object):
    _type_mapping = {}

    def __init__(self, *args, **kwds):
        self.parent = None
        super(TrackedObject, self).__init__(*args, **kwds)

    def track_change(self):
        """Marks the object as changed.
        If a `parent` attribute is set, the `track_change()` method on the parent
        will be called, propagating the change notification up the chain.
        The message (if provided) will be debug logged.
        """
        if self.parent is not None:
            self.parent.track_change()
        elif hasattr(self, "changed"):
            self.changed()

    @classmethod
    def register(cls, origin_type):
        """Registers the class decorated with this method as a mutation tracker.
        The provided `origin_type` is mapped to the decorated class such that
        future calls to `convert()` will convert the object of `origin_type` to an
        instance of the decorated class.
        """

        def decorator(tracked_type):
            """Adds the decorated class to the `_type_mapping` dictionary."""
            cls._type_mapping[origin_type] = tracked_type
            return tracked_type

        return decorator

    @classmethod
    def convert(cls, obj, parent):
        """Converts objects to registered tracked types
        This checks the type of the given object against the registered tracked
        types. When a match is found, the given object will be converted to the
        tracked type, its parent set to the provided parent, and returned.
        If its type does not occur in the registered types mapping, the object
        is returned unchanged.
        """
        obj_type = type(obj)
        if obj_type in cls._type_mapping:
            replacement = cls._type_mapping[obj_type]
            new = replacement(obj)
            new.parent = parent
            return new
        return obj

    @classmethod
    def convert_iterable(cls, iterable, parent):
        """Returns a generator that performs `convert` on every of its members."""
        return (cls.convert(item, parent) for item in iterable)

    @classmethod
    def convert_items(cls, items, parent):
        """Returns a generator like `convert_iterable` for 2-tuple iterators."""
        return ((key, cls.convert(value, parent)) for key, value in items)

    @classmethod
    def convert_mapping(cls, mapping, parent):
        """Convenience method to track either a dict or a 2-tuple iterator."""
        if isinstance(mapping, dict):
            return cls.convert_items(mapping.items(), parent)
        return cls.convert_items(mapping, parent)


@TrackedObject.register(dict)
class TrackedDict(TrackedObject, dict):
    """A TrackedObject implementation of the basic dictionary."""

    def __init__(self, source=(), **kwds):
        super(TrackedDict, self).__init__(
            itertools.chain(
                self.convert_mapping(source, self), self.convert_mapping(kwds, self)
            )
        )

    def __setitem__(self, key, value):
        self.track_change()
        super(TrackedDict, self).__setitem__(key, self.convert(value, self))

    def __delitem__(self, key):
        self.track_change()
        super(TrackedDict, self).__delitem__(key)

    def clear(self):
        self.track_change()
        super(TrackedDict, self).clear()

    def pop(self, *key_and_default):
        self.track_change()
        return super(TrackedDict, self).pop(*key_and_default)

    def popitem(self):
        self.track_change()
        return super(TrackedDict, self).popitem()

    def update(self, source=(), **kwds):
        self.track_change()
        super(TrackedDict, self).update(
            itertools.chain(
                self.convert_mapping(source, self), self.convert_mapping(kwds, self)
            )
        )


@TrackedObject.register(list)
class TrackedList(TrackedObject, list):
    """A TrackedObject implementation of the basic list."""

    def __init__(self, iterable=()):
        super(TrackedList, self).__init__(self.convert_iterable(iterable, self))

    def __setitem__(self, key, value):
        self.track_change()
        super(TrackedList, self).__setitem__(key, self.convert(value, self))

    def __delitem__(self, key):
        self.track_change()
        super(TrackedList, self).__delitem__(key)

    def append(self, item):
        self.track_change()
        super(TrackedList, self).append(self.convert(item, self))

    def extend(self, iterable):
        self.track_change()
        super(TrackedList, self).extend(self.convert_iterable(iterable, self))

    def remove(self, value):
        self.track_change()
        return super(TrackedList, self).remove(value)

    def pop(self, index):
        self.track_change()
        return super(TrackedList, self).pop(index)

    def sort(self, cmp=None, key=None, reverse=False):
        self.track_change()
        super(TrackedList, self).sort(cmp=cmp, key=key, reverse=reverse)


class MutableDict(Mutable, TrackedDict):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super().coerce(key, value)


class MutableList(Mutable, TrackedList):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, list):
            return cls(value)
        return super().coerce(key, value)


class MutableStruct(Mutable):
    """SQLAlchemy `mutable` extension with nested change tracking."""

    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionary to NestedMutable."""
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return MutableDict.coerce(key, value)
        if isinstance(value, list):
            return MutableList.coerce(key, value)
        return super().coerce(key, value)


class JSONEncoded(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(
                value, separators=(",", ":"), ensure_ascii=False  # utf8mb4
            )
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


MutableStruct.associate_with(JSONEncoded)
