from transformers import pipeline
from read_log import create_user, save_chat, read_chat

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
    chat = [{"role": "system", "content": "You are an empathetic assistant who adapts according to the user's feelings, which will be specified at the end of each message along with a confidence level for each. However, they are not part of the message, just a guide to help you respond appropriately."}]
    return chat

def chatbot(pipe, text, chat, classifier):
    actual_emotions = get_emotion(classifier, text)
    emotions_text = ", ".join([f"{emotion} (confidence: {score:.2f})" for emotion, score in actual_emotions.items()])
    message = {"role": "user", "content": text + f"\nEmotions: {emotions_text}"}
 
    chat.append(message)
    response = pipe(chat, max_new_tokens=512)[0]['generated_text'][-1]['content']
    response = response.split('</think>')[-1]
    chat.append({'role': 'assistant', 'content': response})
 
    return chat
 
def load_models():
    classifier = load_classifier()
    pipe = load_chatbot()
    return classifier, pipe

def main_prueba(user, pipe, classifier):
    if read_chat(user) == []:
        chat = initialize_chatbot()
    
    else:
        chat = read_chat(user)
    q = ""
    while q != "exit":
        q = str(input(">>>"))
        chat = chatbot(pipe, q, chat, classifier)
        # print(chat[-1]['content'])
        print(chat)
    
    save_chat(user, chat)


if __name__ == "__main__":
    user = "John"
    create_user(user)
    main_prueba(user)