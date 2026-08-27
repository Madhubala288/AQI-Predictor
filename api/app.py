from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AQI Predictor API Successfully Running!"}

# Baad mein aap apna Machine Learning model yahan load karke /predict endpoint bana sakti hain
