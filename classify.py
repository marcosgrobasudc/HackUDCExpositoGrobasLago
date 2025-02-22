from transformers import pipeline
# from read_log import read_interactions
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
    pipe = pipeline("text-generation", model="lmsys/vicuna-7b-v1.5")     
    pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    return pipe

def chatbot(pipe, text):
     messages = [{"role": "system", "content": "Eres un asistente empático que se adapta según los sentimientos del usuario"},
        {"role": "user", "content": text},
    ]
     return pipe(text)

def call_chatbot(user, pipe, actual_text):
    classifier = load_classifier()
    actual_emotions = get_emotion(classifier, actual_text)
    read_interactions(user) # lista de diccionarios con message, emotions, timestamp

    # read_interactions()

def call_chatbot(user, pipe, actual_text):
    classifier = load_classifier()
    actual_emotions = get_emotion(classifier, actual_text)
    interactions = read_interactions(user)  # Lista de diccionarios con 'message', 'emotions', 'timestamp'
    
    # Construcción del contexto de mensajes anteriores
    context = "Contexto de mensajes anteriores:\n"
    for interaction in interactions:
        message = interaction["message"]
        emotions = interaction["emotions"]
        emotions_text = ", ".join([f"{emotion} ({score:.2f})" for emotion, score in emotions.items()])
        context += f"Mensaje: {message}\nEmoción: {emotions_text}\n\n"

    # Agregar el mensaje actual
    context += f"Mensaje actual, al que debes contestar teniendo en cuenta el contexto:\n{actual_text}"
    
    return context




 


if __name__ == "__main__":
    bot = load_chatbot()
    print(chatbot(bot,"Hi, im irene"), chatbot(bot,"What is my name?"))