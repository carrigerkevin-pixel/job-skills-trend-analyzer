from fastapi import FastAPI

app = FastAPI(title="Job Skills Trend Analyzer API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Skills Trend Analyzer API"}