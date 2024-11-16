from flask import Flask, request, jsonify
from flask_cors import CORS
from models.elastic_search import ElasticsearchClient
from models.generate_gemini import GeminiClient
import json

es_client = ElasticsearchClient()
gemini_client = GeminiClient()
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

    print(query)
    orchestrator = gemini_client.orchestrator(query=query)
    print(orchestrator)

    if "agent_general_search" in orchestrator:
        keywords = gemini_client.generate_keywords(query=query)
        print(keywords)
        retrieved_docs = es_client.search(index_name=INDEX_NAME, query=keywords)        
    elif "agent_specific_search" in orchestrator:
        filename = orchestrator.split(":").strip()[0]
        print(filename)
        retrieved_docs = es_client.search_specific(index_name=INDEX_NAME, query=query, filename=filename)         
    
    print("Quantidade de docs encontrados: ", len(retrieved_docs))

    if not retrieved_docs:
        return jsonify({"error": "No relevant documents found"}), 404

    try:
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

