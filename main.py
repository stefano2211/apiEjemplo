from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="API Industrial de Simulación", version="1.0.0")

class DataPoint(BaseModel):
    TagName: str
    Timestamp: datetime
    Value: Union[float, int, str]
    Quality: str
    Status: str = "N/A" # Categorical
    Category: str = "N/A" # Categorical

# 15 Ejemplos para Maquinaria
machinery_data = [
    {"TagName": "Maquinaria.Motor1.Temperatura", "Timestamp": "2025-06-01T08:00:00Z", "Value": 75.5, "Quality": "Good", "Status": "Running", "Category": "Thermal"},
    {"TagName": "Maquinaria.Motor1.Vibracion", "Timestamp": "2025-06-01T08:05:00Z", "Value": 0.05, "Quality": "Good", "Status": "Running", "Category": "Mechanical"},
    {"TagName": "Maquinaria.BombaA.Presion", "Timestamp": "2025-06-01T08:10:00Z", "Value": 120.2, "Quality": "Good", "Status": "Running", "Category": "Hydraulic"},
    {"TagName": "Maquinaria.BombaA.Caudal", "Timestamp": "2025-06-01T08:15:00Z", "Value": 45.0, "Quality": "Uncertain", "Status": "Running", "Category": "Hydraulic"},
    {"TagName": "Maquinaria.Compresor1.Estado", "Timestamp": "2025-06-01T08:20:00Z", "Value": "Activo", "Quality": "Good", "Status": "Running", "Category": "Operational"},
    {"TagName": "Maquinaria.Compresor1.ConsumoEnergia", "Timestamp": "2025-06-01T08:25:00Z", "Value": 350.5, "Quality": "Good", "Status": "Running", "Category": "Electrical"},
    {"TagName": "Maquinaria.CintaTransportadora.Velocidad", "Timestamp": "2025-06-01T08:30:00Z", "Value": 2.5, "Quality": "Good", "Status": "Running", "Category": "Mechanical"},
    {"TagName": "Maquinaria.CintaTransportadora.Carga", "Timestamp": "2025-06-01T08:35:00Z", "Value": 500.0, "Quality": "Good", "Status": "Running", "Category": "Mechanical"},
    {"TagName": "Maquinaria.RobotEnsamblaje.Ciclos", "Timestamp": "2025-06-01T08:40:00Z", "Value": 150, "Quality": "Good", "Status": "Running", "Category": "Production"},
    {"TagName": "Maquinaria.RobotEnsamblaje.Errores", "Timestamp": "2025-06-01T08:45:00Z", "Value": 2, "Quality": "Bad", "Status": "Maintenance_Req", "Category": "Production"},
    {"TagName": "Maquinaria.HornoFundicion.Temp1", "Timestamp": "2025-06-01T08:50:00Z", "Value": 1450.0, "Quality": "Good", "Status": "Heating", "Category": "Thermal"},
    {"TagName": "Maquinaria.HornoFundicion.Temp2", "Timestamp": "2025-06-01T08:55:00Z", "Value": 1445.5, "Quality": "Good", "Status": "Heating", "Category": "Thermal"},
    {"TagName": "Maquinaria.HornoFundicion.GasLevel", "Timestamp": "2025-06-01T09:00:00Z", "Value": 80.0, "Quality": "Good", "Status": "Heating", "Category": "Chemical"},
    {"TagName": "Maquinaria.TornoCNC.RPM", "Timestamp": "2025-06-01T09:05:00Z", "Value": 3000, "Quality": "Good", "Status": "Running", "Category": "Mechanical"},
    {"TagName": "Maquinaria.TornoCNC.DesgasteHerramienta", "Timestamp": "2025-06-01T09:10:00Z", "Value": 15.2, "Quality": "Warning", "Status": "Running", "Category": "Maintenance"},
]

# 15 Ejemplos para Manufactura / Producción
manufacturing_data = [
    {"TagName": "Manufactura.LineaA.ProduccionHora", "Timestamp": "2025-06-01T10:00:00Z", "Value": 350, "Quality": "Good", "Status": "Optimal", "Category": "KPI"},
    {"TagName": "Manufactura.LineaA.Defectos", "Timestamp": "2025-06-01T10:05:00Z", "Value": 5, "Quality": "Warning", "Status": "Review", "Category": "QualityControl"},
    {"TagName": "Manufactura.LineaA.Turno", "Timestamp": "2025-06-01T10:10:00Z", "Value": "Mañana", "Quality": "Good", "Status": "Active", "Category": "HR"},
    {"TagName": "Manufactura.LineaB.ProduccionHora", "Timestamp": "2025-06-01T10:15:00Z", "Value": 420, "Quality": "Good", "Status": "Optimal", "Category": "KPI"},
    {"TagName": "Manufactura.LineaB.Defectos", "Timestamp": "2025-06-01T10:20:00Z", "Value": 12, "Quality": "Bad", "Status": "Action_Required", "Category": "QualityControl"},
    {"TagName": "Manufactura.LineaB.Turno", "Timestamp": "2025-06-01T10:25:00Z", "Value": "Mañana", "Quality": "Good", "Status": "Active", "Category": "HR"},
    {"TagName": "Manufactura.Empaquetado.CajasSelladas", "Timestamp": "2025-06-01T10:30:00Z", "Value": 1500, "Quality": "Good", "Status": "Optimal", "Category": "Logistics"},
    {"TagName": "Manufactura.Empaquetado.MaterialFaltante", "Timestamp": "2025-06-01T10:35:00Z", "Value": "Carton", "Quality": "Warning", "Status": "Low_Stock", "Category": "Inventory"},
    {"TagName": "Manufactura.Calidad.MuestraAleatoria", "Timestamp": "2025-06-01T10:40:00Z", "Value": "Aprobado", "Quality": "Good", "Status": "Tested", "Category": "QualityControl"},
    {"TagName": "Manufactura.Ensamblaje.TiempoCiclo", "Timestamp": "2025-06-01T10:45:00Z", "Value": 45.5, "Quality": "Good", "Status": "Normal", "Category": "Efficiency"},
    {"TagName": "Manufactura.Ensamblaje.EficienciaOEE", "Timestamp": "2025-06-01T10:50:00Z", "Value": 85.2, "Quality": "Good", "Status": "On_Target", "Category": "KPI"},
    {"TagName": "Manufactura.Pintura.GrosorCapa", "Timestamp": "2025-06-01T10:55:00Z", "Value": 1.2, "Quality": "Good", "Status": "Normal", "Category": "QualityControl"},
    {"TagName": "Manufactura.Pintura.Color", "Timestamp": "2025-06-01T11:00:00Z", "Value": "Rojo_Industrial", "Quality": "Good", "Status": "Active", "Category": "Configuration"},
    {"TagName": "Manufactura.Logistica.PalletsTerminados", "Timestamp": "2025-06-01T11:05:00Z", "Value": 45, "Quality": "Good", "Status": "Ready", "Category": "Logistics"},
    {"TagName": "Manufactura.Logistica.CamionesCargando", "Timestamp": "2025-06-01T11:10:00Z", "Value": 2, "Quality": "Good", "Status": "In_Progress", "Category": "Logistics"},
]

# 15 Ejemplos para Sensores y Medio Ambiente Industrial
environment_data = [
    {"TagName": "MedioAmbiente.Zona1.Temperatura", "Timestamp": "2025-06-01T12:00:00Z", "Value": 24.5, "Quality": "Good", "Status": "Normal", "Category": "Climate"},
    {"TagName": "MedioAmbiente.Zona1.Humedad", "Timestamp": "2025-06-01T12:05:00Z", "Value": 45.0, "Quality": "Good", "Status": "Normal", "Category": "Climate"},
    {"TagName": "MedioAmbiente.Zona1.CalidadAire_AQI", "Timestamp": "2025-06-01T12:10:00Z", "Value": 42, "Quality": "Good", "Status": "Healthy", "Category": "Safety"},
    {"TagName": "MedioAmbiente.Soldadura.NivelCO2", "Timestamp": "2025-06-01T12:15:00Z", "Value": 850.0, "Quality": "Warning", "Status": "Elevated", "Category": "Safety"},
    {"TagName": "MedioAmbiente.Soldadura.ExtraccionAvanzada", "Timestamp": "2025-06-01T12:20:00Z", "Value": "Encendido", "Quality": "Good", "Status": "Active", "Category": "HVAC"},
    {"TagName": "MedioAmbiente.PlantaAgua.PhNivel", "Timestamp": "2025-06-01T12:25:00Z", "Value": 7.2, "Quality": "Good", "Status": "Normal", "Category": "WaterTreatment"},
    {"TagName": "MedioAmbiente.PlantaAgua.Turbidez", "Timestamp": "2025-06-01T12:30:00Z", "Value": 1.5, "Quality": "Good", "Status": "Normal", "Category": "WaterTreatment"},
    {"TagName": "MedioAmbiente.PlantaAgua.BombaFiltro", "Timestamp": "2025-06-01T12:35:00Z", "Value": "Apagado", "Quality": "Good", "Status": "Standby", "Category": "HVAC"},
    {"TagName": "MedioAmbiente.Exterior.Temperatura", "Timestamp": "2025-06-01T12:40:00Z", "Value": 30.5, "Quality": "Good", "Status": "Sunny", "Category": "Weather"},
    {"TagName": "MedioAmbiente.Exterior.VelocidadViento", "Timestamp": "2025-06-01T12:45:00Z", "Value": 12.5, "Quality": "Good", "Status": "Breezy", "Category": "Weather"},
    {"TagName": "MedioAmbiente.Generador.Ruido_dB", "Timestamp": "2025-06-01T12:50:00Z", "Value": 85.0, "Quality": "Warning", "Status": "Loud", "Category": "Safety"},
    {"TagName": "MedioAmbiente.Almacen.Iluminacion", "Timestamp": "2025-06-01T12:55:00Z", "Value": "Eco_Mode", "Quality": "Good", "Status": "EnergySaving", "Category": "Lighting"},
    {"TagName": "MedioAmbiente.Almacen.Presencia", "Timestamp": "2025-06-01T13:00:00Z", "Value": "Detectado", "Quality": "Good", "Status": "Occupied", "Category": "Security"},
    {"TagName": "MedioAmbiente.Oficinas.HVAC_Modo", "Timestamp": "2025-06-01T13:05:00Z", "Value": "Auto", "Quality": "Good", "Status": "Active", "Category": "HVAC"},
    {"TagName": "MedioAmbiente.Oficinas.ConsumoElectrico", "Timestamp": "2025-06-01T13:10:00Z", "Value": 45.2, "Quality": "Good", "Status": "Normal", "Category": "Energy"},
]

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API Industrial",
        "endpoints_disponibles": {
            "maquinaria": ["GET /api/v1/maquinaria", "POST /api/v1/maquinaria"],
            "manufactura": ["GET /api/v1/manufactura", "POST /api/v1/manufactura"],
            "medio_ambiente": ["GET /api/v1/medio-ambiente", "POST /api/v1/medio-ambiente"]
        }
    }

@app.get("/api/v1/maquinaria", response_model=List[DataPoint])
def get_machinery_data():
    return machinery_data

@app.post("/api/v1/maquinaria", response_model=dict, status_code=201)
def add_machinery_data(data: Union[List[DataPoint], DataPoint]):
    if isinstance(data, list):
        machinery_data.extend(data)
        return {"message": f"Se han añadido {len(data)} registros a Maquinaria exitosamente"}
    else:
        machinery_data.append(data)
        return {"message": "Se ha añadido 1 registro a Maquinaria exitosamente"}

@app.get("/api/v1/manufactura", response_model=List[DataPoint])
def get_manufacturing_data():
    return manufacturing_data

@app.post("/api/v1/manufactura", response_model=dict, status_code=201)
def add_manufacturing_data(data: Union[List[DataPoint], DataPoint]):
    if isinstance(data, list):
        manufacturing_data.extend(data)
        return {"message": f"Se han añadido {len(data)} registros a Manufactura exitosamente"}
    else:
        manufacturing_data.append(data)
        return {"message": "Se ha añadido 1 registro a Manufactura exitosamente"}

@app.get("/api/v1/medio-ambiente", response_model=List[DataPoint])
def get_environment_data():
    return environment_data

@app.post("/api/v1/medio-ambiente", response_model=dict, status_code=201)
def add_environment_data(data: Union[List[DataPoint], DataPoint]):
    if isinstance(data, list):
        environment_data.extend(data)
        return {"message": f"Se han añadido {len(data)} registros a Medio Ambiente exitosamente"}
    else:
        environment_data.append(data)
        return {"message": "Se ha añadido 1 registro a Medio Ambiente exitosamente"}
