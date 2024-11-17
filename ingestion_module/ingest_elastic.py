from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_backend.models.elastic_search import ElasticsearchClient
from bs4 import BeautifulSoup
import requests
# from transformers import pipeline
from langchain_community.document_loaders import WebBaseLoader

# Configurações do Elasticsearch
es = ElasticsearchClient()

# Função para indexar um chunk no Elasticsearch
def index_chunk(index_name, chunk, article_name, article_id, url):
    body = {
        "article_name": article_name,
        "content": chunk,
        "article_fulldoc_url": url,
        "article_id": article_id
    }
    es.index(index_name=index_name, id=article_id, body=body)

# Função para extrair o título do artigo da tag meta
def extract_article_title_text_and_fulldocurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Erro ao acessar a URL: {url}")    
    soup = BeautifulSoup(response.text, "html.parser")
    
    
    meta_tag = soup.find("meta", attrs={"name": "title"})
    if not meta_tag or not meta_tag.get("content"):
        raise ValueError("Não foi possível encontrar a meta tag com o título do artigo.")    
    title = meta_tag.get("content")
    print(title)

    meta_tag = soup.find("meta", attrs={"name": "description"})
    if not meta_tag or not meta_tag.get("content"):
        raise ValueError("Não foi possível encontrar a meta tag com o título do artigo.")    
    description = meta_tag.get("content")
    print(description)

    button = soup.find("a", id="item-acessar")
    if button and button.has_attr("href"):
        href = button["href"]
        print(f"O link 'Acessar' foi encontrado: {href}")
    else:
        print("O botão/link com o texto 'Acessar' não foi encontrado.")
    print(href)

    return title, description, href
   

# Carrega os dados do website e processa os chunks
def fetch_and_process_website_summary(url):
    # 1. Extrair o título do artigo
    article_title, description, fulldoc_url = extract_article_title_text_and_fulldocurl(url)
    print(f"Título do artigo extraído: {article_title}")

    # 3. Dividir o conteúdo em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    document = Document(page_content=description, metadata={"title": article_title, "article_fulldoc_url": fulldoc_url})
    chunks = text_splitter.split_documents([document])
    print(f"Dividiu os documentos em {len(chunks)} chunks.")

    # 4. Ingerir os chunks no Elasticsearch
    for i, chunk in enumerate(chunks):
        # Adicionar um sufixo para distinguir múltiplos chunks do mesmo artigo
        chunk_id = f"{article_title}_chunk_{i}"
        index_chunk(index_name="summary_index", chunk=chunk.page_content, article_id=chunk_id, article_name=article_title, url=fulldoc_url),
        print(f"Indexou chunk com ID: {chunk_id}")

    
    fetch_and_process_website_full(url=fulldoc_url, article_title=article_title)    


# Carrega os dados do website e processa os chunks
def fetch_and_process_website_full(url, article_title):
    loader = WebBaseLoader(url)
    # 3. Dividir o conteúdo em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents([loader.load()[0].page_content])
    print(f"Dividiu os documentos em {len(chunks)} chunks.")

    # 4. Ingerir os chunks no Elasticsearch
    for i, chunk in enumerate(chunks):
        # Adicionar um sufixo para distinguir múltiplos chunks do mesmo artigo
        chunk_id = f"{article_title}_chunk_{i}"
        index_chunk(index_name="full_document_index", chunk=chunk.page_content, article_id=chunk_id, article_name=article_title, url=url),
        print(f"Indexou chunk com ID: {chunk_id}")

    print(f"Todos os chunks foram ingeridos no índice.")

# Executa o processamento e ingestão
if __name__ == "__main__":
    website_urls = ['https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W3159296334',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W4389737105',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W2121790392',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W4281643871',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W1990859777',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W2466199754',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W3004465710',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W4205441508',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W2916515250',
                    'https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?task=detalhes&source=&id=W2919890321',                    
                    ]
    
    for  url in website_urls:
        fetch_and_process_website_summary(url)