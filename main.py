from fastapi import FastAPI
from routers import medicines, sales

app = FastAPI(title="Аптека")

app.include_router(medicines.router)
app.include_router(sales.router)

@app.get("/")
def root():
    return {"message": "Сервер запущен"}
