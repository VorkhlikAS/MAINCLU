from fastapi import FastAPI

app = FastAPI()

@app.get("/SCORE/GET")
async def root():
    return {"score": 100}
