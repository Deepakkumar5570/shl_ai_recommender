from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://shl-ai-recommender.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# ROUTES
# =========================

app.include_router(router)