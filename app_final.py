from fastapi import FastAPI, HTTPException

app = FastAPI(title="Calculator", version="1.0.0")

@app.get("/")
def root():
    return {"service": "Calculator", "operations": list()}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"name": "Calculator", "version": "1.0.0"}
