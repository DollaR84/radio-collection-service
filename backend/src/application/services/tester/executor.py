import asyncio
from contextlib import suppress
import time
from types import TracebackType
from typing import Optional, Self, Type

import vlc

from .data import RadioTestData


class RadioTestExecutor:

    def __init__(self, data: RadioTestData, repeat_count: int, repeat_timeout: int):
        self.data = data
        self.repeat_count = repeat_count
        self.repeat_timeout = repeat_timeout

        self.instance = vlc.Instance("--no-video", "--input-repeat=-1")
        self.player = self.instance.media_player_new()

    def __enter__(self) -> Self:
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        self._release_resources()

    def run(self) -> None:
        self.player.set_media(self.instance.media_new(self.data.url))
        self.player.audio_set_mute(True)
        self.player.play()

        for _ in range(self.repeat_count):
            state = self.player.get_state()
            self.data.is_success = state == vlc.State.Playing
            if self.data.is_success:
                break
            time.sleep(self.repeat_timeout)

        asyncio.run_coroutine_threadsafe(
            self.data.callback_after(self.data),
            loop=asyncio.get_event_loop()
        )

    def _release_resources(self) -> None:
        with suppress(Exception):
            self.player.stop()
            self.player.release()

        with suppress(Exception):
            self.instance.release()
