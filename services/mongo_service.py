from pymongo import MongoClient
#URL de conexión
MONGO_URI = (
    "mongodb+srv://DiegoSanJuan:restaurantesyreservas@cluster0.qis2yqu.mongodb.net/?appName=Cluster0"
)

#Variables globales
DB_NAME = "restaurante" 


def get_db():

    db = MongoClient(MONGO_URI)
    return db[DB_NAME]


if __name__ == "__main__":
    try:
        get_db()
    except Exception as e:
        print(f"Error al conectar la base de datos. {e}")
    else:
        print("Conexión exitosa.")
        
