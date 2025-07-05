from datetime import datetime
from functools import singledispatchmethod
import os
import shutil

from application import dto
from application import interactors
from application import Templater
from application.types import FilePlaylistType


class Uploader:

    def __init__(
            self,
            templater: Templater,
            create_file: interactors.CreateFile,
    ):
        self.templater = templater
        self.create_file = create_file

    def write(self, file_path: str, file_id: str, data: list[dto.Station]) -> None:
        content = self.templater("m3u", data=data)

        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, file_id + ".m3u"), "w", encoding="utf-8") as file_data:
            file_data.write(content)

    def create_file_data(self, user_id: int, file_path: str, filename: str) -> dto.NewFile:
        file_id = "".join(str(datetime.utcnow().timestamp()).split("."))
        _, ext = os.path.splitext(filename)
        file_type = FilePlaylistType(ext[1:])

        new_file = dto.NewFile(
            user_id=user_id,
            file_id=file_id,
            file_path=file_path,
            filename=filename,
            fileext=file_type.value,
        )

        return new_file

    @singledispatchmethod
    def load(self, data: dto.UploadStation | dto.UploadStations | dto.UploadPlaylist) -> dto.NewFile:
        raise NotImplementedError("Cannot load station data")

    @load.register
    def _(self, data: dto.UploadStation) -> dto.NewFile:
        new_file = self.create_file_data(data.user_id, data.file_path, f"user{data.user_id}_1station.m3u")
        self.write(data.file_path, new_file.file_id, [data.station])
        return new_file

    @load.register
    def _(self, data: dto.UploadStations) -> dto.NewFile:
        new_file = self.create_file_data(
            data.user_id,
            data.file_path,
            f"user{data.user_id}_{len(data.stations)}stations.m3u",
        )
        self.write(data.file_path, new_file.file_id, data.stations)
        return new_file

    @load.register
    def _(self, data: dto.UploadPlaylist) -> dto.NewFile:
        if data.file.filename is None:
            raise ValueError("file has not filename")

        new_file = self.create_file_data(data.user_id, data.file_path, data.file.filename)

        os.makedirs(data.file_path, exist_ok=True)
        with open(new_file.file_path_with_id, "wb") as buffer:
            shutil.copyfileobj(data.file.file, buffer)

        return new_file

    async def process(self, data: dto.NewFile) -> None:
        await self.create_file(data)
