from app.core.services.bucket_service import BucketService
from app.core.interfaces.chunking import ChunkingStrategy
from app.core.interfaces.embbeding import EmbeddingStrategy
from app.infrastructure.repositories.milvus_repo import BaseRepo
from app.infrastructure.db.vector_schema import MilvulsSchema
from app.infrastructure.configs import settings


from minio.datatypes import Object
from typing import Iterator, cast
import numpy as np

class PopulateVectors:
        
        def __init__(self, bucket: BucketService, chunk: ChunkingStrategy, embbeding: EmbeddingStrategy, repo: BaseRepo):
             self._bucketService = bucket
             self._chunkingService = chunk
             self._embbedingService = embbeding
             self._repo = repo

        def exec(self):

            files = cast(Iterator[Object], self._bucketService.list_objects("silver", None))

            for file_meta in files:

                file = self._bucketService.get_object(file_meta.object_name, "silver")

                content = file.read().decode('utf-8')
                lines = content.splitlines(keepends=True)

                chunks = self._chunkingService.chunk_it("/n".join(lines))
                embbeds = self._embbedingService.embbed_it(chunks)

                items = self.__to_schema(chunks, embbeds)

                self._repo.insert(settings.collection_name, items)


        def __to_schema(self, chunks: list[str], embbeds: np.ndarray[np._AnyShapeT, np.dtype[any]]) -> list[MilvulsSchema]:
             return cast(list[MilvulsSchema],[dict(text=text, text_vector=embbeds[ind]) for ind, text in enumerate(chunks)])


populate = PopulateVectors()

populate.exec()
