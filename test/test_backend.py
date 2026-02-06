import sys
import os
from unittest.mock import patch, MagicMock

# Agregar la carpeta padre al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user_model import User
from models.restaurant_model import Restaurante, Horario
from services.crud_operations import _hash_password, verify_password, register_user, login_user


# ==================== TESTS DE USUARIO ====================

def test_user_creation():
    """Test 1: Crear un usuario correctamente"""
    user = User(
        email="test@example.com",
        nombre="Juan Pérez",
        passwd="password123",
        telefono="123456789",
        usuario="juanperez"
    )
    
    assert user.email == "test@example.com"
    assert user.nombre == "Juan Pérez"
    assert user.usuario == "juanperez"
    assert user.telefono == "123456789"
    print("✓ Test 1 passed: Usuario creado correctamente")


def test_user_to_dict():
    """Test 2: Convertir usuario a diccionario"""
    user = User(
        email="test@example.com",
        nombre="María García",
        passwd="secure_pass",
        telefono="987654321",
        usuario="mariagarcia"
    )
    
    user_dict = user.to_dict()
    
    assert isinstance(user_dict, dict)
    assert user_dict['email'] == "test@example.com"
    assert user_dict['nombre'] == "María García"
    assert 'passwd' in user_dict
    assert 'usuario' in user_dict
    print("✓ Test 2 passed: Usuario convertido a diccionario correctamente")


# ==================== TESTS DE RESTAURANTE ====================

def test_horario_creation():
    """Test 3: Crear un horario correctamente"""
    horario = Horario(apertura="10:00", cierre="22:30")
    
    assert horario.apertura == "10:00"
    assert horario.cierre == "22:30"
    print("✓ Test 3 passed: Horario creado correctamente")


def test_restaurante_creation():
    """Test 4: Crear un restaurante correctamente"""
    horario = Horario(apertura="12:00", cierre="23:00")
    restaurante = Restaurante(
        id="123",
        nombre="La Pizzería",
        direccion="Calle Principal 123",
        telefono="555-1234",
        aforo_maximo=50,
        horario=horario,
        reservas=[],
        imagen_url="https://example.com/pizza.jpg",
        imagenes="https://example.com/images/"
    )
    
    assert restaurante.nombre == "La Pizzería"
    assert restaurante.aforo_maximo == 50
    assert restaurante.horario.apertura == "12:00"
    assert len(restaurante.reservas) == 0
    print("✓ Test 4 passed: Restaurante creado correctamente")


def test_restaurante_to_dict():
    """Test 5: Convertir restaurante a diccionario"""
    horario = Horario(apertura="12:00", cierre="23:00")
    restaurante = Restaurante(
        id="456",
        nombre="El Sushi",
        direccion="Avenida Central 456",
        telefono="555-5678",
        aforo_maximo=30,
        horario=horario,
        reservas=[],
        imagen_url="https://example.com/sushi.jpg",
        imagenes="https://example.com/images/"
    )
    
    rest_dict = restaurante.to_dict()
    
    assert isinstance(rest_dict, dict)
    assert rest_dict['nombre'] == "El Sushi"
    assert rest_dict['aforo_maximo'] == 30
    assert isinstance(rest_dict['horario'], dict)
    assert rest_dict['horario']['apertura'] == "12:00"
    assert rest_dict['horario']['cierre'] == "23:00"
    print("✓ Test 5 passed: Restaurante convertido a diccionario correctamente")


def test_horario_to_dict():
    """Test 6: Convertir horario a diccionario"""
    horario = Horario(apertura="09:00", cierre="21:00")
    horario_dict = horario.to_dict()
    
    assert isinstance(horario_dict, dict)
    assert horario_dict['apertura'] == "09:00"
    assert horario_dict['cierre'] == "21:00"
    print("✓ Test 6 passed: Horario convertido a diccionario correctamente")


# ==================== TESTS DE CONTRASEÑA ====================

def test_hash_password():
    """Test 7: Hash de contraseña se genera correctamente"""
    password = "miContraseña123"
    hashed = _hash_password(password)
    
    # El hash debe contener un salt y el hash separados por $
    assert '$' in hashed
    parts = hashed.split('$')
    assert len(parts) == 2
    
    # El hash no debe ser igual a la contraseña plana
    assert hashed != password
    print("✓ Test 7 passed: Hash de contraseña generado correctamente")


def test_verify_correct_password():
    """Test 8: Verificar contraseña correcta"""
    password = "contraseña_segura"
    hashed = _hash_password(password)
    
    # Debe verificar correctamente una contraseña válida
    assert verify_password(hashed, password) == True
    print("✓ Test 8 passed: Contraseña correcta verificada")


def test_verify_incorrect_password():
    """Test 9: Rechazar contraseña incorrecta"""
    password = "contraseña_correcta"
    wrong_password = "contraseña_incorrecta"
    hashed = _hash_password(password)
    
    # Debe rechazar una contraseña incorrecta
    assert verify_password(hashed, wrong_password) == False
    print("✓ Test 9 passed: Contraseña incorrecta rechazada")


# ==================== TESTS DE REGISTRO ====================

@patch('services.crud_operations.get_db')
def test_register_user_success(mock_get_db):
    """Test 10: Registro de usuario exitoso"""
    # Mock de la base de datos
    mock_db = MagicMock()
    mock_users_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_users_collection
    mock_get_db.return_value = mock_db
    
    # Simular que no existen usuarios con ese username o email
    mock_users_collection.find_one.return_value = None
    
    success, message = register_user(
        name="Carlos López",
        username="carloslopez",
        email="carlos@example.com",
        phone="555-5555",
        password="password123"
    )
    
    assert success == True
    assert "registrado correctamente" in message
    print("✓ Test 10 passed: Registro de usuario exitoso")


@patch('services.crud_operations.get_db')
def test_register_user_duplicate_username(mock_get_db):
    """Test 11: Rechazar usuario duplicado"""
    mock_db = MagicMock()
    mock_users_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_users_collection
    mock_get_db.return_value = mock_db
    
    # Simular que ya existe un usuario con ese username
    mock_users_collection.find_one.return_value = {"usuario": "juanperez"}
    
    success, message = register_user(
        name="Juan Pérez",
        username="juanperez",
        email="juan@example.com",
        phone="555-1111",
        password="password123"
    )
    
    assert success == False
    assert "nombre de usuario ya existe" in message
    print("✓ Test 11 passed: Usuario duplicado rechazado")


# ==================== TESTS DE LOGIN ====================

@patch('services.crud_operations.get_db')
def test_login_user_success(mock_get_db):
    """Test 12: Login exitoso"""
    mock_db = MagicMock()
    mock_users_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_users_collection
    mock_get_db.return_value = mock_db
    
    # Crear una contraseña hasheada válida
    password = "password123"
    hashed_password = _hash_password(password)
    
    # Simular que existe el usuario con contraseña válida
    mock_users_collection.find_one.return_value = {
        "usuario": "testuser",
        "passwd": hashed_password
    }
    
    success, message, username = login_user("testuser", password)
    
    assert success == True
    assert username == "testuser"
    assert "exitoso" in message
    print("✓ Test 12 passed: Login exitoso")


@patch('services.crud_operations.get_db')
def test_login_user_invalid_credentials(mock_get_db):
    """Test 13: Rechazar credenciales inválidas"""
    mock_db = MagicMock()
    mock_users_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_users_collection
    mock_get_db.return_value = mock_db
    
    # Usuario no existe
    mock_users_collection.find_one.return_value = None
    
    success, message, username = login_user("usuarionoexiste", "password123")
    
    assert success == False
    assert username == ""
    assert "Usuario o contraseña incorrectos" in message
    print("✓ Test 13 passed: Credenciales inválidas rechazadas")


if __name__ == '__main__':
    print("\n" + "="*50)
    print("EJECUTANDO TESTS DEL BACKEND")
    print("="*50 + "\n")
    
    test_user_creation()
    test_user_to_dict()
    test_horario_creation()
    test_restaurante_creation()
    test_restaurante_to_dict()
    test_horario_to_dict()
    test_hash_password()
    test_verify_correct_password()
    test_verify_incorrect_password()
    test_register_user_success()
    test_register_user_duplicate_username()
    test_login_user_success()
    test_login_user_invalid_credentials()
    
    print("\n" + "="*50)
    print("✓ TODOS LOS TESTS PASARON CORRECTAMENTE")
    print("="*50)
