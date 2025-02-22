from transformers import pipeline
from read_log import create_user, save_chat, read_chat
from groq import Groq
import re
from embeddings import retrieve_context, store_message_emotions


def load_classifier():
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    return classifier

def get_emotion(classifier, sentences):
    model_outputs = classifier(sentences)
    result = {}

    accumulated_score = 0.0

    for emotion in model_outputs[0]:
        accumulated_score += emotion['score']
        
        result[emotion['label']] = emotion['score']
        
        if accumulated_score >= 0.7:
            break
    return result # devuelve un diccionario con las emociones y su confianza


def load_chatbot():
    client = Groq(api_key="clave")
 
    # pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    return lambda messages: client.chat.completions.create(
        model="deepseek-r1-distill-qwen-32b",
        messages=messages      
    ).choices[0].message.content

def initialize_chatbot():
    chat = [{"role": "system", "content": "Eres un asistente que contesta de forma empática según las emociones de la gente, las cuales se añadirán al final de cada consulta junto con un nivel de confianza para cada una. Las emociones no forman parte de la consulta, solo son una guía para ayudarte a responder de forma adecuada."}]
    return chat

# def chatbot(pipe, text, chat, classifier):
#     actual_emotions = get_emotion(classifier, text)
#     emotions_text = ", ".join([f"{emotion} (confianza: {score:.2f})" for emotion, score in actual_emotions.items()])
#     message = {"role": "user", "content": text + f"\nEmociones: {emotions_text}"}
 
#     chat.append(message)
#     response = pipe(chat)[0]['generated_text'][-1]['content']
#     response = response.split('</think>')[-1]
#     chat.append({'role': 'assistant', 'content': response})
 
#     return chat

def format_message(user, text, classifier):
   
    interactions = retrieve_context(user, text)  # Lista de diccionarios con 'message', 'emotions', 'timestamp'
    # interactions = ["Hola, hoy estoy muy contento", "Hoy me siento muy motivado para hacer cosas nuevas", "Me siento muy excitado por la llegada de mi amigo"]
    # Construcción del contexto de mensajes anteriores
    context = "Contexto de mensajes anteriores:\n"
    context += "\n".join(interactions)

    emotions = get_emotion(classifier, text)
    emotions_text = ", ".join([f"{emotion} (confianza: {score:.2f})" for emotion, score in emotions.items()])
    message = f"{text} Emociones detectadas: {emotions_text}"
    msg_with_context = context + f"Mensaje actual, al que debes contestar teniendo en cuenta el contexto:\n{message}"
    store_message_emotions(user, message)
    return msg_with_context

def chatbot(user, pipe, text, classifier):
    chat = initialize_chatbot()

    message = format_message(user, text, classifier)
    chat.append({"role": "user", "content": message})

    response = pipe(chat)
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)


def main_prueba(user):

    pipe = load_chatbot()
    classifier = load_classifier()

    q = str(input(">>>"))

    while q != "exit":
        response = chatbot(user, pipe, q, classifier)
        print(response)
        q = str(input(">>>"))


# if __name__ == "__main__":
#     user = "John"
#     create_user(user)
#     main_prueba(user)