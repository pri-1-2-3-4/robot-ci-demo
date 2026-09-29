"""A tiny simulated speed-supervision function, similar in spirit to ATP overspeed protection.

Status rules (limit in km/h):
    speed <= limit          -> NORMAL
    limit < speed <= limit+5 -> WARNING
    speed > limit + 5       -> BRAKE
"""
from robot.api import logger
from robot.api.deco import keyword, library


@library(scope="TEST")
class SpeedSupervision:
    WARNING_MARGIN = 5

    def __init__(self):
        self.limit = None
        self.speed = 0.0

    @keyword("Set Speed Limit")
    def set_speed_limit(self, limit_kmph: float):
        self.limit = limit_kmph
        logger.info(f"Speed limit set to {limit_kmph} km/h")

    @keyword("Set Train Speed")
    def set_train_speed(self, speed_kmph: float):
        self.speed = speed_kmph
        logger.info(f"Train speed set to {speed_kmph} km/h")

    @keyword("Supervision Status Should Be")
    def supervision_status_should_be(self, expected: str):
        actual = self._status()
        if actual != expected.upper():
            raise AssertionError(
                f"Expected {expected.upper()} but got {actual} "
                f"(speed {self.speed}, limit {self.limit})"
            )
        logger.info(f"Status is {actual} as expected")

    def _status(self) -> str:
        if self.limit is None:
            raise AssertionError("Speed limit has not been set")
        if self.speed <= self.limit:
            return "NORMAL"
        if self.speed <= self.limit + self.WARNING_MARGIN:
            return "WARNING"
        return "BRAKE"
