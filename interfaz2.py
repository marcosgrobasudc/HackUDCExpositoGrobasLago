# import gradio as gr
# from datetime import date
# import random

# # Función para el chatbot con respuestas aleatorias
# def random_response(messages):
#     responses = ["Hola, ¿cómo estás?", "Cuéntame más.", "Interesante...", "¿Cómo te sientes hoy?", "Eso suena genial."]
#     return random.choice(responses)

# # Funciones originales
# def registro_diario(selected_date, entry, username):
#     return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

# def big_five(test_results, username):
#     return f"Test BigFive completado con los siguientes resultados de {username}: {test_results}"

# # Función para iniciar la interfaz
# def iniciar_interfaz(name):
#     saludo_actualizado = f"""
#     <div style="width: 100%; text-align: right; font-size: 18px; font-weight: bold; 
#                 margin-top: 2px; margin-bottom: 2px; padding: 0;">
#         Hola, {name}
#     </div>
#     """
#     return gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.Tabs(visible=True)

# # Crear la interfaz con Gradio
# with gr.Blocks(title="KeleaCare") as app:
#     gr.HTML("""
#         <script>
#             document.title = "KeleaCare";  
#         </script>
#     """)

#     # Componentes de inicio
#     username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
#     iniciar_btn = gr.Button("Iniciar")

#     # Saludo personalizado (inicialmente oculto)
#     greeting = gr.HTML("")  

#     # Contenedor para el saludo
#     with gr.Row(): 
#         greeting  

#     # Pestañas de opciones (inicialmente ocultas)
#     tabs = gr.Tabs(visible=False)
#     with tabs:
#         with gr.TabItem("Chatbot"):
#             chat_interface = gr.ChatInterface(fn=random_response, type="messages",    chatbot=gr.Chatbot(height=300, max_height=300),
#                 textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7))

#         with gr.TabItem("Hacer un registro diario"):
#             selected_date = gr.Textbox(label="Escribe la fecha (YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
#             entry = gr.Textbox(label="Escribe tu registro diario...")
#             output_registro = gr.Textbox(label="Registro guardado")
#             entry.submit(registro_diario, inputs=[selected_date, entry, username_input], outputs=output_registro)

#         with gr.TabItem("Realizar test de BigFive"):
#             test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
#             output_test = gr.Textbox(label="Resultados del test")
#             test_results.submit(big_five, inputs=[test_results, username_input], outputs=output_test)

#     # Botón de inicio
#     iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# # Lanzar la app
# app.launch()

import gradio as gr
from datetime import date
import random

# Función para el chatbot con respuestas aleatorias
def random_response(messages):
    responses = ["Hola, ¿cómo estás?", "Cuéntame más.", "Interesante...", "¿Cómo te sientes hoy?", "Eso suena genial."]
    return random.choice(responses)

# Funciones originales
def registro_diario(selected_date, entry, username):
    return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

def big_five(test_results, username):
    return f"Test BigFive completado con los siguientes resultados de {username}: {test_results}"

# Función para iniciar la interfaz
def iniciar_interfaz(name):
    saludo_actualizado = f"""
    <div style="display: inline-block; position: absolute; top: 0px; right: 10px; 
                font-size: 16px; font-weight: bold; margin: 0; padding: 0; line-height: 1; height: auto;">
        Hola, {name}
    </div>
    """
    return gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.Tabs(visible=True)

# Crear la interfaz con Gradio
with gr.Blocks(title="KeleaCare") as app:
    gr.HTML("""<script> document.title = "KeleaCare"; </script>""")

    # Componentes de inicio
    username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
    iniciar_btn = gr.Button("Iniciar")

    # Saludo personalizado (inicialmente oculto)
    greeting = gr.HTML("")  

    # Pestañas de opciones (inicialmente ocultas)
    tabs = gr.Tabs(visible=False)
    with tabs:
        with gr.TabItem("Chatbot"):
            chat_interface = gr.ChatInterface(fn=random_response, type="messages",    
                chatbot=gr.Chatbot(height=350, max_height=350),
                textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7))

        with gr.TabItem("Hacer un registro diario"):
            selected_date = gr.Textbox(label="Escribe la fecha (YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
            entry = gr.Textbox(label="Escribe tu registro diario...")
            output_registro = gr.Textbox(label="Registro guardado")
            entry.submit(registro_diario, inputs=[selected_date, entry, username_input], outputs=output_registro)

        with gr.TabItem("Realizar test de BigFive"):
            test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
            output_test = gr.Textbox(label="Resultados del test")
            test_results.submit(big_five, inputs=[test_results, username_input], outputs=output_test)

    # Botón de inicio
    iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# Lanzar la app
app.launch()
