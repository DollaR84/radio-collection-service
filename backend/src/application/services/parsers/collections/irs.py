from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Union

from bs4 import BeautifulSoup, Tag

from application.dto import CollectionData

from .base import BaseCollection


@dataclass(slots=True)
class ItemData:
    name: str
    path: str
    type: str


class UrlType(Enum):
    DIRECTORY = "directory"
    FILE = "file"


class InternetRadioStreamsCollection(BaseCollection):
    order_id: int = 2

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

        self.base_directory_url: str = "https://github.com/mikepierce/internet-radio-streams/tree"
        self.base_file_url: str = "https://raw.githubusercontent.com/mikepierce/internet-radio-streams"

    def make_url(self, **kwargs: Any) -> str:
        url_type: Union[UrlType, str] = kwargs.get("url_type", UrlType.DIRECTORY)
        element_url: str = kwargs.get("element_url", "")
        return self.__make_url__(url_type, element_url)

    def __make_url__(self, url_type: Union[UrlType, str] = UrlType.DIRECTORY, element_url: str = "") -> str:
        if isinstance(url_type, UrlType):
            url_type = url_type.value
        return "/".join([getattr(self, f"base_{url_type}_url"), "main", element_url])

    async def load(self, url: str) -> list[ItemData]:
        results: list[ItemData] = []
        search_data: list[Tag] = []
        content = await self.parser.get_content(url)

        bs = BeautifulSoup(content, "html.parser")
        search1 = bs.find_all("script", {"type": "application/json", "data-target": "react-partial.embeddedData"})
        if search1:
            search_data.extend(search1)
        search2 = bs.find_all("script", {"type": "application/json", "data-target": "react-app.embeddedData"})
        if search2:
            search_data.extend(search2)

        for repository in search_data:
            if not repository:
                continue
            data = json.loads(repository.text)

            props = data.get("props")
            if props:
                payload = props.get("initialPayload")
            else:
                payload = data.get("payload")
            if not payload:
                continue

            tree = payload.get("tree")
            if not tree:
                continue

            items = tree.get("items", [])
            for item in items:
                name = item.get("name")
                if not name or name in (".github", "README.md",):
                    continue
                name = name.replace(".m3u", "")

                results.append(ItemData(
                    name=name,
                    path=item.get("path"),
                    type=item.get("contentType"),
                ))

        return results

    async def process_data(self, url: str) -> list[CollectionData]:
        results = []
        data = await self.load(url)

        for item in data:
            if item.type == UrlType.FILE.value:
                results.extend(await self.read(item))
            elif item.type == UrlType.DIRECTORY.value:
                results.extend(await self.process_data(self.make_url(url_type=item.type, element_url=item.path)))

        return results

    async def read(self, item: ItemData) -> list[CollectionData]:
        results = []
        item.name = item.name.strip().replace("-", " ").replace("_", " ")
        data = await self.parser.get_content(self.make_url(url_type=item.type, element_url=item.path))

        for line in data.splitlines():
            line = line.strip()
            line_start = line[:4]

            if line_start.lower().startswith("http"):
                results.append(CollectionData(name=item.name, url=line))

        return results
