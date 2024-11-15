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
        prompt = f"""Você é um agente orquestrador de LLM, capaz de indicar qual o assistente correto que deve ser utilizado a depender da necessidade do usuário
                    Sua resposta deve ser sempre uma única string indicando qual o próximo agente que será chamado:

                    Agente 1: Caso o usuário faça perguntas gerais sobre informações de artigos científicos sem citar algum específico, você deve retornar a string "agent_general_search"
                    Agente 2: Caso o usuário solicite pesquisar mais detalhes algum documento específico você deve retornar "agent_specific_search: " e concatenar com o nome do documento ou autor que o usuário escolher
                    
                    Exemplo 1: Quais os principais artigos referentes aos animais de grande porte?
                    Resposta 1: "agent_general_search"

                    Exemplo 2: A partir do Artigo 1, de Fulano de Tal, referente a animais de grandes portes, qual a metodologia de pesquisa?
                    Resposta 2: "agent_specif_search: Artigo 1"
                    
                    Aguarde as próximas perguntas para definir o agente

                    EM HIPÓTESE ALGUMA PESQUISE NA WEB, use apenas os dados de input
                    """
        
        gpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        answer = gpt_response["choices"][0]["text"].strip()
        return answer
    
    def generate_keywords(self, query):
        prompt = f"""Você é um assistente de linguagem, que entende a partir do texto indicado pelo usuário, qual o tema principal da pergunta para pesquisas científicas, e retorna palavras chaves que podem ser usadas para pesquisar em um acervo
                    Exemplo 1: Quais os principais artigos que temos em IA Generativa?
                    Resposta 1: IA Generativa, Ciência da Computação
                    
                    Exemplo 2: Qual é o estudo mais relevante em animais de grande porte como o elefante?
                    Resposta 2: Elefante, Biologia

                    Seja sempre extremamente sucinto na resposta, abaixo a pergunta que deve resumir em keywords
                    {query}"""
        gpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        answer = gpt_response["choices"][0]["text"].strip()
        return answer

    
    def generate_answer(self, retrieved_docs, query):
        context = "\n\n".join(retrieved_docs)
        prompt = f"""Você é um assistente especializado em pesquisas científicas, que responde perguntas feitas com base nos documentos de contexto.
                    Restrição: Use apenas o documento de contexto para responder e não use informações adicionais do modelo ou da internet.
                    Sempre indique o nome do documento que foi usado como contexto na resposta

                    Responda à pergunta abaixo com base nos seguintes documentos:

                    Documentos:
                    {context}

                    Pergunta:
                    {query}

                    Resposta:
                    Construa sua resposta trazendo Nome do Documento: Resposta encontrada"""

        gpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        answer = gpt_response["choices"][0]["text"].strip()
        return answer

