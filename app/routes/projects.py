from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from typing import List

from app.database.db import get_db, User, Project
from app.models.schemas import ProjectCreate, ProjectResponse
from app.routes.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    # Cria um novo projeto para o usuário autenticado
    new_project = Project(
        name=project.name,
        client_name=project.client_name,
        description=project.description,
        user_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Adiciona contagem de arquivos
    project_dict = {
    "id": new_project.id,
    "name": new_project.name,
    "client_name": new_project.client_name,
    "description": new_project.description,
    "user_id": new_project.user_id,
    "created_at": new_project.created_at,
    "file_count": 0
    }

    return project_dict

@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()

    # adiciona contagem de arquivos para cada projeto
    result = []
    for project in projects:
        project_dict = {
            "id": project.id,
            "name": project.name, 
            "client_name": project.client_name,
            "description": project.description,
            "user_id": project.user_id,
            "created_at": project.created_at,
            "file_count": len(project.files)  # Supondo que haja um relacionamento 'files'
        }
        result.append(project_dict)
    
    return result

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project (
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    project_dict = {
        "id": project.id,
        "name": project.name,
        "client_name": project.client_name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
        "file_count": len(project.files) # Supondo que haja um relacionamento 'files'
    }

    return project_dict

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    project.name = project_update.name
    project.client_name = project_update.client_name
    project.description = project_update.description

    db.commit()
    db.refresh(project)

    project_dict = {
        "id": project.id,
        "name": project.name,
        "client_name": project.client_name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
        "file_count": len(project.files)
    }

    return project_dict

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    db.delete(project)
    db.commit()
    
    return {"message": "Projeto excluído com sucesso"}





















