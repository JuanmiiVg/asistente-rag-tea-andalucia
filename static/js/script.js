document.addEventListener('DOMContentLoaded', () => {
    const queryForm = document.getElementById('query-form');
    const questionInput = document.getElementById('question-input');
    const submitBtn = document.getElementById('submit-btn');
    const resultsSection = document.getElementById('results-section');
    const answerText = document.getElementById('answer-text');
    const sourcesList = document.getElementById('sources-list');
    const historySection = document.getElementById('history-section');
    const historyList = document.getElementById('history-list');

    let sessionHistory = [];

    // -------------------------------
    // Consulta RAG
    // -------------------------------
    queryForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const question = questionInput.value.trim();
        if (!question) return;

        setLoading(true);
        resultsSection.style.display = "none";

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pregunta: question }),
            });

            const data = await response.json();
            answerText.textContent = data.respuesta;

            sourcesList.innerHTML = "";
            data.fuentes?.forEach(src => {
                const li = document.createElement('li');
                li.textContent = src.documento;
                sourcesList.appendChild(li);
            });

            resultsSection.style.display = "block";
            addToHistory(question, data.respuesta);

        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.classList.toggle("loading", isLoading);
    }

    // -------------------------------
    // Historial de sesión
    // -------------------------------
    function addToHistory(question, answer) {
        sessionHistory.unshift({ question, answer });
        if (sessionHistory.length > 5) sessionHistory.pop();
        renderHistory();
    }

    function renderHistory() {
        historyList.innerHTML = "";
        sessionHistory.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <div class="history-question">${item.question}</div>
                <div class="history-answer">${item.answer}</div>
            `;
            historyList.appendChild(div);
        });
        historySection.style.display = "block";
    }

    // -------------------------------
    // MODAL HISTORIAL COMPLETO
    // -------------------------------
    const btnHistorial = document.getElementById("btnHistorial");
    const modal = document.getElementById("modalHistorial");
    const modalContent = document.querySelector(".modal-content");
    const cerrarModal = document.getElementById("cerrarModal");
    const historialContent = document.getElementById("historialContent");

    btnHistorial.onclick = async () => {
        const res = await fetch("/api/historial?usuario_id=usuario_juan");
        const data = await res.json();

        historialContent.innerHTML = "";

        data.conversaciones?.forEach(item => {
            historialContent.innerHTML += `
                <div class="history-item">
                    <p><strong>Usuario:</strong> ${item.usuario}</p>
                    <p><strong>Asistente:</strong> ${item.agente}</p>
                </div>
            `;
        });

        modal.classList.remove("hidden");
        document.body.style.overflow = "hidden";
    };

    // 🔥 Cerrar modal (FUNCIONA 100%)
    cerrarModal.onclick = () => {
        modal.classList.add("hidden");
        document.body.style.overflow = "";
    };

    // Cerrar al hacer clic fuera del contenido
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.add("hidden");
            document.body.style.overflow = "";
        }
    };

    // Evitar cierre cuando clic en contenido
    modalContent.onclick = (e) => e.stopPropagation();
});
