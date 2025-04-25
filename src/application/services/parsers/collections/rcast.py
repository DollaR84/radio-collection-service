import logging
from typing import Any

from bs4 import BeautifulSoup, Tag

from application.dto import CollectionData

from .base import BaseCollection


class Mp3RadioStationsCollection(BaseCollection):
    order_id: int = 3

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

        self.base_url: str = "https://www.rcast.net/dir/mp3"

        self.current_page: int = 1
        self.last_page: int | None = None

    def make_url(self, **kwargs: Any) -> str:
        return self.__make_url__(kwargs.get("page_number", 1))

    def __make_url__(self, page_number: int = 1) -> str:
        return "/".join([self.base_url, f"page{page_number}"])

    async def load(self, url: str) -> list[CollectionData]:
        results: list[CollectionData] = []
        content = await self.parser.get_content(url)

        bs = BeautifulSoup(content, "html.parser")
        table = bs.find("table")
        if not isinstance(table, Tag):
            return results

        for row in table.find_all("tr"):
            item = None
            for column in row.find_all("td"):
                title = column.find("h4")
                if not title and not item:
                    continue

                if title:
                    name = title.find("a").text
                    url = column.find("small").find("a").text

                    if all([name, url]):
                        item = CollectionData(name=name.strip(), url=url)
                    continue

                if item is None:
                    continue

                params = column.find("p")
                if params:
                    rows = params.text.split("\n")
                    item.add_info(rows[0], rows[2])

                results.append(item)

        if not self.last_page:
            is_disabled = False
            pagination = bs.find("ul", {"class": "pagination"})
            if not isinstance(pagination, Tag):
                return results

            for line in pagination.find_all("li"):
                if "disabled" in line.get("class", []):
                    is_disabled = True
                elif not is_disabled:
                    continue
                else:
                    self.last_page = int(line.find("a").text)
                    break

        return results

    async def process_data(self, url: str) -> list[CollectionData]:
        results = []
        try:
            results.extend(await self.load(url))

            self.current_page += 1
            if self.last_page and self.current_page <= self.last_page:
                results.extend(await self.process_data(self.make_url(page_number=self.current_page)))
        except Exception as error:
            logging.error(error, exc_info=True)

        return results
