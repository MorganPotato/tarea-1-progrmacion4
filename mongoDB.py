from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["recetario"]  # Base de datos llamada 'recetario'
coleccion_recetas = db["recetas"]  # Colección donde guardaremos las recetas

# Función para agregar una receta
def agregar_receta():
    nombre = input("Introduce el nombre de la receta: ")

    receta = {
        "nombre": nombre,
        "ingredientes": [],
        "pasos": []
    }

    print("\n--- Ingredientes ---")
    while True:
        ingrediente = input("Introduce un ingrediente (deja vacío para terminar): ")
        if ingrediente == "":
            break
        receta["ingredientes"].append(ingrediente)

    print("\n--- Pasos ---")
    while True:
        paso = input("Introduce un paso (deja vacío para terminar): ")
        if paso == "":
            break
        receta["pasos"].append(paso)

    # Insertar la receta en la colección
    coleccion_recetas.insert_one(receta)
    print("Receta agregada con éxito.")

# Función para ver las recetas
def ver_recetas():
    recetas = list(coleccion_recetas.find())
    if recetas:
        print("\n--- Listado de recetas ---")
        for receta in recetas:
            print(f"ID: {receta['_id']} | Nombre: {receta['nombre']}")
            print("Ingredientes:")
            for ingrediente in receta['ingredientes']:
                print(f"  - {ingrediente}")
            print("Pasos:")
            for paso in receta['pasos']:
                print(f"  - {paso}")
            print("\n")
    else:
        print("No hay recetas registradas.")

# Menú principal
def menu():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("b) Ver listado de recetas")
        print("f) Salir")

        opcion = input("Selecciona una opción: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'b':
            ver_recetas()
        elif opcion == 'f':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

# Ejecución del programa
if __name__ == "__main__":
    menu()