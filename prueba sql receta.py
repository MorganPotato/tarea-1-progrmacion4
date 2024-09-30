from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor de base de datos
engine = create_engine('mysql+mysqlconnector://usuario:contraseña@localhost/recetario', echo=True)

# Base declarativa de SQLAlchemy
Base = declarative_base()

# Definición de las tablas como clases de Python
class Receta(Base):
    __tablename__ = 'recta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ingredientes = relationship("Ingrediente", back_populates="recta")
    pasos = relationship("Paso", back_populates="recta")


class Ingrediente(Base):
    __tablename__ = 'ingrdnt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    recta_id = Column(Integer, ForeignKey('recta.id'))
    nombre = Column(String(100), nullable=False)
    recta = relationship("Receta", back_populates="ingredientes")


class Paso(Base):
    __tablename__ = 'paso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    recta_id = Column(Integer, ForeignKey('recta.id'))
    descripcion = Column(String(255), nullable=False)
    recta = relationship("Receta", back_populates="pasos")


# Crear las tablas
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

def agregar_receta(session):
    nombre = input("Introduce el nombre de la receta: ")
    receta = Receta(nombre=nombre)

    session.add(receta)
    session.commit()

    print("\n--- Ingredientes ---")
    while True:
        ingrediente = input("Introduce un ingrediente (deja vacío para terminar): ")
        if ingrediente == "":
            break
        nuevo_ingrediente = Ingrediente(nombre=ingrediente, recta=receta)
        session.add(nuevo_ingrediente)

    print("\n--- Pasos ---")
    while True:
        paso = input("Introduce un paso (deja vacío para terminar): ")
        if paso == "":
            break
        nuevo_paso = Paso(descripcion=paso, recta=receta)
        session.add(nuevo_paso)

    session.commit()

def ver_recetas(session):
    recetas = session.query(Receta).all()
    if recetas:
        print("\n--- Listado de recetas ---")
        for receta in recetas:
            print(f"{receta.id}. {receta.nombre}")
    else:
        print("No hay recetas registradas.")

def menu():
    session = Session()

    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("b) Ver listado de recetas")
        print("f) Salir")

        opcion = input("Selecciona una opción: ").lower()

        if opcion == 'a':
            agregar_receta(session)
        elif opcion == 'b':
            ver_recetas(session)
        elif opcion == 'f':
            session.close()
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

# Ejecución del programa
if __name__ == "__main__":
    menu()
