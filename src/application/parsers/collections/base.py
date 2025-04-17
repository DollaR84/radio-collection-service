from __future__ import annotations

from abc import ABC, abstractmethod
import re
from typing import Any, Type

from application.dto import CollectionData

from ..base import BaseParser


class BaseCollection(ABC):
    _collections: dict[str, Type[BaseCollection]] = {}
    order_id: int

    def __init_subclass__(cls, **kwargs: Any) -> None:
        name = cls.get_name()
        if name not in cls._collections:
            cls._collections[name] = cls

    @classmethod
    def get_name(cls) -> str:
        _name = cls.__name__.replace("Collection", "")
        return " ".join(list(re.findall(r"[A-Z][a-z0-9]+", _name)))

    @classmethod
    def get_collection(cls, name: str, **kwargs: Any) -> BaseCollection:
        collection_cls = cls._collections.get(name)
        if collection_cls is None:
            raise ValueError(f"collection '{name}' does not exist")

        return collection_cls(name, **kwargs)

    @classmethod
    def get_collections_names(cls) -> list[str]:
        data = dict(sorted(cls._collections.items(), key=lambda item: item[1].order_id))
        return list(data.keys())

    def __init__(self, name: str, parser: BaseParser, **kwargs: Any):
        super().__init__(**kwargs)
        self.name = name
        self.parser: BaseParser = parser

    async def parse(self) -> list[CollectionData]:
        return await self.process_data(self.make_url())

    @abstractmethod
    def make_url(self, **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    async def process_data(self, url: str) -> list[CollectionData]:
        raise NotImplementedError

    @abstractmethod
    async def load(self, url: str) -> list:
        raise NotImplementedError
