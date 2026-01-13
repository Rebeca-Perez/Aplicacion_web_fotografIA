import requests

BASE_URL = "http://localhost:5000"

def test_query_endpoint():
    response = requests.post(
        f"{BASE_URL}/query",
        json={"pregunta": "¿Qué es la fotografía macro?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "respuesta" in data
    assert isinstance(data["respuesta"], str)

def test_historial_endpoint():
    response = requests.get(f"{BASE_URL}/historial")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "pregunta" in data[0]
        assert "respuesta" in data[0]
        assert "fecha" in data[0]
