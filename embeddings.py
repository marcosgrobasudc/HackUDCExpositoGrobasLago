from sentence_transformers import SentenceTransformer
import chromadb
import uuid

# Cargar el modelo de embeddings
model = SentenceTransformer("intfloat/e5-large-v2")

# Inicializar ChromaDB (base de datos vectorial)
client = chromadb.PersistentClient(path="./chroma_db")  # Guarda los datos en disco
collection = client.get_or_create_collection(name="chat_history")

# Función para guardar un mensaje en la base de datos
def store_message_emotions(user_name, message):
    embedding = model.encode("passage: " + message).tolist()  # E5 usa "passage: " para documentos
    message_id = str(uuid.uuid4())
    collection.add(
        ids=[message_id],  # ID único
        embeddings=[embedding],
        metadatas=[{"text": message, "user_name": user_name}]
    )
    print(f"Guardado en la DB: {message} (Usuario: {user_name})")

# Función para recuperar contexto relevante de un usuario específico
def retrieve_context(user_name, query, top_k=5):
    query_embedding = model.encode("query: " + query).tolist()  # E5 usa "query: " para consultas
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k, where={"user_name": user_name}, include=['embeddings', 'metadatas'])
   
    # Verificar si hay resultados antes de acceder a los datos
    if not results or "metadatas" not in results or results["metadatas"][0] == []:
        return ["No hay contexto disponible aún."]
 
    context = results["metadatas"][0][0]['text']
   
    return context if context else ["No se encontró contexto relevante."]
