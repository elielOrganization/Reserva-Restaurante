import hashlib
import os
from services.mongo_service import get_db
from datetime import datetime, timedelta
from models.restaurant_model import Restaurante

def _hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored: str, password: str) -> bool:
    try:
        salt, hashed = stored.split("$", 1)
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == hashed
    except Exception:
        return False

def register_user(name: str, username: str, email: str, phone: str, password: str) -> tuple[bool, str]:
    try:
        db = get_db()
        users = db["Usuarios"]

        if users.find_one({"usuario": username}): 
            return False, "El nombre de usuario ya existe"

        if users.find_one({"email": email}):
            return False, "El email ya está registrado"

        pwd_hash = _hash_password(password)
        user_doc = {
            "email": email,
            "nombre": name,
            "passwd": pwd_hash,
            "telefono": phone,
            "usuario": username,
        }

        users.insert_one(user_doc)
        return True, "Usuario registrado correctamente"
    except Exception as ex:
        return False, f"Error al registrar usuario: {str(ex)}"

def login_user(username: str, password: str) -> tuple[bool, str, str]:
    try:
        db = get_db()
        users = db["Usuarios"]
        
        user = users.find_one({"usuario": username})
        
        if not user:
            return False, "Usuario o contraseña incorrectos", ""
        
        if not verify_password(user.get("passwd", ""), password):
            return False, "Usuario o contraseña incorrectos", ""
        
        return True, "Login exitoso", username
    except Exception as ex:
        return False, f"Error al iniciar sesión: {str(ex)}", ""

def registrar_reserva(username: str, fech_hora: str, rest_nombre: str, num_pers: int):
    try:
        db = get_db()
        
        reserva_doc = {
            "fecha_hora": fech_hora,
            "estado": "confirmada",
            "restaurante_nombre": rest_nombre,
            "num_personas": num_pers,
            "usuario": username,
        }

        db.Restaurantes.update_one(
            {"nombre": rest_nombre},
            {"$push": {"reservas": reserva_doc}},
        )

        return True, "Reserva registrada correctamente"
    
    except Exception as ex:
        return False, f"Error al registrar la reserva: {str(ex)}"

def calcular_reservas_disponible(restaurante: Restaurante, fecha: str):
    aforo_max = restaurante.aforo_maximo
    reservas_realizadas = 0

    if hasattr(restaurante, 'reservas') and restaurante.reservas:
        for reserva in restaurante.reservas:
            fecha_reserva = reserva["fecha_hora"].split("T")[0]
            if fecha_reserva == fecha and reserva.get("estado") == "confirmada":
                reservas_realizadas += int(reserva["num_personas"])
    
    return aforo_max - reservas_realizadas

def obtener_reservas_usuario(username: str):
    try:
        db = get_db()
        cursor = db.Restaurantes.find({"reservas.usuario": username})
        
        mis_reservas = []
        
        for restaurante in cursor:
            if "reservas" in restaurante:
                for reserva in restaurante["reservas"]:
                    if reserva.get("usuario") == username:
                        reserva_con_nombre = reserva.copy()
                        if "restaurante_nombre" not in reserva_con_nombre:
                            reserva_con_nombre["restaurante_nombre"] = restaurante.get("nombre")
                        mis_reservas.append(reserva_con_nombre)
                        
        return mis_reservas
    except Exception as e:
        print(f"Error recuperando reservas: {e}")
        return []

def cancelar_reserva_usuario(username, restaurante_nombre, fecha_hora):
    try:
        db = get_db()
        
        resultado = db.Restaurantes.update_one(
            {"nombre": restaurante_nombre},
            {"$pull": {
                "reservas": {
                    "usuario": username, 
                    "fecha_hora": fecha_hora
                }
            }}
        )
        
        if resultado.modified_count > 0:
            return True, "Reserva cancelada correctamente"
        else:
            return False, "No se pudo encontrar la reserva para cancelar"
            
    except Exception as e:
        return False, f"Error al cancelar: {str(e)}"