# # model = SentenceTransformer("intfloat/e5-large-v2")
# # text = "query: ¿Cómo funciona el aprendizaje profundo?"
# # embedding = model.encode(text)


# from sentence_transformers import SentenceTransformer
# import chromadb

# # Cargar el modelo de embeddings
# model = SentenceTransformer("intfloat/e5-large-v2")

# # Inicializar ChromaDB (base de datos vectorial)
# client = chromadb.PersistentClient(path="./chroma_db")  # Guarda los datos en disco
# collection = client.get_or_create_collection(name="chat_history")

# # Función para guardar un mensaje en la base de datos
# def store_message(message, message_id):
#     embedding = model.encode("passage: " + message).tolist()  # E5 usa "passage: " para documentos
#     collection.add(
#         ids=[message_id],  # ID único
#         embeddings=[embedding],
#         metadatas=[{"text": message}]
#     )
#     print(f"✅ Guardado en la DB: {message}")

# # Función para recuperar contexto relevante
# def retrieve_context(query, top_k=3):
#     query_embedding = model.encode("query: " + query).tolist()  # E5 usa "query: " para consultas
#     results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    
#     # Extraer textos relevantes
#     context = [res["text"] for res in results["metadatas"][0]]
#     return context

# # Simulación de conversación con contexto
# def chat_with_memory(user_input):
#     # Recuperar contexto relevante
#     context = retrieve_context(user_input)

#     # Construir mensaje con contexto
#     full_prompt = f"Contexto relevante:\n{context}\n\nUsuario: {user_input}\nBot:"
    
#     # Aquí puedes integrar un LLM (ej. GPT) para generar respuestas
#     print("🔍 Contexto recuperado:", context)
#     print("\n🤖 Respuesta del LLM:", "[Aquí iría la respuesta generada]")

# # Ejemplo de uso
# store_message("La inteligencia artificial permite automatizar tareas complejas.", "msg_1")
# store_message("Existen diferentes tipos de redes neuronales, como CNN y RNN.", "msg_2")

# chat_with_memory("¿Qué tipos de redes neuronales existen?")

# # from sentence_transformers import SentenceTransformer

# # model = SentenceTransformer("intfloat/e5-large-v2")



from sentence_transformers import SentenceTransformer
import chromadb

# Cargar el modelo de embeddings
model = SentenceTransformer("intfloat/e5-large-v2")

# Inicializar ChromaDB (base de datos vectorial)
client = chromadb.PersistentClient(path="./chroma_db")  # Guarda los datos en disco
collection = client.get_or_create_collection(name="chat_history")

# Función para guardar un mensaje en la base de datos
def store_message_emotions(user_name, message):
    embedding = model.encode("passage: " + message).tolist()  # E5 usa "passage: " para documentos
    collection.add(
        # ids=[message_id],  # ID único
        embeddings=[embedding],
        metadatas=[{"text": message, "user_name": user_name}]
    )
    print(f"Guardado en la DB: {message} (Usuario: {user_name})")

# Función para recuperar contexto relevante de un usuario específico
def retrieve_context(query, user_name, top_k=5):
    query_embedding = model.encode("query: " + query).tolist()  # E5 usa "query: " para consultas
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    
    # Filtrar los resultados para que solo muestren los mensajes del usuario actual
    context = []
    for res, meta in zip(results["metadatas"][0], results["texts"][0]):
        if meta["user_name"] == user_name:
            context.append(res["text"])

    return context

# Simulación de conversación con contexto
def chat_with_memory(user_input, user_name):
    # Recuperar contexto relevante para el usuario
    context = retrieve_context(user_input, user_name)

    # Construir mensaje con contexto
    full_prompt = f"Contexto relevante:\n{context}\n\nUsuario: {user_input}\nBot:"
    
    # Aquí puedes integrar un LLM (ej. GPT) para generar respuestas
    print("Contexto recuperado:", context)
    print("\nRespuesta del LLM:", "[Aquí iría la respuesta generada]")

# Ejemplo de uso
store_message_emotions("La inteligencia artificial permite automatizar tareas complejas.", "msg_1", "usuario_1")
store_message_emotions("Existen diferentes tipos de redes neuronales, como CNN y RNN.", "msg_2", "usuario_1")
store_message_emotions("Las redes neuronales convolucionales son muy eficaces para el procesamiento de imágenes.", "msg_3", "usuario_2")

# Simulamos una consulta para el usuario_1
chat_with_memory("¿Qué tipos de redes neuronales existen?", "usuario_1")

# Simulamos una consulta para el usuario_2
chat_with_memory("¿Qué es una red neuronal convolucional?", "usuario_2")
