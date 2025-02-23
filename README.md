# KeleaCare: Asistente empático con análisis de personalidad

## Descripción

Este proyecto es un asistente conversacional empático funcional que interactúa con los usuarios, detecta emociones en los mensajes y ajusta sus respuestas de acuerdo con el estado emocional del usuario. Además, analiza los patrones conversacionales y registros diarios para inferir rasgos de personalidad según el modelo Big Five.

## Funcionalidades

- **Chatbot empático**: Procesa conversaciones y detecta emociones usando un modelo basado en BERT.
- **Registro diario**: Permite a los usuarios escribir registros sobre su estado emocional, almacenados en una base de datos relacional.
- **Análisis de personalidad**: Clasifica los rasgos de personalidad según el modelo Big Five a partir de embeddings generados en las conversaciones y registros.

## Dependencias

Este proyecto ha sido realizado en `python` y utiliza las siguientes librerías:

- `sklearn`
- `groq`
- `gradio`
- `pytorch`
- `transformers`
- `pandas`
- `re`
- `scipy`
- `numpy`
- `chromadb`
- `sentence-transformers`
- `uuid`
- `sqlite`

## Datasets
Este proyecto utiliza el dataset de textos con clasificación en los rasgos Big Five, disponible en el siguiente [repositorio](https://github.com/estiei/Big-Five-Backstage/blob/main/LICENSE).

## Uso

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el proyecto:
   ```bash
   python main.py
   ```
4. Una vez ejecutado, aparecerá un enlace en la terminal para acceder a la interfaz web de Gradio.

## Soporte

Para obtener ayuda sobre este proyecto, los usuarios pueden consultar la documentación en el repositorio o abrir un issue en GitHub.

## Autores

Este proyecto ha sido desarrollado por un equipo de estudiantes en inteligencia artificial: Alejandro Expósito, Marcos Grobas e Irene Lago, durante un hackathon en la UDC, cumpliendo un reto propuesto por la empresa Kelea.

## Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Todas las librerías utilizadas en este proyecto son compatibles con esta licencia, lo que permite su uso, modificación y distribución bajo los términos de la misma, siempre que se cumplan las condiciones establecidas, como la inclusión de los avisos de copyright y la licencia. Consulta el archivo LICENSE para más detalles.
