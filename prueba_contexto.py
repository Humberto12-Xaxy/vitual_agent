import spacy
nlp = spacy.load("es_core_news_sm")
import es_core_news_sm

nlp = es_core_news_sm.load()

def get_context(text):
    # Analizar el texto
    doc = nlp(text)
    
    # Obtener el contexto
    context = [w for w in doc.noun_chunks]

    # Devolver el contexto
    return context

print(get_context("muchas gracias bye"))
