import redis
import json

# Configuración de la base de datos
client = redis.Redis(host='localhost', port=6379, db=0)


# Función para agregar una receta
def agregar_receta():
    receta_id = client.incr('receta_id')  # Genera un nuevo ID incremental
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes (separados por comas): ")
    pasos = input("Ingrese los pasos: ")

    nueva_receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    # Almacenar la receta como un JSON en KeyDB
    client.set(f"receta:{receta_id}", json.dumps(nueva_receta))
    print("Receta agregada exitosamente.\n")


# Función para actualizar una receta
def actualizar_receta():
    receta_id = input("Ingrese el ID de la receta a actualizar: ")
    receta_key = f"receta:{receta_id}"

    if client.exists(receta_key):
        nombre = input("Ingrese el nuevo nombre de la receta: ")
        ingredientes = input("Ingrese los nuevos ingredientes (separados por comas): ")
        pasos = input("Ingrese los nuevos pasos: ")

        receta_actualizada = {
            "nombre": nombre,
            "ingredientes": ingredientes,
            "pasos": pasos
        }

        client.set(receta_key, json.dumps(receta_actualizada))
        print("Receta actualizada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")


# Función para eliminar una receta
def eliminar_receta():
    receta_id = input("Ingrese el ID de la receta a eliminar: ")
    receta_key = f"receta:{receta_id}"

    if client.exists(receta_key):
        client.delete(receta_key)
        print("Receta eliminada exitosamente.\n")
    else:
        print("Receta no encontrada.\n")


# Función para ver todas las recetas
def ver_recetas():
    print("\nListado de recetas:")
    for key in client.scan_iter("receta:*"):
        receta_id = key.decode().split(":")[1]
        receta = json.loads(client.get(key).decode())
        print(f"{receta_id} - {receta['nombre']}")
    print()


# Función para buscar los ingredientes y pasos de una receta
def buscar_receta():
    receta_id = input("Ingrese el ID de la receta que desea buscar: ")
    receta_key = f"receta:{receta_id}"

    if client.exists(receta_key):
        receta = json.loads(client.get(receta_key).decode())
        print(f"\nReceta: {receta['nombre']}\nIngredientes: {receta['ingredientes']}\nPasos: {receta['pasos']}\n")
    else:
        print("Receta no encontrada.\n")


# Función para mostrar el menú
def mostrar_menu():
    print("Seleccione una opción:")
    print("a) Agregar nueva receta")
    print("b) Actualizar receta existente")
    print("c) Eliminar receta existente")
    print("d) Ver listado de recetas")
    print("e) Buscar ingredientes y pasos de receta")
    print("f) Salir")


# Función principal para ejecutar el programa
def main():
    while True:
        mostrar_menu()
        opcion = input("Opción: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'b':
            actualizar_receta()
        elif opcion == 'c':
            eliminar_receta()
        elif opcion == 'd':
            ver_recetas()
        elif opcion == 'e':
            buscar_receta()
        elif opcion == 'f':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

    # Cerrar la conexión al salir
    client.close()


# Ejecutar el programa
main()

