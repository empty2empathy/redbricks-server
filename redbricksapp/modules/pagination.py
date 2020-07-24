from typing import Any, Iterator, Optional, Callable, Mapping, Generator, Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import QueryKlass


def serialize(obj):
    if isinstance(obj, (str, int, float, bool)):
        return obj
    elif isinstance(obj, (Sequence, Iterator, Generator)):
        return list(serialize(v) for v in obj)
    elif isinstance(obj, Mapping):
        return {k: serialize(v) for k, v in obj.items()}
    elif hasattr(obj, "__iter__") and hasattr(obj, "keys"):
        return dict(obj)
    elif hasattr(obj, "serialize"):
        return obj.serialize()
    else:
        raise ValueError(f"Cannot encode datatype {type(obj)}")


class Pagination:
    def __init__(self, query: "QueryKlass", page: int = 1, page_unit: int = 20) -> None:
        self.query: "QueryKlass" = query
        self.page: int = page
        self.page_unit: int = max(min(page_unit, 40), 1)
        self.total: int = query.count()
        self._items = None

    @property
    def pages(self) -> int:
        if self.page_unit == 0 or self.total == 0:
            return 0
        else:
            return (self.total // self.page_unit) + int(self.total % self.page_unit > 0)

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    def prev(self) -> "Pagination":
        if self.has_prev:
            prev_page = min(self.page - 1, 1)
            page_unit = max(min(self.page_unit, 40), 1)
            return self.query.paginate(prev_page, page_unit)
        else:
            raise ValueError("Prev page is not exists.")

    def next(self) -> "Pagination":
        return self.query.paginate(self.page + 1, self.page_unit)

    @property
    def items(self) -> Any:
        if not self._items:
            self._items = (
                self.query.offset((self.page - 1) * self.page_unit)
                .limit(self.page_unit)
                .all()
            )
        return self._items

    def __iter__(self) -> Iterator:
        for item in self.items:
            yield item

    def __repr__(self) -> str:
        return f"<{type(self).__name__}> [query={repr(self.query)}, page={self.page}, page_unit={self.page_unit}, total={self.total}]"

    def __call__(self, mapper: Optional[Callable[[Any], Any]] = None) -> dict:
        return self.to_dict(mapper=mapper)

    def to_dict(self, mapper: Optional[Callable[[Any], Any]] = None) -> dict:
        if mapper:
            items = list(map(lambda v: v.to_dict(mapper=mapper), self.items))
        else:
            items = list(map(lambda v: serialize(v), self.items))

        return dict(
            items=items,
            page=self.page,
            pages=self.pages,
            hasNext=self.has_next,
            hasPrev=self.has_prev,
        )
