from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.routes.pokemon_route import pokemon_router


load_dotenv(".env")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemon_router, tags=["POKEMON ROUTES"])

@app.get("/")
async def root():
    return {"message": "Hello from home"}

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        port=5001
    )
