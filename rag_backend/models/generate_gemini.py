import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(GeminiClient, cls).__new__(cls)
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            cls.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 300,
                    "response_mime_type": "text/plain",
                },
            )
        return cls._instance

    def orchestrator(self, query):
        chat_session = self.model.start_chat(history=[])
        prompt = (
            "Você é um agente orquestrador de LLM, capaz de indicar qual o assistente correto que deve ser utilizado "
            "a depender da necessidade do usuário. Sua resposta deve ser sempre uma única string indicando qual o "
            "próximo agente que será chamado:\n\n"
            "Agente 1: Caso o usuário faça perguntas gerais sobre informações de artigos científicos sem citar algum "
            "específico, você deve retornar a string 'agent_general_search'.\n"
            "Agente 2: Caso o usuário solicite pesquisar mais detalhes de algum documento específico você deve retornar "
            "'agent_specific_search: ' e concatenar com o nome do documento ou autor que o usuário escolher.\n\n"
            "Exemplo 1: Quais os principais artigos referentes aos animais de grande porte?\n"
            "Resposta 1: 'agent_general_search'.\n\n"
            "Exemplo 2: A partir do Artigo 1, de Fulano de Tal, referente a animais de grandes portes, qual a metodologia de pesquisa?\n"
            "Resposta 2: 'agent_specific_search: Artigo 1'.\n\n"
            "EM HIPÓTESE ALGUMA PESQUISE NA WEB, use apenas os dados de input.\n\n"
            f"Pergunta: {query}"
        )
        response = chat_session.send_message(prompt)
        return response.text.strip()

    def generate_keywords(self, query):
        chat_session = self.model.start_chat(history=[])
        prompt = (
            "Você é um assistente de linguagem, que entende a partir do texto indicado pelo usuário, qual o tema "
            "principal da pergunta para pesquisas científicas, e retorna palavras-chaves que podem ser usadas para "
            "pesquisar em um acervo.\n\n"
            "Exemplo 1: Quais os principais artigos que temos em IA Generativa?\n"
            "Resposta 1: IA Generativa\n\n"
            "Exemplo 2: Qual é o estudo mais relevante em animais de grande porte como o elefante?\n"
            "Resposta 2: Elefante\n\n"
            "Seja sempre extremamente sucinto na resposta.\n\n"
            f"{query}"
        )
        response = chat_session.send_message(prompt)
        return response.text.strip()

    def generate_answer(self, retrieved_docs, query):
        chat_session = self.model.start_chat(history=[])
        
        context = "\n\n".join(f'"{article_name}": "{content}"' for article_name, content in retrieved_docs.items())

        formato_output = """
                        
                        {"Nome do Documento 1": "Resposta encontrada 1", "Nome do Documento n": "Resposta encontrada n"} 
                        
                        """
        
        
        prompt = (
            "Você é um assistente especializado em pesquisas científicas, que responde perguntas feitas com base nos "
            "documentos de contexto. \n\n"
            "Restrição: Use apenas o documento de contexto para responder e não use informações adicionais do modelo ou "
            "da internet. Sempre indique o nome do documento que foi usado como contexto na resposta.\n\n"
            f"Documentos:\n{context}\n\n"
            f"Pergunta: {query}\n\n"
            f"Resposta: Construa sua resposta como um JSON conforme o exemplo abaixo, \n {formato_output} "
            "\nSeja conciso na sua resposta, tente ser sempre o mais direto, use as aspas triplas para garantir que não quebrará o dicionário JSON, não traga o termo 'JSON' na resposta, apenas o dicionário"
        )
        print(prompt)
        response = chat_session.send_message(prompt)
        print(response)
        return response.text.strip()