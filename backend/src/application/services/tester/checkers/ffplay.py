from .base import BaseFFMpegChecker


class FFPlayChecker(BaseFFMpegChecker):

    def __call__(self) -> bool:
        command = [
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-v", "error", "-i",
            self.url,
        ]

        return self.run(command)
