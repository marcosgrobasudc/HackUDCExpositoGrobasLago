import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import re
import torch
from big_five import BETOBigFive
from transformers import AutoTokenizer, pipeline

def load_classifier():
    """
    Cargar el clasificador de emociones

    Returns:
    classifier: clasificador de emociones
    """
    classifier = pipeline(task="text-classification", model="finiteautomata/beto-emotion-analysis", top_k=None)
    return classifier

def get_emotion(classifier, sentences):
    """
    Obtener el resultado de clasificar las emociones de un texto

    Args:
    classifier: clasificador de emociones
    sentences: lista de frases a clasificar

    Returns:
    result: diccionario con las emociones y su confianza
    """
    model_outputs = classifier(sentences)
    result = {}

    accumulated_score = 0.0
    for emotion in model_outputs[0]:
        accumulated_score += emotion['score']
        result[emotion['label']] = emotion['score']
        if accumulated_score >= 0.7:
            break
    return result


def reduce_embeddings_kmeans(embeddings, texts, n_clusters=5):
    """
    Realiza un clustering de los embeddings y selecciona el texto más cercano a cada centroide

    Args:
    embeddings: matriz de embeddings
    texts: lista de textos
    n_clusters: número de clusters
    
    Returns:
    selected_texts: lista de textos
    """
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

def reduce_chat(embeddings, texts, registry, pipe, n_clusters = 3):
    """
    Reducir los textos de un chat a un número menor de textos

    Args:
    embeddings: matriz de embeddings
    texts: lista de textos
    registry: lista de tuplas (fecha, registro)
    pipe: chatbot
    n_clusters: número de clusters

    Returns:
    response: respuesta del chatbot
    """
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
    """
    Cargar el modelo de clasificación de personalidad Big5
    
    Returns:
    model: modelo de clasificación
    tokenizer: tokenizador
    device: dispositivo de ejecución
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BETOBigFive().to(device)
    model.load_state_dict(torch.load("beto_big5.pth", map_location=device))
    tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased")
    return model, tokenizer, device
 
def predict_big5(text, model, tokenizer, device):
    """
    Predecir los rasgos de personalidad Big5 de un texto
    
    Args:
    text: texto a clasificar
    model: modelo de clasificación
    tokenizer: tokenizador
    device: dispositivo de ejecución

    Returns:
    logits: logits de la clasificación
    """
    encoding = tokenizer(text, padding='max_length', truncation=True, max_length=512, return_tensors="pt")
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_ids, attention_mask)
   
    return output.detach().cpu().numpy().flatten()
 
def map_logits_to_big5(logits):
    """
    Mapear los logits de clasificación a los rasgos de personalidad Big5
    
    Args:
    logits: logits de clasificación

    Returns:
    big5: diccionario con los rasgos de personalidad Big
    """
    big5 = ["Extroversión", "Amabilidad", "Apertura a la experiencia", "Neuroticismo", "Responsabilidad"]
    return {big5[i]: logits[i] for i in range(5)}

def registry_big5(embeddings, texts, registry, pipe, model, tokenizer, device):
    """
    Clasificar la personalidad Big5 de un usuario a partir de un chat y un registro diario
    
    Args:
    embeddings: matriz de embeddings
    texts: lista de textos
    registry: lista de tuplas (fecha, registro)
    pipe: chatbot
    model: modelo de clasificación
    tokenizer: tokenizador
    device: dispositivo de ejecución

    Returns:
    response: respuesta del chatbot
    """
    input = reduce_chat(embeddings, texts, registry, pipe, 3)
    logits = predict_big5(input, model, tokenizer, device)
    big5 = map_logits_to_big5(logits)
    message=""
    for personality, score in big5.items():
        message += f"{personality}: {score:.2f}\n"
    command = 'Eres un asistente que habla en ESPAÑOL. Describe la personalidad y forma de ser del usuario y clasifica su personalidad según Big5. Se te proporcionan intervenciones del usuario en un chat y un registro diario de su estado. También se te proporciona una puntuación para cada rasgo de la personalidad del usuario. Tienes que basarte en esas puntuaciones, pero es muy importante que NO las menciones en ningún momento. En tu respuesta, puedes hacer referencia al chat y al registro. Ve explicando cómo es el usuario en cada uno de los 5 rasgos de Big5, con un grado de pertenencia a ese rasgo (bajo, medio, alto, muy alto). Puedes utilizar emoticonos en los títulos.'
    input = [{'role': 'system', 'content': command},{'role': 'user', 'content': message}]
    response = pipe(input)
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)