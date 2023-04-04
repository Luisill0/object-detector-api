import os
import cv2
import numpy as np
from typing import Any, List

from api.types import DetectionResult, Prediction

workdir = os.path.dirname(os.path.abspath(__file__))
modelDir = workdir + '/models'

class YOLOSSD:
    """
        YOLO SSD Implementation using Darknet and OpenCV
    """

    detectionModel: Any
    classes: List[str]

    def __init__(self) -> None:
        net = cv2.dnn.readNetFromDarknet(f'{modelDir}/yolov4.cfg', f'{modelDir}/yolov4.weights')

        self.detectionModel = cv2.dnn_DetectionModel(net)
        self.detectionModel.setInputParams(
            scale=1/255, size=(416,416), swapRB=True
        )

        with open(f'{modelDir}/coco.names', 'r') as cocoNamesFile:
            self.classes = cocoNamesFile.read().splitlines()
        cocoNamesFile.close()

    def predict(self, image: np.ndarray) -> List[Prediction]:
        detection = DetectionResult(
            self.detectionModel.detect(
            image, confThreshold=0.6, nmsThreshold=0.4
        ))

        predictions: List[Prediction] = []
        for(classIndex, score, box) in zip(detection.indexes, detection.scores, detection.boxes):
            predictions.append(
                Prediction(
                    classID=classIndex,
                    className=self.classes[classIndex],
                    score=score,
                    box=box
                )
            )

        return predictions