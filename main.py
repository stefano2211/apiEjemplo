import os
import time
from datetime import datetime
from typing import List, Union, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/industrial_db")

# Intentar reconectar si la DB no está lista (útil en Docker Compose)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO ORM ---
class MeasurementORM(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(255), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Text)  # Guardamos como texto para soportar float, int, str
    quality = Column(String(50))
    status = Column(String(50), default="N/A")
    category = Column(String(100), default="N/A")
    department = Column(String(100)) # Maquinaria, Manufactura, MedioAmbiente

# --- ESQUEMAS PYDANTIC ---
class DataPoint(BaseModel):
    TagName: str
    Timestamp: datetime
    Value: Union[float, int, str]
    Quality: str
    Status: str = "N/A"
    Category: str = "N/A"

    class Config:
        from_attributes = True

# --- DEPENDENCIAS ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- DATOS INICIALES PARA SEEDING ---
initial_data = {
    "Maquinaria": [
        {"TagName": "Maquinaria.Motor1.Temperatura", "Timestamp": "2025-06-01T08:00:00Z", "Value": 75.5, "Quality": "Good", "Status": "Running", "Category": "Thermal"},
        {"TagName": "Maquinaria.Motor1.Vibracion", "Timestamp": "2025-06-01T08:05:00Z", "Value": 0.05, "Quality": "Good", "Status": "Running", "Category": "Mechanical"},
        {"TagName": "Maquinaria.BombaA.Presion", "Timestamp": "2025-06-01T08:10:00Z", "Value": 120.2, "Quality": "Good", "Status": "Running", "Category": "Hydraulic"},
    ],
    "Manufactura": [
        {"TagName": "Manufactura.LineaA.ProduccionHora", "Timestamp": "2025-06-01T10:00:00Z", "Value": 350, "Quality": "Good", "Status": "Optimal", "Category": "KPI"},
        {"TagName": "Manufactura.LineaA.Defectos", "Timestamp": "2025-06-01T10:05:00Z", "Value": 5, "Quality": "Warning", "Status": "Review", "Category": "QualityControl"},
    ],
    "MedioAmbiente": [
        {"TagName": "MedioAmbiente.Zona1.Temperatura", "Timestamp": "2025-06-01T12:00:00Z", "Value": 24.5, "Quality": "Good", "Status": "Normal", "Category": "Climate"},
        {"TagName": "MedioAmbiente.Zona1.Humedad", "Timestamp": "2025-06-01T12:05:00Z", "Value": 45.0, "Quality": "Good", "Status": "Normal", "Category": "Climate"},
    ]
}

def seed_db(db: Session):
    count = db.query(MeasurementORM).count()
    if count == 0:
        print("🌱 Seeding database with initial simulation data...")
        for dept, points in initial_data.items():
            for p in points:
                db_item = MeasurementORM(
                    tag_name=p["TagName"],
                    timestamp=datetime.fromisoformat(p["Timestamp"].replace("Z", "+00:00")),
                    value=str(p["Value"]),
                    quality=p["Quality"],
                    status=p["Status"],
                    category=p["Category"],
                    department=dept
                )
                db.add(db_item)
        db.commit()
        print("✅ Seeding complete.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Intentar conexión con reintentos para esperar a Postgres
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            db = SessionLocal()
            seed_db(db)
            db.close()
            print("🚀 Database initialized successfully.")
            break
        except OperationalError:
            retries -= 1
            print(f"⌛ Waiting for database... ({retries} retries left)")
            time.sleep(2)
    yield

app = FastAPI(title="API Industrial de Simulación (SQL Enabled)", version="2.0.0", lifespan=lifespan)

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API Industrial con persistencia SQL",
        "database": "PostgreSQL",
        "endpoints_disponibles": {
            "maquinaria": ["GET /api/v1/maquinaria", "POST /api/v1/maquinaria"],
            "manufactura": ["GET /api/v1/manufactura", "POST /api/v1/manufactura"],
            "medio_ambiente": ["GET /api/v1/medio-ambiente", "POST /api/v1/medio-ambiente"]
        }
    }

def get_dept_data(dept: str, db: Session):
    items = db.query(MeasurementORM).filter(MeasurementORM.department == dept).all()
    # Convertir a formato Pydantic para la respuesta
    return [
        {
            "TagName": item.tag_name,
            "Timestamp": item.timestamp,
            "Value": item.value, # Devolvemos como string para ser seguros, o podrías intentar castear
            "Quality": item.quality,
            "Status": item.status,
            "Category": item.category
        } for item in items
    ]

def add_dept_data(dept: str, data: Union[List[DataPoint], DataPoint], db: Session):
    points = data if isinstance(data, list) else [data]
    for p in points:
        new_item = MeasurementORM(
            tag_name=p.TagName,
            timestamp=p.Timestamp,
            value=str(p.Value),
            quality=p.Quality,
            status=p.Status,
            category=p.Category,
            department=dept
        )
        db.add(new_item)
    db.commit()
    return {"message": f"Se han añadido {len(points)} registros a {dept} exitosamente en la DB"}

@app.get("/api/v1/maquinaria")
def get_machinery_data(db: Session = Depends(get_db)):
    return get_dept_data("Maquinaria", db)

@app.post("/api/v1/maquinaria", status_code=201)
def add_machinery_data(data: Union[List[DataPoint], DataPoint], db: Session = Depends(get_db)):
    return add_dept_data("Maquinaria", data, db)

@app.get("/api/v1/manufactura")
def get_manufacturing_data(db: Session = Depends(get_db)):
    return get_dept_data("Manufactura", db)

@app.post("/api/v1/manufactura", status_code=201)
def add_manufacturing_data(data: Union[List[DataPoint], DataPoint], db: Session = Depends(get_db)):
    return add_dept_data("Manufactura", data, db)

@app.get("/api/v1/medio-ambiente")
def get_environment_data(db: Session = Depends(get_db)):
    return get_dept_data("MedioAmbiente", db)

@app.post("/api/v1/medio-ambiente", status_code=201)
def add_environment_data(data: Union[List[DataPoint], DataPoint], db: Session = Depends(get_db)):
    return add_dept_data("MedioAmbiente", data, db)
