import json
import numpy as np
from app.db.connection import get_connection
from app.embeddings.hf import get_embedding
from app.embeddings.similarity import cosine_similarity

def get_relevant_chunks(document_id: int, question: str, top_k: int, min_similarity: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM documents WHERE id = %s", (document_id,))
    doc = cursor.fetchone()
    if not doc:
        conn.close()
        return []

    document_name = doc["name"] if isinstance(doc, dict) else doc[0]

    cursor.execute(
        "SELECT id, chunk_index, text, embedding FROM chunks WHERE document_id = %s",
        (document_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    query_embedding = get_embedding(question)

    scored = []
    for row in rows:
        rowid = row["id"] if isinstance(row, dict) else row[0]
        idx = row["chunk_index"] if isinstance(row, dict) else row[1]
        text = row["text"] if isinstance(row, dict) else row[2]
        blob = row["embedding"] if isinstance(row, dict) else row[3]

        embedding = np.array(json.loads(blob), dtype=float)
        sim = cosine_similarity(query_embedding, embedding)

        if sim >= min_similarity:
            scored.append({
                "chunk_id": rowid,
                "text": text,
                "similarity": sim,
                "document": document_name
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
