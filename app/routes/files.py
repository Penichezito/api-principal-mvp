from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db, User, Project, File
from app.models.schemas import FileResponse
from app.routes.auth import get_current_user
from app.services.api_secondary import secondary_api

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    project_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"📤 Upload iniciado: {file.filename}, projeto: {project_id}")
    
    # Verifica se o projeto existe e pertence ao usuário
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        logger.error(f"❌ Projeto {project_id} não encontrado para usuário {current_user.id}")
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    logger.info(f"✅ Projeto encontrado: {project.name}")
    
    # Lê o conteúdo do arquivo
    try:
        content = await file.read()
        logger.info(f"✅ Arquivo lido: {len(content)} bytes")
    except Exception as e:
        logger.error(f"❌ Erro ao ler arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao ler arquivo: {str(e)}")

    # Envia o arquivo para API secundária para processamento
    try:
        logger.info(f"📡 Enviando para API secundária...")
        secondary_response = await secondary_api.upload_file(
            file_content=content,
            filename=file.filename or "uploaded_file",
            file_type=file.content_type or "application/octet-stream"
        )
        logger.info(f"✅ Resposta da API secundária: {secondary_response}")
    except Exception as e:
        logger.error(f"❌ Erro na API secundária: {str(e)}", exc_info=True)
        error_detail = f"Erro ao processar o arquivo: {str(e)}"
        if "timeout" in str(e).lower():
            raise HTTPException(status_code=504, detail="Timeout ao processar arquivo na API secundária")
        elif "connection" in str(e).lower():
            raise HTTPException(status_code=502, detail="Não foi possível conectar com a API secundária")
        else:
            raise HTTPException(status_code=500, detail=error_detail)
    
    # Salva informações do arquivo no banco
    try:
        logger.info(f"💾 Salvando no banco de dados...")
        new_file = File(
            filename=file.filename,
            file_path=secondary_response.get("file_path", ""),
            file_type=file.content_type or "application/octet-stream",
            size=len(content),
            project_id=project.id,
            secondary_file_id=secondary_response.get("file_id")
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        logger.info(f"✅ Arquivo salvo no banco: ID {new_file.id}")
    except Exception as e:
        logger.error(f"❌ Erro ao salvar no banco: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")

    logger.info(f"🎉 Upload concluído com sucesso!")
    return {
        "id": new_file.id,
        "filename": new_file.filename,
        "file_type": new_file.file_type,
        "size": new_file.size,
        "project_id": new_file.project_id,
        "tags": secondary_response.get("tags", []),
        "created_at": new_file.created_at
    }

@router.get("", response_model=List[FileResponse])
async def get_files(
    project_id: int | None = None, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    query = db.query(File).join(Project).filter(Project.user_id == current_user.id)

    if project_id is not None:
        query = query.filter(File.project_id == project_id)

    files = query.all()

    result = []
    for file in files:
        # Busca tags do arquivo na API secundária
        tags = []
        if file.secondary_file_id:
            try:
                tag_response = await secondary_api.get_file_tags(file.secondary_file_id)
                tags = tag_response.get("tags", [])
            except:
                tags = []
        
        result.append({
            "id": file.id,
            "filename": file.filename,
            "file_type": file.file_type,
            "size": file.size,
            "project_id": file.project_id,
            "tags": tags,
            "created_at": file.created_at
        })
    
    return result

@router.get("/search")
async def search_files(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    # Busca nos nomes de arquivos
    files = db.query(File).join(Project).filter(
        Project.user_id == current_user.id,
        File.filename.ilike(f"%{q}%")
    ).all()

    result = []
    for file in files:
        tags = []
        if file.secondary_file_id:
            try:
                tag_response = await secondary_api.get_file_tags(file.secondary_file_id)
                tags = tag_response.get("tags", [])
            except:
                tags = []
        
        result.append({
            "id": file.id,
            "filename": file.filename,
            "file_type": file.file_type,
            "size": file.size,
            "project_id": file.project_id,
            "tags": tags,
            "created_at": file.created_at
        })
    
    return result

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).join(Project).filter(
        File.id == file_id,
        Project.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    db.delete(file)
    db.commit()

    return {"detail": "Arquivo deletado com sucesso"}
























