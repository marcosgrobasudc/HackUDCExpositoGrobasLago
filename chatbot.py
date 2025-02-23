from groq import Groq
import re
from embeddings import retrieve_context, retrieve_embedding, store_message_emotions
from classify import get_emotion, get_model_big5, registry_big5
from relational_db import read_all_records

recent_chat = []

def load_chatbot():
    """
    Carga el chatbot

    Returns:
    function: función que recibe una lista de mensajes y devuelve la respuesta del chatbot
    """
    client = Groq(api_key=None) # Poner api_key de Groq
    return lambda messages: client.chat.completions.create(
        model="deepseek-r1-distill-qwen-32b",
        messages=messages
    ).choices[0].message.content

def initialize_chatbot():
    """
    Inicializa el chatbot para que sepa que rol debe tomar en la conversación

    Returns:
    list: lista de diccionarios con el rol y contenido del mensaje
    """
    chat = [{"role": "system", "content": "Eres un asistente llamado KeleaCare Assistant que contesta de forma empática según las emociones de la gente, las cuales se añadirán al final de cada consulta junto con un nivel de confianza para cada una. Las emociones no forman parte de la consulta, solo son una guía para ayudarte a responder de forma adecuada."}]
    return chat

def format_message(user, text, classifier):
    """
    Formatea el mensaje del usuario para que el chatbot tenga contexto sobre la comversación y las emociones del usuario

    Args:
    user (str): nombre del usuario
    text (str): mensaje del usuario
    classifier: modelo de clasificación de emociones

    Returns:
    str: mensaje formateado con el contexto y las emociones detectadas
    """
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

def chatbot(user, pipe, text, classifier):
    """
    Llama al chatbot para obtener una respuesta

    Args:
    user (str): nombre del usuario
    pipe (function): función que recibe una lista de mensajes y devuelve la respuesta del chatbot
    text (str): mensaje del usuario
    classifier: modelo de clasificación de emociones

    Returns:
    str: respuesta
    """
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
    """
    Recoge los datos necesarios de las bases de datos y llama a la función de registro de personalidad

    Args:
    username_value (str): nombre del usuario

    Returns:
    str: registro de personalidad
    """
    pipe = load_chatbot()
    model, tokenizer, device = get_model_big5()
    
    records = read_all_records(username_value)

    texts, embeddings = retrieve_embedding(username_value)
    return registry_big5(embeddings, texts, records, pipe, model, tokenizer, device)
