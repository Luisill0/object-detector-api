import cv2
import base64
import numpy as np
from typing import List

from api.types import Prediction
from api.color import Color

def decodeB64Image(b64_image: str) -> np.ndarray:
    image_string = b64_image.split(',')[1] if b64_image[0]=='d' else b64_image
    bytes_data = base64.b64decode(image_string)
    bytes_array = np.frombuffer(bytes_data, dtype=np.uint8)
    cv_image = cv2.imdecode(bytes_array, cv2.IMREAD_COLOR)

    return cv_image

def encodeImageB64(image: np.ndarray) -> str:
    encoded_image = cv2.imencode('.jpg', image)
    b64_string = base64.b64encode(encoded_image[1]).decode('utf-8')
    return b64_string
    
def annotateImage(image: np.ndarray, predictions: List[Prediction]) -> np.ndarray:
    colors = [Color.randomColor() for _ in range(0, 81)]

    for prediction in predictions:
        box = prediction['box']
        score = prediction['score']
        className = prediction['className']
        index = prediction['classID']

        color = colors[index].asTuple()

        cv2.rectangle(
            image, color=color, thickness=3,
            pt1=(box.xmin, box.ymin), pt2=(box.xmax, box.ymax)
        )
        cv2.putText(
            image, f'{className}: {score:.3}',
            (box.xmin, box.ymin - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            color=color, thickness=2
        )

    return image    