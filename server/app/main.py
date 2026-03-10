from fastapi import FastAPI

app = FastAPI(title="ShiftPilot API")


@app.get("/health")
def health_check():
    return {"status": "ok"}