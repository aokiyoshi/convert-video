# pylint: disable=missing-module-docstring
from pydantic import BaseModel

# pylint: disable=missing-class-docstring
class Params(BaseModel): # pylint: disable=too-few-public-methods
    input_path: str
    output_path: str
    width: int
    height: int
    fps: int
    gpu: bool

class VideoInfo(BaseModel): # pylint: disable=too-few-public-methods
    width: int
    height: int
    fps: int
    duration: int
