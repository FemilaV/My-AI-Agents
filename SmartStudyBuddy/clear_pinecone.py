from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "study-buddy-langchain"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if INDEX_NAME in existing_indexes:
    print(f"Found index: {INDEX_NAME}")
    print("Deleting all vectors...")
    index = pc.Index(INDEX_NAME)
    index.delete(delete_all=True)
    print("✓ All vectors deleted!")
else:
    print(f"Index '{INDEX_NAME}' doesn't exist yet. Nothing to clear.")
    print("It will be created when you run your main script.")