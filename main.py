from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about airline reviews. Use the provided reviews to answer the question as accurately as possible.

Here are some relevant reviews: 
{reviews}

Here is the question to answer: {question}

IMPORTANT: Base your answer ONLY on the reviews provided above. If no reviews are provided, say "No reviews were found."
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (Press 'q' to quit): ")
    print("\n\n")
    if question.lower() == "q":
        break
    
    # Retrieve documents
    docs = retriever.invoke(question)
    
    # Debug: print number of documents retrieved
    #print(f"DEBUG: Retrieved {len(docs)} documents")
    
    if len(docs) == 0:
        print("ERROR: No documents retrieved from vector store!")
        continue
    
    # Debug: print first document
    #print(f"DEBUG: First document preview: {docs[0].page_content[:200]}...")
    
    # Extract the text content from documents
    reviews_text = "\n\n---\n\n".join([
        f"{doc.page_content}\nMetadata: Airline={doc.metadata.get('airline_name')}, "
        f"Rating={doc.metadata.get('overall_rating')}, Recommended={doc.metadata.get('recommended')}"
        for doc in docs
    ])
    
    #print(f"DEBUG: Reviews text length: {len(reviews_text)}")
    
    result = chain.invoke({"reviews": reviews_text, "question": question})
    print(result)
