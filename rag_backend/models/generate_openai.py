import openai
from dotenv import load_dotenv
import os

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            api_key = os.environ.get('OPENAI_API_KEY', 'Empty')
            openai.api_key = api_key
        return cls._instance
    
    def orchestrator(self, query):
        messages = [
            {"role": "system", "content": (
                "Você é um agente orquestrador de LLM, capaz de indicar qual o assistente correto que deve ser utilizado "
                "a depender da necessidade do usuário. Sua resposta deve ser sempre uma única string indicando qual o "
                "próximo agente que será chamado: \n\n"
                "Agente 1: Caso o usuário faça perguntas gerais sobre informações de artigos científicos sem citar algum "
                "específico, você deve retornar a string 'agent_general_search'.\n"
                "Agente 2: Caso o usuário solicite pesquisar mais detalhes de algum documento específico você deve retornar "
                "'agent_specific_search: ' e concatenar com o nome do documento ou autor que o usuário escolher.\n\n"
                "Exemplo 1: Quais os principais artigos referentes aos animais de grande porte?\n"
                "Resposta 1: 'agent_general_search'.\n\n"
                "Exemplo 2: A partir do Artigo 1, de Fulano de Tal, referente a animais de grandes portes, qual a metodologia de pesquisa?\n"
                "Resposta 2: 'agent_specific_search: Artigo 1'.\n\n"
                "EM HIPÓTESE ALGUMA PESQUISE NA WEB, use apenas os dados de input."
            )},
            {"role": "user", "content": f"Pergunta: {query}"}
        ]
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def generate_keywords(self, query):
        messages = [
            {"role": "system", "content": (
                "Você é um assistente de linguagem, que entende a partir do texto indicado pelo usuário, qual o tema "
                "principal da pergunta para pesquisas científicas, e retorna palavras-chaves que podem ser usadas para "
                "pesquisar em um acervo.\n\n"
                "Exemplo 1: Quais os principais artigos que temos em IA Generativa?\n"
                "Resposta 1: IA Generativa, Ciência da Computação\n\n"
                "Exemplo 2: Qual é o estudo mais relevante em animais de grande porte como o elefante?\n"
                "Resposta 2: Elefante, Biologia\n\n"
                "Seja sempre extremamente sucinto na resposta."
            )},
            {"role": "user", "content": query}
        ]
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def generate_answer(self, retrieved_docs, query):
        context = "\n\n".join(retrieved_docs)
        messages = [
            {"role": "system", "content": (
                "Você é um assistente especializado em pesquisas científicas, que responde perguntas feitas com base nos "
                "documentos de contexto. \n\n"
                "Restrição: Use apenas o documento de contexto para responder e não use informações adicionais do modelo ou "
                "da internet. Sempre indique o nome do documento que foi usado como contexto na resposta."
            )},
            {"role": "assistant", "content": f"Documentos:\n{context}"},
            {"role": "user", "content": f"Pergunta: {query}"}
        ]
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()