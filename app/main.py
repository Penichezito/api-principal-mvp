from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.db import init_db
from app.routes import auth, projects, files
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Freela Facility API",
    description="API Principal para gerenciamento de projetos freelance",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(files.router)

@app.on_event("startup")
async def startup_event():
    # Inicializa banco de dados
    init_db()

@app.get("/", include_in_schema=False)
async def root():
    # Redireciona para a documentação
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health():
    # Verifica saúde da aplicação
    return {"status": "healthy"}