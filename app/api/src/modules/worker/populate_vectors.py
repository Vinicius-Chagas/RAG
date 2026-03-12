from src.modules.bucket.bucket_service import BucketService
from src.modules.chunking.chunking_service import ChunkingService
from src.modules.embbeding.embbeding_service import EmbbedingService
from src.db.repository.base_repo import BaseRepo
from src.db.schema import MilvulsSchema
from src.consts.collection import collection_name

from minio.datatypes import Object
from typing import Iterator, cast
import numpy as np

class PopulateVectors():
        bucketService = BucketService()
        chunkingService = ChunkingService()
        embbedingService = EmbbedingService()
        repo = BaseRepo()

        def exec(self):

            files = cast(Iterator[Object], self.bucketService.list_objects("silver", None))

            for file_meta in files:
                print(file_meta)

                file = self.bucketService.get_object(file_meta.object_name)
                
                with open(file=file) as text:

                    chunks = self.chunkingService.chunk_it(text.readlines())
                    embbeds = self.embbedingService.embbed_it(chunks)

                    items = self.__to_schema(chunks, embbeds)

                    self.repo.insert(collection_name, items)


        def __to_schema(chunks: list[str], embbeds: np.ndarray[np._AnyShapeT, np.dtype[any]]) -> list[MilvulsSchema]:
             return cast(list[MilvulsSchema],[dict(text=text, text_vector=embbeds[ind]) for ind, text in chunks])


populate = PopulateVectors()

populate.exec()
