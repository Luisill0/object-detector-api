import os
import requests
from alive_progress import alive_it

def download(url: str, dest: str) -> None:
    if not os.path.exists(dest):
        os.makedirs(dest)

    filename = url.split('/')[-1]
    filepath = os.path.join(dest, filename)

    req = requests.get(url, stream=True)
    if req.ok:
        with open(filepath, 'wb') as file:
            chunks = req.iter_content(chunk_size=1024 * 8)
            for chunk in alive_it(chunks, total=31460):
                if chunk:
                    file.write(chunk)
                    file.flush()
                    os.fsync(file.fileno())
        file.close()

if __name__ == '__main__':
    download('https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4.weights', '/app/api/models')