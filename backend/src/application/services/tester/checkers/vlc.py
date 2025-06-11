import vlc

from .base import BaseChecker


class VLCChecker(BaseChecker):

    def __init__(self, url: str, timeout: float):
        super().__init__(url, timeout)

        vlc_params = [
            "--no-video",
            "--no-audio",
            "--aout=dummy",
            "--codec=faad",
            "--audio-replay-gain-mode=disable",
            "--audio-filter=none",
            "--http-continuous",
            "--http-reconnect",
            "--http-user-agent='Mozilla/5.0'",
            "--quiet",
            "--demux=avformat",
            "--live-caching=2000",
            "--clock-jitter=0",
            "--clock-synchro=0",
            "--network-caching=5000",
            "--input-repeat=-1",
        ]

        self.instance = vlc.Instance(*vlc_params)
        self.player = self.instance.media_player_new()
        self.set_media()

    def set_media(self) -> None:
        media = self.instance.media_new(self.url)
        self.player.set_media(media)
        self.player.audio_set_mute(True)
        self.player.play()

    def close(self) -> None:
        self.player.stop()
        self.player.release()
        self.player = None

        self.instance.release()
        self.instance = None

    def __call__(self) -> bool:
        result = False
        state = self.player.get_state()

        try:
            if state == vlc.State.Error:
                self.player.stop()
                self.set_media()

            result = state in (vlc.State.Playing, vlc.State.Buffering)
        except Exception:
            result = False

        return result
