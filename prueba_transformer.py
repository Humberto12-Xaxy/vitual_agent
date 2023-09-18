from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Cargar el modelo GPT-3.5 y el tokenizador
modelo = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B")
tokenizador = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Texto de entrada
texto_entrada = "Tengo problemas con mi conexión a internet. "

# Codificar el texto de entrada en tokens
entrada_tokens = tokenizador.encode(texto_entrada, return_tensors="pt")

# Generar texto continuando la secuencia
salida = modelo.generate(entrada_tokens, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50)

# Decodificar la salida en texto
texto_salida = tokenizador.decode(salida[0], skip_special_tokens=True)

print("Texto generado:")
print(texto_salida)
