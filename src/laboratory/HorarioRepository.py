from config.conection import get_db
from bson.objectid import ObjectId

db = get_db()
horario_collection = db["horarios"]

class HorarioRepository:
    @staticmethod
    def create_horario(data: dict) -> str:
        """Crea un nuevo horario en la base de datos"""
        result = horario_collection.insert_one(data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_horario_by_id(horario_id: str) -> dict | None:
        """Busca un horario por su ID"""
        return horario_collection.find_one({"_id": ObjectId(horario_id)})
    
    @staticmethod
    def find_horarios_by_laboratory(lab_id: str) -> list:
        """Obtiene todos los horarios de un laboratorio específico"""
        return list(horario_collection.find({"laboratorio_id": lab_id}))
    
    @staticmethod
    def find_horarios_by_laboratory_and_day(lab_id: str, dia_semana: str) -> list:
        """Obtiene los horarios de un laboratorio para un día específico"""
        return list(horario_collection.find({
            "laboratorio_id": lab_id,
            "dia_semana": dia_semana
        }))
    
    @staticmethod
    def all_horarios() -> list:
        """Obtiene todos los horarios"""
        return list(horario_collection.find())
    
    @staticmethod
    def update_horario(horario_id: str, new_data: dict) -> bool:
        """Actualiza un horario por su ID"""
        result = horario_collection.update_one(
            {"_id": ObjectId(horario_id)}, 
            {"$set": new_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_horario(horario_id: str) -> bool:
        """Elimina un horario por su ID"""
        result = horario_collection.delete_one({"_id": ObjectId(horario_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def delete_horarios_by_laboratory(lab_id: str) -> int:
        """Elimina todos los horarios de un laboratorio específico"""
        result = horario_collection.delete_many({"laboratorio_id": lab_id})
        return result.deleted_count