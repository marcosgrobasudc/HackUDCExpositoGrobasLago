# # import gradio as gr
# # from datetime import date

# # # Funciones
# # def chatbot(input_text):
# #     return f"Chatbot respondido: {input_text}"

# # def registro_diario(selected_date, entry, username):
# #     return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

# # def big_five(test_results, username):
# #     return f"Test BigFive completado con los siguientes resultados de {username}: {test_results}"

# # # Función para iniciar la interfaz
# # def iniciar_interfaz(name):
# #     # Guarda el nombre del usuario
# #     greeting.value = f"Hola, {name}"
# #     # Cambiar visibilidad de los componentes
# #     return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)

# # # Crear la interfaz con Gradio
# # with gr.Blocks() as app:
# #     # Definir componentes
# #     username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
# #     iniciar_btn = gr.Button("Iniciar")

# #     # Saludo personalizado (invisible al inicio)
# #     # greeting = gr.Textbox(label="Saludo", interactive=False, visible=False)
# #     greeting = gr.Markdown(value="", visible=False)

# #     # Contenedor para mostrar el saludo en la parte superior derecha
# #     with gr.Row():
# #         gr.Textbox(value=" ", interactive=False, visible=False)  # Espaciador vacío
# #         greeting  # Saludo se alinea a la derecha dentro de la fila

# #     # Pestañas de opciones (inicialmente ocultas)
# #     with gr.Tabs(visible=False) as tabs:
# #         with gr.TabItem("Hablar con el chatbot"):
# #             input_text = gr.Textbox(label="Escribe algo para el chatbot...")
# #             output_chatbot = gr.Textbox(label="Respuesta del Chatbot")
# #             input_text.submit(chatbot, inputs=input_text, outputs=output_chatbot)

# #         with gr.TabItem("Hacer un registro diario"):
# #             selected_date = gr.Textbox(label="Escribe la fecha (formato: YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
# #             entry = gr.Textbox(label="Escribe tu registro diario...")
# #             output_registro = gr.Textbox(label="Registro guardado")
# #             entry.submit(registro_diario, inputs=[selected_date, entry, username_input], outputs=output_registro)

# #         with gr.TabItem("Realizar test de BigFive"):
# #             test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
# #             output_test = gr.Textbox(label="Resultados del test")
# #             test_results.submit(big_five, inputs=[test_results, username_input], outputs=output_test)

# #     # Hacer clic en el botón de iniciar y actualizar la interfaz
# #     iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# # # Lanzar la interfaz
# # app.launch()

import gradio as gr
from datetime import date

# Funciones
def chatbot(input_text):
    return f"Chatbot respondido: {input_text}"

def registro_diario(selected_date, entry, username):
    return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

def big_five(test_results, username):
    return f"Test BigFive completado con los siguientes resultados de {username}: {test_results}"

# Función para iniciar la interfaz
def iniciar_interfaz(name):
    # Actualiza el saludo con el nombre del usuario
    greeting.value = f"Hola, {name}"  # Saludo sin el HTML para Markdown
    # Cambiar visibilidad de los componentes
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

# Crear la interfaz con Gradio
with gr.Blocks() as app:
    # Cambiar el título de la pestaña mediante un componente HTML al principio
    gr.HTML("<script>document.title = 'KeleaCare';</script>")

    # Definir componentes
    username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
    iniciar_btn = gr.Button("Iniciar")

    # Saludo personalizado (invisible al inicio)
    greeting = gr.Markdown(value="", visible=False)  # Markdown para mostrar el saludo

    # Contenedor para mostrar el saludo en la parte superior
    with gr.Column():
        greeting  # Saludo se coloca en la parte superior, dentro de una columna

    # Pestañas de opciones (inicialmente ocultas)
    with gr.Tabs() as tabs:
        with gr.TabItem("Hablar con el chatbot"):
            input_text = gr.Textbox(label="Escribe algo para el chatbot...")
            output_chatbot = gr.Textbox(label="Respuesta del Chatbot")
            input_text.submit(chatbot, inputs=input_text, outputs=output_chatbot)

        with gr.TabItem("Hacer un registro diario"):
            selected_date = gr.Textbox(label="Escribe la fecha (formato: YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
            entry = gr.Textbox(label="Escribe tu registro diario...")
            output_registro = gr.Textbox(label="Registro guardado")
            entry.submit(registro_diario, inputs=[selected_date, entry, username_input], outputs=output_registro)

        with gr.TabItem("Realizar test de BigFive"):
            test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
            output_test = gr.Textbox(label="Resultados del test")
            test_results.submit(big_five, inputs=[test_results, username_input], outputs=output_test)

    # Hacer clic en el botón de iniciar y actualizar la interfaz
    iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting])

# Lanzar la interfaz
app.launch()


# import gradio as gr
# from datetime import date

# # Funciones
# def chatbot(input_text):
#     return f"Chatbot respondido: {input_text}"

# def registro_diario(selected_date, entry, username):
#     return f"Registro para el día {selected_date} de {username} guardado con el texto: {entry}"

# def big_five(test_results, username):
#     return f"Test BigFive completado con los siguientes resultados de {username}: {test_results}"

# # Función para iniciar la interfaz
# def iniciar_interfaz(name):
#     # Actualiza el saludo con el nombre del usuario
#     greeting.update(value=f"Hola, {name}", visible=True)  # Actualizar el saludo
#     # Cambiar visibilidad de los componentes
#     return (
#         gr.update(visible=False),  # Ocultar el input de nombre
#         gr.update(visible=False),  # Ocultar el botón de iniciar
#         gr.update(visible=True),   # Mostrar el saludo
#         gr.update(visible=True)    # Mostrar las pestañas
#     )

# # Crear la interfaz con Gradio
# with gr.Blocks() as app:
#     # Cambiar el título de la pestaña usando JavaScript
#     gr.HTML("<script>document.title = 'KeleaCare';</script>")

#     # Definir componentes
#     username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
#     iniciar_btn = gr.Button("Iniciar")

#     # Saludo personalizado (invisible al inicio)
#     greeting = gr.Textbox(label="", value="", interactive=False, visible=False)  # Usamos Textbox para el saludo

#     # Contenedor para el saludo (arriba a la derecha)
#     with gr.Row():
#         # Columna vacía para ocupar espacio a la izquierda
#         gr.Column(scale=3)  # Ajusta el espacio a la izquierda
#         # Columna para el saludo
#         with gr.Column(scale=1):
#             greeting  # Saludo se coloca en la parte superior derecha

#     # Pestañas de opciones (inicialmente ocultas)
#     with gr.Tabs(visible=False) as tabs:
#         with gr.TabItem("Hablar con el chatbot"):
#             input_text = gr.Textbox(label="Escribe algo para el chatbot...")
#             output_chatbot = gr.Textbox(label="Respuesta del Chatbot")
#             input_text.submit(chatbot, inputs=input_text, outputs=output_chatbot)

#         with gr.TabItem("Hacer un registro diario"):
#             selected_date = gr.Textbox(label="Escribe la fecha (formato: YYYY-MM-DD)", value=date.today().strftime('%Y-%m-%d'))
#             entry = gr.Textbox(label="Escribe tu registro diario...")
#             output_registro = gr.Textbox(label="Registro guardado")
#             entry.submit(registro_diario, inputs=[selected_date, entry, username_input], outputs=output_registro)

#         with gr.TabItem("Realizar test de BigFive"):
#             test_results = gr.Textbox(label="Escribe los resultados del test BigFive...")
#             output_test = gr.Textbox(label="Resultados del test")
#             test_results.submit(big_five, inputs=[test_results, username_input], outputs=output_test)

#     # Hacer clic en el botón de iniciar y actualizar la interfaz
#     iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, greeting, tabs])

# # Lanzar la interfaz
# app.launch()