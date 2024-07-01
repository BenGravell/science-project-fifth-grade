from enum import IntEnum

from pydantic import BaseModel


class ChassisLength(IntEnum):
    SHORT = 1
    LONG = 2


class WheelSize(IntEnum):
    SMALL = 1
    LARGE = 2


class BodyStyle(IntEnum):
    BARE = 0
    CUBOID = 1
    TAPERED = 2
    TAPERED_REVERSE = 3


class TrialData(BaseModel):
    chassis_length: ChassisLength
    wheel_size: WheelSize
    body_style: BodyStyle
    average_time_to_finish_sec: float
