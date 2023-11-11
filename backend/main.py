import os
from pathlib import Path

import uvicorn
from appdirs import *
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from ultralytics import YOLO

app_path = Path(user_data_dir(appname='camera-ai', appauthor='', roaming=True))

app = FastAPI()

origins = [
    "http://192.168.0.104:8080",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def detect(file: UploadFile):
    try:
        contents = file.file.read()
        uploads_path = app_path / 'uploads' / file.filename
        with open(uploads_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    model = YOLO("best.pt")

    model.predict(
        source=uploads_path,
        save=True,
        project=app_path / 'done' / os.path.splitext(file.filename)[0],
    )


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    file_path = (app_path / 'done' / os.path.splitext(file.filename)[0] / 'predict' /
                 (os.path.splitext(file.filename)[0] + '.avi'))
    if os.path.isfile(file_path):
        os.remove(file_path)
        os.rmdir(app_path / 'done' / os.path.splitext(file.filename)[0] / 'predict')
        os.rmdir(app_path / 'done' / os.path.splitext(file.filename)[0])

    await detect(file)
    os.remove(app_path / 'uploads' / file.filename)
    return FileResponse(path=file_path,
                        filename=os.path.splitext(file.filename)[0] + '.avi',
                        media_type='multipart/form-data')


if __name__ == "__main__":
    print('app path: ' + str(app_path))
    # os.mkdir(app_path)
    os.makedirs(app_path / 'uploads', exist_ok=True)
    os.makedirs(app_path / 'done', exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
