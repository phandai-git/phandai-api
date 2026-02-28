from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth,
    businesses,
    bots,
    contacts,
    conversations,
    analytics,
    billing,
)

app = FastAPI(
    title="Phandai API",
    description="AI chatbot and workflow automation platform for South African small businesses",
    version="0.1.0",
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://dashboard.phand.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──
app.include_router(auth.router, prefix="/api/v1")
app.include_router(businesses.router, prefix="/api/v1")
app.include_router(bots.router, prefix="/api/v1")
app.include_router(contacts.router, prefix="/api/v1")
app.include_router(conversations.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "phandai-api"}
