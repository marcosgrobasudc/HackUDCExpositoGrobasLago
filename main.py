# Use a pipeline as a high-level helper
from transformers import pipeline


messages = [{"role": "system", "content": "Eres un asistente empático que se adapta según los sentimientos del usuario"},
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
print(pipe(messages))


# from transformers import pipeline

# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

# sentences = ["I am not having a great day"]

# model_outputs = classifier(sentences)
# print(model_outputs[0])
# # produces a list of dicts for each of the labels


def main():
    while True:
        print("\nMenú Principal")
        print("1. Hablar con el chatbot")
        print("2. Hacer un registro diario")
        print("3. Realizar test de BigFive")
        print("4. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            chatbot()
        elif opcion == "2":
            registro_diario()
        elif opcion == "3":
            big_five()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()

