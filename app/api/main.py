from fastapi import FastAPI, UploadFile
from api.bucket.bucket_service import BucketService

app = FastAPI()
bucketService = BucketService()

@app.get("/health")
def health():
    return { "ok": "ok" }

@app.post("/upload-file")
async def upload_file(file: UploadFile):
    bucketService.append_object("bronze", file)
    return { "status": "file created with success" }

@app.delete("/remove-file")
async def remove_file(file_name: str):
    bucketService.remove_object("bronze", file_name)
    return { "status": "file removed with success" }

@app.put("/update-file")
async def update_file(file_name: str, file: UploadFile):
    bucketService.update_object("bronze", file_name, file.file, file.size)
    return { "status": "file updated with success" }