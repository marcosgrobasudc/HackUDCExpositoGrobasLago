import gradio as gr
from datetime import date, timedelta
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
    return f"Registro para el día {selected_date} del usuario '{username}': {entry}"

# Función para cargar el registro si existe
def cargar_registro(selected_date):
    return registros.get(selected_date, "")

# Función para iniciar la interfaz
def iniciar_interfaz(name):
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

# Crear la interfaz con Gradio
with gr.Blocks(title="KeleaCare") as app:
    gr.HTML("""<script> document.title = "KeleaCare"; </script>""")

    # Evitar scrollbar vertical y reducir margen superior de las pestañas
    gr.HTML("""
    <style> 
        body { overflow: hidden; height: 100vh; margin: 0; padding: 0; } 
        .tabs-container { margin-top: -40px; }
    </style>
    """)

    # Componentes de inicio
    username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
    iniciar_btn = gr.Button("Iniciar")

    # Saludo personalizado (inicialmente oculto)
    greeting = gr.HTML("")  

    # Pestañas de opciones (inicialmente ocultas)
    tabs = gr.Tabs(visible=False, elem_classes=["tabs-container"])  # Aplicamos la clase CSS aquí
    with tabs:
        with gr.TabItem("Chatbot"):
            chat_interface = gr.ChatInterface(fn=random_response, type="messages",
                chatbot=gr.Chatbot(height=400, max_height=400),
                textbox=gr.Textbox(placeholder="Escribe tu pregunta", container=False, scale=7))

        with gr.TabItem("Registro Diario"):
            fechas_validas = generar_fechas_validas()
            selected_date = gr.Dropdown(label="Selecciona la fecha", choices=fechas_validas, value=date.today().strftime('%Y-%m-%d'))
            entry = gr.Textbox(label="Escribe tu registro diario...", placeholder="¿Cómo te sientes hoy?")
            output_registro = gr.Textbox(label="")
            guardar_btn = gr.Button("Guardar")
            
            selected_date.change(cargar_registro, inputs=selected_date, outputs=entry)
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
