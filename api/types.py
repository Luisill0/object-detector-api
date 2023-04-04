from typing import List, Tuple, TypedDict

class BoundingBox:
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def __init__(self, xmin:int, ymin:int, xmax:int, ymax:int) -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    @classmethod
    def fromYOLOTuple(cls, box: Tuple[int,int,int,int]):
        return cls(box[0], box[1], box[0] + box[2], box[1] + box[3])


class DetectionResult:
    """
    Result of sending an image to the neural network
    ---
    index: index of class (see coco.names for the full list)
    score: confidence score
    box: bounding box using (xmin,ymin),(xmax,ymax) coordinates
    """
    indexes: List[int]
    scores: List[float]
    boxes: List[BoundingBox]

    def __init__(self, result: Tuple[List[int], List[float], List[Tuple[int,int,int,int]]]) -> None:
        self.indexes = result[0]
        self.scores = result[1]
        self.boxes = [BoundingBox.fromYOLOTuple(box) for box in result[2]]

class Prediction(TypedDict):
    className: str
    box: BoundingBox
    score: float
    classID: int