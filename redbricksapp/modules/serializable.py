from typing import Any


class SerializableMixin:
    __EXCEPT_KEY__ = tuple()

    def serialize(self) -> dict:
        items = {k: v for k, v in self if k not in self.__EXCEPT_KEY__}
        return items

    def serialize_with(self, *args, **kwargs) -> Any:
        # custom implementation
        return self.serialize()

    def __iter__(self) -> Any:
        raise NotImplementedError
