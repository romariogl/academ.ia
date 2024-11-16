from flask import Flask, request, jsonify
from flask_cors import CORS
from models.elastic_search import ElasticsearchClient
from models.generate_gemini import GeminiClient
import json

es_client = ElasticsearchClient()
gemini_client = GeminiClient()

app = Flask(__name__)
CORS(app)  # Permite comunicação com o frontend


def document_retrieval(query):
    orchestrator = gemini_client.orchestrator(query=query)
    print(orchestrator)
    if "agent_general_search" in orchestrator:
        keywords = gemini_client.generate_keywords(query=query)
        retrieved_docs = es_client.search(index_name='summary_index', query=keywords)        
    elif "agent_specific_search" in orchestrator:
        filename = orchestrator.split(":")[-1].strip()
        query = query.replace(filename, "")
        print(f"Pesquisa específica no artigo: {filename}, procurando: {query}")
        retrieved_docs = es_client.search_specific(index_name="full_document_index", query=query, filename=filename)

    return retrieved_docs

def get_llm_response(retrieved_docs, query):
    answer = ''
    llm_response = gemini_client.generate_answer(retrieved_docs, query)
    start_index = llm_response.find('{')
    end_index = llm_response.rfind('}')
    if start_index != -1 and end_index != -1:
        dict_str = llm_response[start_index:end_index+1]
        dict_str = dict_str.encode('utf-8').decode('unicode_escape')
        print(dict_str)
        llm_response = json.loads(dict_str)        
        
    else:
        llm_response = json.loads(llm_response)
            
    print(llm_response)
    for k, v in llm_response.items():
        k = "<strong>" + k.encode('latin1').decode('utf-8') + "</strong>"
        v = v.encode('latin1').decode('utf-8') + "<br /><br />"
        answer += k + ": " + v

    print(answer)
    return answer

@app.route("/rag", methods=["POST"])
def rag():
    """
    Endpoint para lógica de Recuperação-Augmentação-Geração.
    """
    query = request.json.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400


    retrieved_docs = document_retrieval(query=query)

    if not retrieved_docs:
        return jsonify({"error": "No relevant documents found"}), 404
    
    answer = get_llm_response(retrieved_docs=retrieved_docs, query=query)

    try:
        return jsonify({
            "query": query,
            "documents": retrieved_docs,
            "answer": answer
        })   

    except Exception as e:
        print(f"Error {e}") 
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

