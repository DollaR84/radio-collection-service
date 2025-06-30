from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type

from application.dto import CollectionData

from utils.text import paschal_case_to_words

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
        return paschal_case_to_words(_name)

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

    def __init__(self, name: str, **kwargs: Any):
        self.name = name
        parser = kwargs.get("parser")
        if not isinstance(parser, BaseParser):
            raise ValueError(f"parser can't be '{type(parser)}'")
        self.parser: BaseParser = parser

        if self.parser is None:
            raise RuntimeError("for parse collections need set parser")

    async def parse(self) -> list[list[CollectionData]]:
        full_data = await self.process_data(self.make_url())
        return self.parser.get_batch_data(full_data)

    @abstractmethod
    def make_url(self, **kwargs: Any) -> str:
        raise NotImplementedError

    @abstractmethod
    async def process_data(self, url: str) -> list[CollectionData]:
        raise NotImplementedError

    @abstractmethod
    async def load(self, url: str) -> list:
        raise NotImplementedError
