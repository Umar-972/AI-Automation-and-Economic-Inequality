from fastapi import FastAPI
app=FastAPI(title="QuantChronicle")

@app.get("/")
def root():
    return {"name":"QuantChronicle","status":"running"}
