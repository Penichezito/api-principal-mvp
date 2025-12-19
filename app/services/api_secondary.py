import httpx
from app.config import settings

class SecondaryAPIService:
    """Serviço para interagir com a API secundária"""
    def __init__(self) -> None:
        self.base_url = settings.SECONDARY_API_URL

    async def upload_file(self, file_content: bytes, filename: str, file_type: str):
        """ Envia arquivo para a API secundária para processamento"""
        async with httpx.AsyncClient(timeout=120.0) as client:  # 2 minutos para imagens grandes
            files = {"file": (filename, file_content, file_type)}
            response = await client.post(f"{self.base_url}/api/files/process", files=files) 
            response.raise_for_status()
            return response.json()

    async def get_file_tags(self, file_id: int):
        """Busca tags de um arquivo na API secundária"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/files/{file_id}/tags")
            response.raise_for_status()
            return response.json()
    
    async def search_by_tags(self, tags: list):
        """Busca arquivos por tags na API secundária"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/files/search",
                json={"tags": tags}
            )
            response.raise_for_status()
            return response.json()

secondary_api = SecondaryAPIService()
            