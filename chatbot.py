from groq import Groq
import re
from embeddings import retrieve_context, retrieve_embedding, store_message_emotions
from classify import get_emotion, get_model_big5, registry_big5
from relational_db import read_all_records
recent_chat = []

# Función para cargar el chatbot
def load_chatbot():
    client = Groq(api_key="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")
    return lambda messages: client.chat.completions.create(
        model="deepseek-r1-distill-qwen-32b",
        messages=messages
    ).choices[0].message.content

# Función para inicializar el chatbot
def initialize_chatbot():
    chat = [{"role": "system", "content": "Eres un asistente llamado KeleaCare Assistant que contesta de forma empática según las emociones de la gente, las cuales se añadirán al final de cada consulta junto con un nivel de confianza para cada una. Las emociones no forman parte de la consulta, solo son una guía para ayudarte a responder de forma adecuada."}]
    return chat


# Función para formatear el mensaje y obtener el contexto
def format_message(user, text, classifier):
    global recent_chat
    interactions = retrieve_context(user, text)  # Lista de diccionarios con 'message', 'emotions', 'timestamp'
    context = "Contexto de mensajes anteriores:\n"
    context += "\n".join(interactions)

    context += "\n\nÚltimos mensajes del chat:\n"
    for recent in recent_chat:
        context += f"\n\n{recent['role']}: {recent['content']}"


    emotions = get_emotion(classifier, text)
    emotions_text = ", ".join([f"{emotion} (confianza: {score:.2f})" for emotion, score in emotions.items()])
    message = f"{text} Emociones detectadas: {emotions_text}"
    msg_with_context = context + f"Mensaje actual, al que debes contestar teniendo en cuenta el contexto:\n{message}"
    store_message_emotions(user, message)
    return msg_with_context

# Función principal para el chatbot con emociones
def chatbot(user, pipe, text, classifier):
    global recent_chat
    chat = initialize_chatbot()

    message = format_message(user, text, classifier)
    chat.append({"role": "user", "content": message})

    response = pipe(chat)
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    recent_chat.append({"role": "user", "content": text})
    recent_chat.append({"role": "bot", "content": response})
    while len(recent_chat) > 6:
        recent_chat.pop(0)
    return response


def analise_big5(username_value):
    pipe = load_chatbot()
    model, tokenizer, device = get_model_big5()
    
    # Obtener todos los registros y embeddings del usuario
    records = read_all_records(username_value)
    # texts = []
    # embeddings = []
    
    # for date, record in records:
    texts, embeddings = retrieve_embedding(username_value)
    # texts.append(text)
    # embeddings.append(embedding)
    
    return registry_big5(embeddings, texts, records, pipe, model, tokenizer, device)
