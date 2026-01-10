
from mains import process_all_pdfs
# ========== SETUP (Run once) ==========
print("SETTING UP STUDY BUDDY WITH CONTEXTUAL RETRIEVAL")

# Process all PDFs with contextual enhancement (Skip if already indexed)
pdf_directory = "./study_materials"
try:
    index_stats = pc.Index(INDEX_NAME).describe_index_stats()
    total_vectors = index_stats.get('total_vector_count', 0)
    print(f"DEBUG: Index '{INDEX_NAME}' contains {total_vectors} vectors.")
except Exception as e:
    print(f"DEBUG: Could not get index stats: {e}")
    total_vectors = 0

if total_vectors > 0:
    print("\nSkipping indexing because vectors already exist.")
    total_chunks = total_vectors
else:
    vectorstore, total_chunks = process_all_pdfs(pdf_directory)

print(f"\nSuccessfully processed {total_chunks} contextualized chunks!")

# Wait for index to be searchable (longer sleep for serverless index propagation)
print("\nWaiting for vectors to be searchable...")
time.sleep(20)