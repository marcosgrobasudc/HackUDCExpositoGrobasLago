# Use a pipeline as a high-level helper
# from transformers import pipeline


# messages = [{"role": "system", "content": "Eres un asistente empático que se adapta según los sentimientos del usuario"},
#     {"role": "user", "content": "Who are you?"},
# ]
# pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
# print(pipe(messages))


# # from transformers import pipeline

# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# sentences = ["I am not having a great day"]

# model_outputs = classifier(sentences)
# print(model_outputs[0])




# def main():
#     while True:
#         print("\nMenú Principal")
#         print("1. Hablar con el chatbot")
#         print("2. Hacer un registro diario")
#         print("3. Realizar test de BigFive")
#         print("4. Salir")
#         opcion = input("Elige una opción: ")
#         if opcion == "1":
#             chatbot()
#         elif opcion == "2":
#             registro_diario()
#         elif opcion == "3":
#             big_five()
#         elif opcion == "4":
#             print("¡Hasta luego!")
#             break
#         else:
#             print("Opción no válida. Intenta de nuevo.")

# if __name__ == "__main__":
    # main()


import gradio as gr
from datetime import date, timedelta
from transformers import pipeline
# from read_log import create_user, save_chat, read_chat
from groq import Groq
import re
from embeddings import retrieve_context, store_message_emotions
from relational_db import insert_daily_record, read_daily_record
import random

# Diccionario para almacenar los registros diarios
registros = {}

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

# Función para guardar o actualizar el registro diario
# def guardar_registro(selected_date, entry, username):
#     print('holaaaaaa', username)
#     registros[selected_date] = entry
#     return f"Registro para el día {selected_date} del usuario '{username}': {entry}"

# # Función para cargar el registro si existe
# def cargar_registro(selected_date):
#     return registros.get(selected_date, "")


# Función para guardar o actualizar el registro diario
def guardar_registro(selected_date, entry, username):
    print('Guardando registro para el usuario:', username)
    # Llamar a la función insert_daily_record para guardar el registro en la base de datos
    insert_daily_record(selected_date, entry, username)
    return f"Registro para el día {selected_date} del usuario '{username}': {entry}"

# Función para cargar el registro si existe
def cargar_registro(selected_date, username):
    # Llamar a la función read_daily_record para obtener el registro de la base de datos
    record = read_daily_record(selected_date, username)
    return record
    # if record:
    #     return f"Registro para el día {selected_date} del usuario '{username}': {record}"
    # else:
    #     return f"No hay registro para el día {selected_date} del usuario '{username}'."

# Función para iniciar la interfaz
def iniciar_interfaz(name):
    global username_value
    username_value = name
    saludo_actualizado = f"""
    <div style="position: fixed; top: 20px; right: 15px; 
                font-size: 16px; font-weight: bold; margin: 0; padding: 5px; line-height: 1;">
        Hola, {name}
    </div>
    """
    return gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.Tabs(visible=True)

# Función para generar una lista de fechas válidas
def generar_fechas_validas():
    today = date.today()
    return [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]


def chatbot_wrapper(messages, history=None):
    print(username_value)
    # print(username_input_value)
    return chatbot(username_value, pipe, messages, classifier)


if __name__ == "__main__":
    recent_chat = []
    # Crear la interfaz con Gradio
    with gr.Blocks(title="KeleaCare") as app:
        gr.HTML("""<script> document.title = "KeleaCare"; </script>""")
        
        # Evitar scrollbar vertical y reducir margen superior de las pestañas
        gr.HTML("""<style> body { overflow: hidden; height: 100vh; margin: 0; padding: 0; } .tabs-container { margin-top: -40px; }</style>""")

        # Componentes de inicio
        username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
        # username_input_value=f"Hola {username_input}"
        iniciar_btn = gr.Button("Iniciar")

        # Saludo personalizado (inicialmente oculto)
        greeting = gr.HTML("")  

        # Pestañas de opciones (inicialmente ocultas)
        tabs = gr.Tabs(visible=False, elem_classes=["tabs-container"])
        with tabs:
            with gr.TabItem("Chatbot"):
                # Cargar el chatbot y el clasificador
                pipe = load_chatbot()
                classifier = load_classifier()

                chat_interface = gr.ChatInterface(fn=chatbot_wrapper,
                                    type="messages",
                                    chatbot=gr.Chatbot(height=400, max_height=400),
                                    textbox=gr.Textbox(placeholder="Escribe tu pregunta", container=False, scale=7))

                # # Interfaz de chat
                # chat_interface = gr.ChatInterface(fn=lambda msg: chatbot(username_input.value, pipe, msg, classifier),
                #                                   type="messages",
                #                                   chatbot=gr.Chatbot(height=400, max_height=400),
                #                                   textbox=gr.Textbox(placeholder="Escribe tu pregunta", container=False, scale=7))

            with gr.TabItem("Registro Diario"):
                fechas_validas = generar_fechas_validas()
                selected_date = gr.Dropdown(label="Selecciona la fecha", choices=fechas_validas, value=date.today().strftime('%Y-%m-%d'))
                entry = gr.Textbox(label="Escribe tu registro diario...", placeholder="¿Cómo te sientes hoy?")
                output_registro = gr.Textbox(label="")
                guardar_btn = gr.Button("Guardar")
                
                selected_date.change(cargar_registro, inputs=[selected_date, username_input], outputs=entry)
                guardar_btn.click(guardar_registro, inputs=[selected_date, entry, username_input], outputs=output_registro)
            
            with gr.TabItem("Realizar test de BigFive"):
                test_results = gr.Textbox(label="Resultados del test BigFive...")
                output_test = gr.Textbox(label="Resultados del test")
                test_results.submit(lambda tr, u: f"Test BigFive completado con los siguientes resultados de {u}: {tr}",
                                    inputs=[test_results, username_input], outputs=output_test)

        # Botón de inicio
        iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

    # Lanzar la app
    app.launch(share=True)
