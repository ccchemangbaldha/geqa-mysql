import json
from app.db.connection import get_connection

def save_document_with_chunks(filename: str, chunk_records: list):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO documents (name) VALUES (%s)",
            (filename,)
        )
        document_id = cursor.lastrowid

        for record in chunk_records:
            cursor.execute(
                """
                INSERT INTO chunks (document_id, chunk_index, text, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    document_id,
                    record["chunk_id"],
                    record["chunk_text"],
                    json.dumps(record["embedding"])
                )
            )

        conn.commit()
        return document_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
