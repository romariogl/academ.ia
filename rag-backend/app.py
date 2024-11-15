from flask import Flask, request, jsonify
from flask_cors import CORS
from models.elastic_search import ElasticsearchClient
from models.generate_openai import OpenAIClient

es_client = ElasticsearchClient()
openai_client = OpenAIClient()
INDEX_NAME = "documents"

app = Flask(__name__)
CORS(app)  # Permite comunicação com o frontend

@app.route("/rag", methods=["POST"])
def rag():
    """
    Endpoint para lógica de Recuperação-Augmentação-Geração.
    """
    query = request.json.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    
    orchestrator = openai_client.orchestrator(query=query)
    
    if "agent_general_search" in orchestrator:
        keywords = openai_client.generate_keywords(query=query)
        retrieved_docs = es_client.search(index_name=INDEX_NAME, query=keywords)
    elif "agent_general_search" in orchestrator:
        filename = orchestrator.split(":").strip()[0]
        retrieved_docs = es_client.search_specific(index_name=INDEX_NAME, query=query, filename=filename)         
    
    if not retrieved_docs:
        return jsonify({"error": "No relevant documents found"}), 404

    try:        
        llm_response = openai_client.generate_answer(retrieved_docs, query)
        return jsonify({
            "query": query,
            "documents": retrieved_docs,
            "answer": llm_response
        })   

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

