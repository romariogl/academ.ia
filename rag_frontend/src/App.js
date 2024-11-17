import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const BACKEND_URL = "http://127.0.0.1:5000"; // URL do seu backend Flask
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Mensagem de instruções iniciais
    const initialMessage = {
      sender: "bot",
      text: `
      <p><strong>Bem-vindo!</strong> Eu sou a <strong>Academ.ia</strong>. Atualmente sou um protótipo de agente capaz de responder principalmente sobre artigos de inteligência artificial do CAPES.</p>
      <p>Posso te ajudar com perguntas gerais:</p>
      <ul>
        <li><strong>Exemplo 1:</strong> Quais são os artigos sobre Inteligência Artificial?</li>
        <li><strong>Exemplo 2:</strong> Quais artigos falam sobre medicina?</li>
        <li><strong>Exemplo 3:</strong> Quais artigos falam sobre educação?.</li>
      </ul>
      <p>Ou te ajudar com perguntas específicas de algum artigo que encontrou:</p>
      <ul>
        <li><strong>Exemplo 1:</strong> no artigo "Problemas bioéticos emergentes de la inteligencia artificial" quais as principais conclusões do autor?</li>
      </ul>
      <p>No momento ainda estamos em construção!</p>
      <p>Sinta-se à vontade para começar!</p>      
      `,
    };
    setMessages([initialMessage]);
  }, []);
  
  
  const handleSend = async () => {
    if (input.trim()) {
      // Adiciona a mensagem do usuário
      setMessages([...messages, { sender: "user", text: input }]);
      const userInput = input; // Salva a mensagem do usuário para exibir depois
      setInput("");

      try {
        // Faz a requisição para a rota /rag
        const response = await axios.post(`${BACKEND_URL}/rag`, { query: userInput });

        // Adiciona a resposta do backend (bot)
        const botResponse = response.data.answer || "Erro ao gerar resposta";
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: botResponse },
        ]);
      } catch (error) {
        console.error("Erro ao se conectar com o backend:", error);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "Erro ao obter a resposta. Tente novamente." },
        ]);
      }
    }
  };

  // Rola automaticamente para a mensagem mais recente
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="container mt-4" style={{Width: "70vw" }}>
      {/* Chat Header */}
      <div className="card shadow rounded">
        <div className="card-header d-flex align-items-center justify-content-between text-black rounded-top" style={{backgroundColor: "#f8f9fa" }}>
          <img src="/logocapes.png" alt="Logo" style={{ height: "10px", marginRight: "10px", position: "absolute", left: "10px" }}/>
          <h5 className="mb-0 w-100 text-center">Academ.ia</h5>
        </div>

        {/* Chat Body */}
        <div
          className="card-body"
          style={{
            height: "70vh",
            overflowY: "auto",
            backgroundColor: "#ffffff",
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`d-flex ${msg.sender === "user"
                  ? "justify-content-end"
                  : "justify-content-start"
                } mb-3`}
            >
              <div
                className={`p-3 rounded shadow-sm ${msg.sender === "user"
                    ? "bg-primary text-white"
                    : "bg-light text-dark"
                  }`}
                style={{
                  maxWidth: "75%",
                  transition: "all 0.3s ease-in-out",
                }}
              >                
                {msg.sender === "user" ? (msg.text) : (<div dangerouslySetInnerHTML={{ __html: msg.text }} />)} 
              </div>
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        {/* Chat Footer */}
        <div className="card-footer">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Digite sua pergunta..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              className="btn btn-primary"
              type="button"
              onClick={handleSend}
            >
              <i className="bi bi-send-fill"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatApp;