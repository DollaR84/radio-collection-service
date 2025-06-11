from .base import BaseFFMpegChecker


class FFProbeChecker(BaseFFMpegChecker):

    def __call__(self) -> bool:
        command = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "format=duration",
            "-of", "default=nokey=1:noprint_wrappers=1",
            "-timeout", str(self.timeout),
            self.url,
        ]

        return self.run(command)
