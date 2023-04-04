import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from api.yolo import YOLOSSD
from api.image_utils import annotateImage, decodeB64Image, encodeImageB64

class APIRequest(BaseModel):
    image: str

class APIResponse(BaseModel):
    image: str

prefix = os.getenv('CLUSTER_ROUTE_PREFIX', '').rstrip('/')

app = FastAPI(
    title='Object Detection API',
    version='1.0',
    description='Upload base64 encoded image, returns base64 encoded image with annotations',
    openapi_prefix=prefix
)

objectDetector = YOLOSSD()

@app.post('/upload/detect')
async def detect(request: APIRequest) -> APIResponse:
    if not request.image:
        raise HTTPException(400, 'Image not received')

    if not isinstance(request.image, str): 
        raise HTTPException(422, 'Invalid image type')

    try:
        cvImage = decodeB64Image(request.image)
    except:
        raise HTTPException(422, 'Invalid image, is the image correctly encoded?')

    predictions = objectDetector.predict(cvImage)
    annotatedImage = annotateImage(cvImage, predictions)
    encodedAnnotatedImage = encodeImageB64(annotatedImage)
    base64ImagePrefix = 'data:image/jpeg;base64,'
    return APIResponse(image=base64ImagePrefix+encodedAnnotatedImage)