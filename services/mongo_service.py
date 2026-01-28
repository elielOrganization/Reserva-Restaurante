from pymongo import MongoClient
from models.restaurant_model import Restaurante, Horario

#URL de conexión
MONGO_URI = (
    "mongodb+srv://DiegoSanJuan:restaurantesyreservas@cluster0.qis2yqu.mongodb.net/?appName=Cluster0"
)

#Variables globales
DB_NAME = "restaurante" 


def get_db():

    db = MongoClient(MONGO_URI)
    return db[DB_NAME]

def cargar_restaurantes():
    """
    Carga los restaurantes desde la base de datos MongoDB y los 
    mapea a objetos de la clase Restaurante.
    """
    db = get_db()
    coleccion = db['Restaurantes']
    
    # Lista donde guardaremos los objetos instanciados
    restaurantes_lista = []
    
    # Obtenemos los documentos de la colección
    cursor_restaurantes = coleccion.find({})

    for res in cursor_restaurantes:
        # Extraemos el horario para instanciar su modelo correspondiente
        # Usamos .get() para evitar errores si el campo no existe
        datos_horario = res.get('horario', {})
        horario_obj = Horario(
            apertura=datos_horario.get('apertura', "00:00"),
            cierre=datos_horario.get('cierre', "00:00")
        )

        # Instanciamos el objeto Restaurante con los datos de Atlas
        nuevo_restaurante = Restaurante(
            # Si tu modelo Restaurante usa 'id', mapeamos el '_id' de Mongo
            id=str(res.get('_id')), 
            nombre=res.get('nombre', 'Sin nombre'),
            direccion=res.get('direccion', 'Dirección no disponible'),
            telefono=res.get('telefono', ''),
            aforo_maximo=res.get('aforo_maximo', 0),
            horario=horario_obj,
            reservas=res.get('reservas', []),
            imagen_url=res.get('imagen_url', ''),
            imagenes=res.get('imagenes', [])
        )
        
        restaurantes_lista.append(nuevo_restaurante)


    # Si la base de datos está vacía, podrías devolver el cache por defecto 
    # o simplemente la lista (que estaría vacía o llena según la BD)
    return restaurantes_lista if restaurantes_lista else []


if __name__ == "__main__":
    try:
        get_db()
    except Exception as e:
        print(f"Error al conectar la base de datos. {e}")
    else:
        print("Conexión exitosa.")
        
