from transformers import pipeline
from read_log import read_chat, save_chat, create_user

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
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    return pipe

def initialize_chatbot():
    chat = [{"role": "system", "content": "Eres un asistente empático que se adapta según los sentimientos del usuario, los cuales serán especificados al final de cada mensaje junto a un nivel de confianaza para cada uno, pero no son parte del mensaje, solo una ayuda para que puedas contestarlo bien. Debes contestar en español."}]
    return chat

def chatbot(pipe, text, chat):
    classifier = load_classifier()
    actual_emotions = get_emotion(classifier, text)
    emotions_text = ", ".join([f"{emotion} (confianza: {score:.2f})" for emotion, score in actual_emotions.items()])
    message = {"role": "user", "content": text + f"\nEmociones: {emotions_text}"}
 
    chat.append(message)
 
    return pipe(chat, max_tokens=512)
 
def main_prueba(user):
    pipe = load_chatbot()

    if read_chat(user) == []:
        chat = initialize_chatbot()
    
    else:
        chat = read_chat(user)

    q = ""
    while q != "exit":
        q = str(input(">>>"))
        chat = chatbot(pipe, q, chat)[0]['generated_text']
        print(chat[-1]['content'])
    
    save_chat(user, chat)


if __name__ == "__main__":
    user = "John"
    create_user(user)
    main_prueba(user)