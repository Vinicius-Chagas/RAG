from src.bucket.bucket_service import BucketService
from src.extractor.extractor_factory import ExtractorFactory
from minio.datatypes import Object
from typing import Iterator, cast
import os

def extract_text():
    service = BucketService()

    files = cast(Iterator[Object], service.list_objects("bronze", None))

    for file_meta in files:
        print(file_meta)
        name, extension = os.path.splitext(file_meta.object_name)
        extractor = ExtractorFactory().getExtractor(str(extension).removeprefix("."))

        print(extractor)

        if extractor == None: continue

        file = service.get_object(file_meta.object_name)

        txt = extractor.extract(file)

        print(f"extracted txt size {len(txt)}")
        extractor.save_as_txt(txt, file_meta.object_name)

    print("extracted with success")



extract_text()