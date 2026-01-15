import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

df = pd.read_csv("airline_reviews.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
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
        
vector_store = Chroma(
    collection_name="airline_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)