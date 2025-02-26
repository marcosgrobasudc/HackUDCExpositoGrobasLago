import gradio as gr
from datetime import date
from chatbot import chatbot, load_chatbot, analise_big5
from classify import load_classifier
from registry import cargar_registro, guardar_registro, generar_fechas_validas


def iniciar_interfaz(name):
    """
    Función para iniciar la interfaz con el nombre de usuario

    Args:
    name (str): nombre de usuario

    Returns:
    str: sal
    """
    global username_value
    username_value = name
    saludo_actualizado = f"""
    <div style="position: fixed; top: 20px; right: 15px; 
                font-size: 16px; font-weight: bold; margin: 0; padding: 5px; line-height: 1;">
        Hola, {name}
    </div>
    """
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(value=saludo_actualizado), gr.update(visible=True)

def chatbot_wrapper(messages, history=None):
    """
    Wrapper para el chatbot que recibe los mensajes y llama a la función principal
    
    Args:
    messages (list): lista de mensajes
    history (list): historial de mensajes

    Returns:
    str: respuesta del chatbot
    """
    print(username_value)
    return chatbot(username_value, pipe, messages, classifier)


if __name__ == "__main__":
    with gr.Blocks(title="KeleaCare") as app:
        gr.HTML("""<script> document.title = "KeleaCare"; </script>""")
        
        gr.HTML("""<style> 
            body { overflow: hidden; height: 100vh; margin: 0; padding: 0; }
            .tabs-container { margin-top: -40px; }
            #test_output { max-height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        </style>""")
        
        with gr.Column():
            imagen = gr.Image(value="https://media-asgard.s3.eu-west-1.amazonaws.com/22/09/15/20cc2074-3d1b-461c-8442-ddff0d14ca2d_kelea.png", 
                              label="", show_label=False, interactive=False,
                              elem_id="imagen_kelea", image_mode="auto", height=100)
            username_input = gr.Textbox(label="Introduce tu nombre de usuario", placeholder="username")
            iniciar_btn = gr.Button("Iniciar")

        greeting = gr.HTML("")

        tabs = gr.Tabs(visible=False, elem_classes=["tabs-container"])
        with tabs:
            with gr.TabItem("Chatbot"):
                pipe = load_chatbot()
                classifier = load_classifier()
                chat_interface = gr.ChatInterface(fn=chatbot_wrapper,
                                    type="messages",
                                    chatbot=gr.Chatbot(height=400, max_height=400),
                                    textbox=gr.Textbox(placeholder="Escribe tu pregunta", container=False, scale=7))

            with gr.TabItem("Registro Diario"):
                fechas_validas = generar_fechas_validas()
                selected_date = gr.Dropdown(label="Selecciona la fecha", choices=fechas_validas, value=date.today().strftime('%Y-%m-%d'))
                entry = gr.Textbox(label="Escribe tu registro diario...", placeholder="¿Cómo te sientes hoy?")
                output_registro = gr.Textbox(label="")
                guardar_btn = gr.Button("Guardar")
                
                selected_date.change(cargar_registro, inputs=[selected_date, username_input], outputs=entry)
                guardar_btn.click(guardar_registro, inputs=[selected_date, entry, username_input], outputs=output_registro)
            
            with gr.TabItem("Realizar test de BigFive"):
                analizar_btn = gr.Button("Realizar Análisis Big Five")
                output_test = gr.Markdown(elem_id="test_output")  
                analizar_btn.click(fn=analise_big5, inputs=[username_input], outputs=output_test)

        iniciar_btn.click(iniciar_interfaz, inputs=username_input, outputs=[username_input, iniciar_btn, imagen, greeting, tabs])

    app.launch(share=True)
