from laboratory.LaboratoryRepository import LaboratorioRepository
from laboratory.HorarioRepository import HorarioRepository
from datetime import datetime
import re

class LaboratorioController:
    def __init__(self):
        self.lab_repo = LaboratorioRepository
        self.horario_repo = HorarioRepository
    
    # --- CRUD Laboratorios ---
    
    def create_laboratorio(self, nombre, ubicacion, capacidad, equipamiento, estado='activo'):
        """Crea un nuevo laboratorio"""
        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                return None
        except ValueError:
            return None
            
        data = {
            "nombre": nombre,
            "ubicacion": ubicacion,
            "capacidad": capacidad,
            "equipamiento": equipamiento,
            "estado": estado
        }
        
        return self.lab_repo.create_laboratory(data)
    
    def get_all_laboratorios(self):
        """Obtiene todos los laboratorios con ID como string"""
        labs = self.lab_repo.all_laboratory()
        # Convertir ObjectId a string para facilitar el manejo en la GUI
        for lab in labs:
            lab["id"] = str(lab["_id"])
            del lab["_id"]
        return labs
    
    def get_laboratorio_by_id(self, lab_id):
        """Obtiene un laboratorio por su ID"""
        lab = self.lab_repo.find_laboratory_by_id(lab_id)
        if lab:
            lab["id"] = str(lab["_id"])
            del lab["_id"]
        return lab
    
    def update_laboratorio(self, lab_id, nombre, ubicacion, capacidad, equipamiento, estado):
        """Actualiza los datos de un laboratorio"""
        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                return False
        except ValueError:
            return False
            
        data = {
            "nombre": nombre,
            "ubicacion": ubicacion,
            "capacidad": capacidad,
            "equipamiento": equipamiento,
            "estado": estado
        }
        
        return self.lab_repo.update_laboratory(lab_id, data)
    
    def delete_laboratorio(self, lab_id):
        """Elimina un laboratorio y sus horarios asociados"""
        # Primero eliminar todos los horarios del laboratorio
        self.horario_repo.delete_horarios_by_laboratory(lab_id)
        # Luego eliminar el laboratorio
        return self.lab_repo.delete_laboratory(lab_id)
    
    # --- CRUD Horarios ---
    
    def create_horario(self, laboratorio_id, dia_semana, hora_inicio_str, hora_fin_str, tipo):
        """Crea un nuevo horario para un laboratorio"""
        # Validar formato de hora
        if not self._validar_formato_hora(hora_inicio_str) or not self._validar_formato_hora(hora_fin_str):
            return None
        
        # Validar que hora_fin sea mayor que hora_inicio
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fin = datetime.strptime(hora_fin_str, "%H:%M").time()
            
            if hora_fin <= hora_inicio:
                return None
        except ValueError:
            return None
        
        # Verificar disponibilidad (no superposición)
        if not self.verificar_disponibilidad(laboratorio_id, dia_semana, hora_inicio_str, hora_fin_str):
            return None
        
        data = {
            "laboratorio_id": laboratorio_id,
            "dia_semana": dia_semana,
            "hora_inicio": hora_inicio_str,
            "hora_fin": hora_fin_str,
            "tipo": tipo
        }
        
        return self.horario_repo.create_horario(data)
    
    def get_horarios_by_laboratorio(self, laboratorio_id):
        """Obtiene todos los horarios de un laboratorio específico"""
        horarios = self.horario_repo.find_horarios_by_laboratory(laboratorio_id)
        # Convertir ObjectId a string para facilitar el manejo en la GUI
        for horario in horarios:
            horario["id"] = str(horario["_id"])
            del horario["_id"]
        return horarios
    
    def get_horario_by_id(self, horario_id):
        """Obtiene un horario por su ID"""
        horario = self.horario_repo.find_horario_by_id(horario_id)
        if horario:
            horario["id"] = str(horario["_id"])
            del horario["_id"]
        return horario
    
    def update_horario(self, horario_id, laboratorio_id, dia_semana, hora_inicio_str, hora_fin_str, tipo):
        """Actualiza los datos de un horario"""
        # Validar formato de hora
        if not self._validar_formato_hora(hora_inicio_str) or not self._validar_formato_hora(hora_fin_str):
            return False
        
        # Validar que hora_fin sea mayor que hora_inicio
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fin = datetime.strptime(hora_fin_str, "%H:%M").time()
            
            if hora_fin <= hora_inicio:
                return False
        except ValueError:
            return False
        
        # Verificar disponibilidad (excluyendo el horario que estamos editando)
        if not self.verificar_disponibilidad(laboratorio_id, dia_semana, hora_inicio_str, hora_fin_str, horario_id):
            return False
        
        data = {
            "laboratorio_id": laboratorio_id,
            "dia_semana": dia_semana,
            "hora_inicio": hora_inicio_str,
            "hora_fin": hora_fin_str,
            "tipo": tipo
        }
        
        return self.horario_repo.update_horario(horario_id, data)
    
    def delete_horario(self, horario_id):
        """Elimina un horario por su ID"""
        return self.horario_repo.delete_horario(horario_id)
    
    def verificar_disponibilidad(self, laboratorio_id, dia_semana, hora_inicio_str, hora_fin_str, excluir_horario_id=None):
        """Verifica si un horario está disponible para el laboratorio"""
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fin = datetime.strptime(hora_fin_str, "%H:%M").time()
            
            # Obtener todos los horarios del laboratorio para ese día
            horarios = self.horario_repo.find_horarios_by_laboratory_and_day(laboratorio_id, dia_semana)
            
            # Verificar superposición con otros horarios
            for horario in horarios:
                # Si estamos editando un horario, ignorar el mismo horario
                if excluir_horario_id and str(horario["_id"]) == excluir_horario_id:
                    continue
                
                h_inicio = datetime.strptime(horario["hora_inicio"], "%H:%M").time()
                h_fin = datetime.strptime(horario["hora_fin"], "%H:%M").time()
                
                # Verificar superposición
                if (hora_inicio < h_fin and hora_fin > h_inicio):
                    return False
            
            return True
        except (ValueError, KeyError):
            return False
    
    def _validar_formato_hora(self, hora_str):
        """Valida que el formato de hora sea HH:MM"""
        pattern = re.compile(r'^([0-1][0-9]|2[0-3]):([0-5][0-9])$')
        return bool(pattern.match(hora_str))