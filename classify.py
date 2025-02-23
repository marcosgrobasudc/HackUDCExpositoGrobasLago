import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
# from chatbot import load_chatbot
import re
import torch
from big_five import BETOBigFive
from transformers import AutoTokenizer, pipeline
# from embeddings import retrieve_embedding
# from relational_db import read_all_records


# Función para cargar el clasificador de emociones
def load_classifier():
    classifier = pipeline(task="text-classification", model="finiteautomata/beto-emotion-analysis", top_k=None)
    return classifier

# Función para obtener emociones
def get_emotion(classifier, sentences):
    model_outputs = classifier(sentences)
    result = {}

    accumulated_score = 0.0
    for emotion in model_outputs[0]:
        accumulated_score += emotion['score']
        result[emotion['label']] = emotion['score']
        if accumulated_score >= 0.7:
            break
    return result  # Devuelve un diccionario con las emociones y su confianza


def reduce_embeddings_kmeans(embeddings, texts, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(embeddings)
   
    # Obtener los centroides
    centroids = kmeans.cluster_centers_
 
    # Encontrar el texto más cercano a cada centroide
    selected_texts = []
    for centroid in centroids:
        distances = cdist([centroid], embeddings, metric='euclidean')  # Distancia a todos los puntos
        closest_idx = np.argmin(distances)  # Índice del punto más cercano
        selected_texts.append(texts[closest_idx])  # Guardar el texto correspondiente
   
    return selected_texts

 
# embeddings = matriz (n_textos, dim_embedding)
# texts = lista de textos originales
def reduce_chat(embeddings, texts, registry, pipe, n_clusters = 3):
    if len(embeddings) < n_clusters:
        reduced_texts = texts
    else:
        reduced_texts = reduce_embeddings_kmeans(embeddings, texts, n_clusters)
    message = "\n".join(reduced_texts) + "Registro diario:\n" + "\n".join([f"{date}: {record}" for date, record in registry])
    command = 'Eres un asistente que resume y se queda con lo importante del texto. Hablas en español.'
    input = [{'role': 'system', 'content': command},{'role': 'user', 'content': message}]
    response = pipe(input)
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    return response


def get_model_big5():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BETOBigFive().to(device)
    model.load_state_dict(torch.load("beto_big5.pth", map_location=device))
    tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")
    return model, tokenizer, device
 
def predict_big5(text, model, tokenizer, device):
    # model, tokenizer, device = get_model_big5()
    encoding = tokenizer(text, padding='max_length', truncation=True, max_length=512, return_tensors="pt")
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_ids, attention_mask)
   
    return output.detach().cpu().numpy().flatten()
 
def map_logits_to_big5(logits):
    big5 = ["Extroversión", "Amabilidad", "Apertura a la experiencia", "Neuroticismo", "Responsabilidad"]
    return {big5[i]: logits[i] for i in range(5)}

def registry_big5(embeddings, texts, registry, pipe, model, tokenizer, device):
    input = reduce_chat(embeddings, texts, registry, pipe, 3)
    logits = predict_big5(input, model, tokenizer, device)
    big5 = map_logits_to_big5(logits)
    message=""
    for personality, score in big5.items():
        message += f"{personality}: {score:.2f}\n"
    command = 'Eres un asistente que habla en ESPAÑOL. Describe la personalidad y forma de ser del usuario y clasifica su personalidad según Big5. Se te proporcionan intervenciones del usuario en un chat y un registro diario de su estado. También se te proporciona una puntuación para cada rasgo de la personalidad del usuario. Tienes que basarte en esas puntuaciones, pero es muy importante que NO las menciones en ningún momento. En tu respuesta, puedes hacer referencia al chat y al registro, pero NO inventes datos. Ve explicando cómo es el usuario en cada uno de los 5 rasgos de Big5, con un grado de pertenencia a ese rasgo (bajo, medio, alto, muy alto). Puedes utilizar emoticonos en los títulos.'
    input = [{'role': 'system', 'content': command},{'role': 'user', 'content': message}]
    response = pipe(input)
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

# if __name__ == "__main__":
#     # Lista de textos (mensajes) de un usuario
#     texts = [
#         "Hola, ¿cómo estás? Estoy sintiéndome muy bien hoy.",
#         "La vida es difícil a veces, pero trato de mantenerme positivo.",
#         "Ayer fue un día genial, salí con mis amigos y nos divertimos mucho.",
#         "Últimamente he estado muy estresado por el trabajo.",
#         "Me encanta leer libros, especialmente novelas de misterio."
#     ]

#     # Lista de embeddings correspondientes a cada texto (ejemplo ficticio)
#     embeddings = [
#         [0.1, 0.02, -0.05, 0.03, 0.07, -0.01, 0.09, -0.04, 0.2, 0.05],  # Embedding de texto 1
#         [0.03, -0.08, 0.07, 0.1, -0.06, 0.04, -0.02, 0.08, -0.1, 0.06],  # Embedding de texto 2
#         [0.2, 0.05, 0.03, -0.1, 0.02, -0.03, 0.05, 0.07, -0.02, 0.01],  # Embedding de texto 3
#         [-0.05, 0.09, -0.02, 0.08, 0.01, -0.04, 0.1, -0.07, 0.03, -0.06],  # Embedding de texto 4
#         [0.04, -0.03, 0.09, -0.02, 0.05, -0.08, 0.02, 0.1, -0.1, 0.07]   # Embedding de texto 5
#     ]
#     pipe = load_chatbot()
#     model, tokenizer, device = get_model_big5()
#     user_name = "John"
#     date = "2022-05-15"
#     texts, embeddings = retrieve_embedding(user_name)
#     registry = read_daily_record(date, user_name)
#     print(registry_big5(embeddings, texts, registry, pipe, model, tokenizer, device))