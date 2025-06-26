from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
def ping():
    return {"msg": "pong"}
