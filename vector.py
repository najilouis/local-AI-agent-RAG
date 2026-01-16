import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Read CSV
df = pd.read_csv("airline_reviews_light.csv")
#print(f"Loaded {len(df)} rows from CSV")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_location = "./chrome_langchain_db"

# Initialize vector store
vector_store = Chroma(
    collection_name="airline_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Check if we need to add documents
doc_count = vector_store._collection.count()
#print(f"Vector store currently has {doc_count} documents")

if doc_count == 0:
    #print("Adding documents to vector store...")
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        document = Document(
            page_content=(
                f"Review Title: {row['Review_Title']}\n"
                f"Review: {row['Review']}"
            ),
            metadata={
                "airline_name": row["Airline_Name"],
                "overall_rating": row["Overall_Rating"],
                "recommended": row["Recommended"] == "yes",
                "verified": row["Verified"] == "yes",
                "review_date": row["Review_Date"],
                "date_flown": row["Date_Flown"],
                "route": row["Route"],
                "aircraft": row["Aircraft"],
                "seat_type": row["Seat_Type"],
                "traveller_type": row["Type_Of_Traveller"],
                "value_for_money": row["Value_For_Money"]
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
    
    #print(f"Created {len(documents)} documents")
    #print("Adding documents to vector store (this may take a few minutes)...")
    vector_store.add_documents(documents=documents, ids=ids)
    #print("Documents added successfully!")
#else:
    #print("Vector store already populated, skipping document addition")
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

#print("Retriever initialized successfully!")
