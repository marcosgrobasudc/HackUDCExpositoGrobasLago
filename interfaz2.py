

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
#     <div style="display: inline-block; position: absolute; top: 0px; right: 10px; 
#                 font-size: 16px; font-weight: bold; margin: 0; padding: 0; line-height: 1; height: auto;">
#         Hola, {name}
#     </div>
#     """
#     return gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.Tabs(visible=True)

# # Crear la interfaz con Gradio
# with gr.Blocks(title="KeleaCare") as app:
#     gr.HTML("""<script> document.title = "KeleaCare"; </script>""")

#     # Componentes de inicio
#     username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
#     iniciar_btn = gr.Button("Iniciar")

#     # Saludo personalizado (inicialmente oculto)
#     greeting = gr.HTML("")  

#     # Pestañas de opciones (inicialmente ocultas)
#     tabs = gr.Tabs(visible=False)
#     with tabs:
#         with gr.TabItem("Chatbot"):
#             chat_interface = gr.ChatInterface(fn=random_response, type="messages",    
#                 chatbot=gr.Chatbot(height=350, max_height=350),
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

# import gradio as gr
# import datetime
# from datetime import date
# import random

# # Diccionario para almacenar los registros diarios
# registros = {}

# # Función para el chatbot con respuestas aleatorias
# def random_response(messages):
#     responses = ["Hola, ¿cómo estás?", "Cuéntame más.", "Interesante...", "¿Cómo te sientes hoy?", "Eso suena genial."]
#     return random.choice(responses)

# # Función para obtener o actualizar un registro diario
# def obtener_registro(selected_date, username):
#     clave = f"{username}_{selected_date}"
#     return registros.get(clave, "")

# def guardar_registro(selected_date, entry, username):
#     clave = f"{username}_{selected_date}"
#     registros[clave] = entry
#     return f"Registro guardado para el día {selected_date}" 

# # Función para iniciar la interfaz
# def iniciar_interfaz(name):
#     saludo_actualizado = f"""
#     <div style="display: inline-block; position: absolute; top: 0px; right: 10px; 
#                 font-size: 16px; font-weight: bold; margin: 0; padding: 0; line-height: 1; height: auto;">
#         Hola, {name}
#     </div>
#     """
#     return gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.Tabs(visible=True)

# # Crear la interfaz con Gradio
# with gr.Blocks(title="KeleaCare") as app:
#     gr.HTML("""<script> document.title = "KeleaCare"; </script>""")

#     # gr.HTML("""
#     #     <style>
#     #         body {
#     #             margin: 0;
#     #             padding: 0;
#     #             overflow: hidden; /* Elimina el scroll */
#     #         }
#     #         .gradio-container {
#     #             overflow: hidden; /* Elimina el scroll en la interfaz */
#     #         }
#     #     </style>
#     # """)

#     # Componentes de inicio
#     username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
#     iniciar_btn = gr.Button("Iniciar")

#     # Saludo personalizado (inicialmente oculto)
#     greeting = gr.HTML("")  

#     # Pestañas de opciones (inicialmente ocultas)
#     tabs = gr.Tabs(visible=False)
#     with tabs:
#         with gr.TabItem("Chatbot"):
#             chat_interface = gr.ChatInterface(fn=random_response, type="messages",    
#                 chatbot=gr.Chatbot(height=350, max_height=350),
#                 textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7))

#         with gr.TabItem("Hacer un registro diario"):
#             selected_date = gr.DateTime(label="Selecciona la fecha", value=datetime.now().strftime("%Y-%m-%d"))
#             entry = gr.Textbox(label="¿Cómo te sientes hoy?", placeholder="Escribe aquí tu registro del día...", lines=5)
#             output_registro = gr.Textbox(label="Estado", interactive=False)
#             cargar_btn = gr.Button("Cargar Registro")
#             guardar_btn = gr.Button("Guardar Registro")

#             cargar_btn.click(obtener_registro, inputs=[selected_date, username_input], outputs=entry)
#             guardar_btn.click(guardar_registro, inputs=[selected_date, entry, username_input], outputs=output_registro)
        
#         with gr.TabItem("Realizar test de BigFive"):
#             test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
#             output_test = gr.Textbox(label="Resultados del test")
#             test_results.submit(lambda tr, u: f"Test BigFive completado con los siguientes resultados de {u}: {tr}",
#                                 inputs=[test_results, username_input], outputs=output_test)

#     # Botón de inicio
#     iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# # Lanzar la app
# app.launch()


import gradio as gr
from datetime import date, datetime
import random

# Diccionario para almacenar los registros diarios
registros = {}

# Función para el chatbot con respuestas aleatorias
def random_response(messages):
    responses = ["Hola, ¿cómo estás?", "Cuéntame más.", "Interesante...", "¿Cómo te sientes hoy?", "Eso suena genial."]
    return random.choice(responses)

# Función para guardar o actualizar el registro diario
def guardar_registro(selected_date, entry, username):
    registros[selected_date] = entry
    return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

# Función para cargar el registro si existe
def cargar_registro(selected_date):
    return registros.get(selected_date, "")

# Función para validar el formato de la fecha
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Función para iniciar la interfaz
def iniciar_interfaz(name):
    saludo_actualizado = f"""
    <div style="display: inline-block; position: absolute; top: 2px; right: 10px; 
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

        with gr.TabItem("Registro Diario"):
            selected_date = gr.Textbox(label="Escribe la fecha (YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
            entry = gr.Textbox(label="Escribe tu registro diario...", placeholder="¿Cómo te sientes hoy?")
            output_registro = gr.Textbox(label="Registro guardado")
            guardar_btn = gr.Button("Guardar")
            
            # Cargar el registro si existe
            selected_date.change(cargar_registro, inputs=selected_date, outputs=entry)
            
            # Guardar el registro
            guardar_btn.click(guardar_registro, inputs=[selected_date, entry, username_input], outputs=output_registro)

        with gr.TabItem("Realizar test de BigFive"):
            test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
            output_test = gr.Textbox(label="Resultados del test")
            test_results.submit(lambda tr, u: f"Test BigFive completado con los siguientes resultados de {u}: {tr}",
                                inputs=[test_results, username_input], outputs=output_test)

    # Botón de inicio
    iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# Lanzar la app
app.launch()