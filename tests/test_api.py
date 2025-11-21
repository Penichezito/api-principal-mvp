"""
Exemplo de testes unitários com pytest
Instale com: pip install pytest pytest-asyncio httpx
Rode com: pytest -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Cliente de teste
client = TestClient(app)


class TestHealthEndpoints:
    """Testes dos endpoints de health"""
    
    def test_health_check(self):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "online"


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_404_not_found(self):
        """Testa erro 404"""
        response = client.get("/api/endpoint-inexistente")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Testa erro 405"""
        response = client.post("/health")  # Health deve ser GET
        assert response.status_code == 405
    
    def test_invalid_json(self):
        """Testa erro com JSON inválido"""
        response = client.post(
            "/auth/login",
            json={"email": "invalido", "password": "123"}  # Email inválido
        )
        # Deve retornar erro de validação ou falha de autenticação
        assert response.status_code in [422, 401, 400]


class TestValidation:
    """Testes de validação de entrada"""
    
    def test_missing_required_field(self):
        """Testa campo obrigatório faltando"""
        response = client.post(
            "/auth/login",
            json={"email": "user@example.com"}  # Falta password
        )
        assert response.status_code in [422, 400]
    
    def test_empty_fields(self):
        """Testa campos vazios"""
        response = client.post(
            "/auth/login",
            json={"email": "", "password": ""}
        )
        assert response.status_code in [422, 400]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

