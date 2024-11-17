from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_backend.models.elastic_search import ElasticsearchClient
from bs4 import BeautifulSoup
import requests
from langchain_community.document_loaders import WebBaseLoader
from sentence_transformers import SentenceTransformer 


model = SentenceTransformer('all-MiniLM-L6-v2')
# Configurações do Elasticsearch
es = ElasticsearchClient()

# Função para indexar um chunk no Elasticsearch
def index_chunk(index_name, chunk, article_name, article_id, url):
    embedding = model.encode(chunk).tolist()
    body = {
        "article_name": article_name,
        "content": chunk,
        "article_fulldoc_url": url,
        "article_id": article_id,
        "embedding": embedding
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
    print("loader", loader.load())
    chunks = text_splitter.split_documents(loader.load())
    print(f"Dividiu os documentos em {len(chunks)} chunks.")

    # 4. Ingerir os chunks no Elasticsearch
    for i, chunk in enumerate(chunks):
        # Adicionar um sufixo para distinguir múltiplos chunks do mesmo artigo
        chunk_id = f"{article_title}_chunk_{i}"
        index_chunk(index_name="full_document_index", chunk=chunk.page_content, article_id=chunk_id, article_name=article_title, url=url),
        print(f"Indexou chunk com ID: {chunk_id}")

    print(f"Todos os chunks foram ingeridos no índice.")

def extract_website_urls():
    capes_ia_search_url = "https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html?q=intelig%C3%AAncia+artificial&source=&publishyear_min%5B%5D=1943&publishyear_max%5B%5D=2025&page="
    # extract 240 article url
    capes_ia_articles_urls = []
    for i in range(4):
        response = requests.get(capes_ia_search_url + str(i))
        if response.status_code != 200:
            raise ValueError(f"Erro ao acessar a URL: {url}")    
        soup = BeautifulSoup(response.text, "html.parser")

        # Localize o elemento <a> com a classe 'titulo-busca'
        links = soup.find_all('a', class_='titulo-busca')

        for link in links:
            url = "https://www.periodicos.capes.gov.br" + link.get('href')
            capes_ia_articles_urls.append(url)
    

    return capes_ia_articles_urls

        
# Executa o processamento e ingestão
if __name__ == "__main__":
    
    website_urls = extract_website_urls()
    print(website_urls)

    for url in website_urls:
        fetch_and_process_website_summary(url)