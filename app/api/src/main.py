from fastapi import FastAPI, UploadFile
from src.modules.bucket.bucket_service import BucketService
from src.modules.bucket.bucket_structure import BucketStructure
from src.dto.file import File
from io import BytesIO

app = FastAPI()
bucketService = BucketService()
bucketStructure = BucketStructure()

bucketStructure.build()

@app.get("/health")
def health():
    return { "ok": "ok" }

@app.post("/upload-file")
async def upload_file(file: UploadFile):
    file_obj = File(BytesIO(file.file.read()),file.filename, file.content_type)
    file.file.close()
    file_name = bucketService.add_object("bronze", file_obj)
    return { "status": "file created with success", "file_name" : file_name }

@app.delete("/remove-file")
async def remove_file(file_name: str):
    bucketService.remove_object("bronze", file_name)
    return { "status": "file removed with success" }

@app.put("/update-file")
async def update_file(file_name: str, file: UploadFile):
    bucketService.update_object("bronze", file_name, file.file, file.size)
    return { "status": "file updated with success" }