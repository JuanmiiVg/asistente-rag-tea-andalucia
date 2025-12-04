from services.agent_service import SimpleAgent
from pathlib import Path


class MockRAG:
    def query(self, question: str):
        return {"respuesta": "Respuesta simulada", "fuentes": ["doc1.pdf"]}


def main():
    mock = MockRAG()
    agent = SimpleAgent(rag_service=mock)
    res = agent.perform_task("Generar solicitud de ejemplo para prueba", usuario_id="test_user")
    print(res)
    print("Carpeta data/solicitudes existe?", (Path("data") / "solicitudes").exists())


if __name__ == '__main__':
    main()
