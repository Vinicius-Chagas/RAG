from app.core.services.bucket_service import BucketService
from app.core.services.chunking_service import ChunkingService
from app.core.services.embbeding_service import EmbbedingService
from app.infrastructure.clients.milvus_client import milvusClient
from app.infrastructure.repositories.base_repo import BaseRepo
from app.infrastructure.db.vector_schema import MilvulsSchema
from app.infrastructure.configs import settings

from minio.datatypes import Object
from typing import Iterator, cast
import numpy as np

class PopulateVectors():
        bucketService = BucketService()
        chunkingService = ChunkingService()
        embbedingService = EmbbedingService()
        repo = BaseRepo(milvusClient)

        def exec(self):

            files = cast(Iterator[Object], self.bucketService.list_objects("silver", None))

            for file_meta in files:

                file = self.bucketService.get_object(file_meta.object_name, "silver")

                content = file.read().decode('utf-8')
                lines = content.splitlines(keepends=True)

                chunks = self.chunkingService.chunk_it("/n".join(lines))
                embbeds = self.embbedingService.embbed_it(chunks)

                items = self.__to_schema(chunks, embbeds)

                self.repo.insert(settings.collection_name, items)


        def __to_schema(self, chunks: list[str], embbeds: np.ndarray[np._AnyShapeT, np.dtype[any]]) -> list[MilvulsSchema]:
             return cast(list[MilvulsSchema],[dict(text=text, text_vector=embbeds[ind]) for ind, text in enumerate(chunks)])


populate = PopulateVectors()

populate.exec()
