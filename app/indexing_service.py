class IndexingService:

    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def index(self, chunks):
        texts = [chunk.content for chunk in chunks]

        embeddings = self.embedder.embed_batch(texts)

        if len(embeddings) != len(chunks):
            raise ValueError("Number of embeddings must match number of chunks")

        for chunk, embedding in zip(chunks, embeddings):
            self.vector_store.add(chunk, embedding)
