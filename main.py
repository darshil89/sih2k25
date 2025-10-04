from fastapi import FastAPI
import uvicorn

port = 8080

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=port, reload=True)