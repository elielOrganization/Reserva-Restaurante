from .mongo_service import get_db
import hashlib
import os

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
    """
    Intenta hacer login con usuario y contraseña
    Retorna: (success: bool, message: str, username_or_error: str)
    """
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
