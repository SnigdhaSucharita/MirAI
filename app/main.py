from fastapi import FastAPI
from app.routes.semantic import router as semantic_router
from app.routes.picstoria import router as picstoria_router
from app.routes.movique import router as movique_router
from app.routes.docuvault import router as docuvault_router

app = FastAPI(title="MirAI")

@app.on_event("startup")
def warmup():
    print("MirAI service starting up...")
    
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(semantic_router)
app.include_router(picstoria_router)
app.include_router(movique_router)
app.include_router(docuvault_router)


