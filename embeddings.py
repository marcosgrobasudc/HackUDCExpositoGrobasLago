from sentence_transformers import SentenceTransformer
import chromadb
import uuid

model = SentenceTransformer("intfloat/e5-large-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="chat_history")

def store_message_emotions(user_name, message):
    """
    Almacena un mensaje en la base de datos con su embedding

    Args:
    user_name: nombre del usuario
    message: mensaje a almacenar

    Returns:
    None
    """
    embedding = model.encode("passage: " + message).tolist()  # E5 usa "passage: " para documentos
    message_id = str(uuid.uuid4())
    collection.add(
        ids=[message_id],  # ID único
        embeddings=[embedding],
        metadatas=[{"text": message, "user_name": user_name}]
    )
    print(f"Guardado en la DB: {message} (Usuario: {user_name})")

def retrieve_context(user_name, query, top_k=5):
    """
    Recupera el contexto de un usuario a partir de una consulta

    Args:
    user_name: nombre del usuario
    query: consulta para recuperar el contexto
    top_k: cantidad de resultados a recuperar

    Returns:
    context: contexto recuperado
    """
    query_embedding = model.encode("query: " + query).tolist()  # E5 usa "query: " para consultas
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k, where={"user_name": user_name}, include=['embeddings', 'metadatas'])
   
    # Verificar si hay resultados antes de acceder a los datos
    if not results or "metadatas" not in results or results["metadatas"][0] == []:
        return ["No hay contexto disponible aún."]
 
    context = results["metadatas"][0][0]['text']
   
    return context if context else ["No se encontró contexto relevante."]


def retrieve_embedding(user_name):
    """
    Recupera los mensajes y embeddings de un usuario
    
    Args:
    user_name: nombre del usuario

    Returns:
    messages: lista de mensajes
    embeddings: lista de embeddings
    """
    results = collection.get(
        where={"user_name": user_name},  # Filtrar por el usuario
        include=["embeddings", "metadatas"]  # Obtener embeddings y metadatos
    )
 
    # Extraer los textos y embeddings
    messages = [item["text"] for item in results["metadatas"]]
    embeddings = results["embeddings"]
    return messages, embeddings