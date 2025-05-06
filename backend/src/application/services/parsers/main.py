from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any

from config import ParserConfig

from .base import BaseParser
from .collections import BaseCollection


class CollectionParser(BaseParser):

    def __init__(self, config: ParserConfig):
        super().__init__(config)
        self.collections = BaseCollection

        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        self._futures: list[Future] = []

    @property
    def collections_names(self) -> list[str]:
        return self.collections.get_collections_names()

    def get_collection(self, name: str, **kwargs: Any) -> BaseCollection:
        return self.collections.get_collection(name, **kwargs)

    def update(self) -> None:
        if self._futures:
            self._futures.clear()

        for name in self.collections_names:
            collection = self.get_collection(name, parser=self)
            self._futures.append(self._executor.submit(collection.parse))
