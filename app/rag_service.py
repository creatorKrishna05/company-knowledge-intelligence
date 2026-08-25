class RAGService:


    def __init__(
        self,
        retriever,
        context_builder,
        answer_generator,
    ):

        self.retriever = retriever
        self.context_builder = context_builder
        self.answer_generator = answer_generator


    def answer(self, query: str, top_k: int, filters=None) -> str:

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        
        chunks = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
        )

        if not chunks:
            return "I couldn't find relevant information in the knowledge base." 
            

        context = self.context_builder.build(chunks)

        return self.answer_generator.generate(
            query=query,
            context=context,
        )


