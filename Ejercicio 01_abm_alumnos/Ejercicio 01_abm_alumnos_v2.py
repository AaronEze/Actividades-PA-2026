import functools

#Decorador personalizado para loguear las operaciones
def log_operacion(operacion):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n>>> Iniciando operación: {operacion}")
            resultado = func(*args, **kwargs)
            print(f">>> Operación '{operacion}' Finalizada exitosamente.")
            return resultado
        return wrapper
    return decorador

#Decorador para registrar actividades de altas y bajas
def registro_actividad(actividad):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)
            if resultado:
                print(f"Registro de actividad: {actividad}")
            return resultado
        return wrapper
    return decorador


class Alumno:

    def __init__(self, id_alumno, nombre, curso, promedio):
        self._id = id_alumno
        self.nombre = nombre
        self.curso = curso
        self.promedio = promedio 

    @property
    def id(self):
        return self._id
    
    @property
    def promedio(self):
        return self._promedio
    
    @promedio.setter 
    def promedio(self, valor):
        if valor <0 or valor >10:
            raise ValueError("El promedio no puede ser ni negativo ni mayor a 10.")
        self._promedio = valor

    def __str__(self):
        return f"[ID: {self._id}] {self.nombre} - {self.curso} | {self.promedio:.2f}"
    

class GestorAlumnos:
    #Clase para manejar el abm.

    def __init__(self):
        self.alumnos = {}

    @registro_actividad("alta")
    def agregar_alumno(self, id_alumno, nombre, curso, promedio):
        if id_alumno in self.alumnos:
            print(f"Error: ya existe un alumno con el ID {id_alumno}.")
            return False
        
        try:
            nuevo_alumno = Alumno(id_alumno, nombre, curso, promedio)
            self.alumnos[id_alumno] = nuevo_alumno
            print(f"Alumno agregado al gestor: {nuevo_alumno.nombre}.")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        
    @log_operacion("Listar alumnos")
    def listar_alumnos(self):
        if not self.alumnos:
            print("No hay alumnos registrados en el sistema por ahora.")
            return
        
        print("\n--- Lista de Alumnos ---")
        for alumno in self.alumnos.values():
            print(alumno)
        print("-----------------------")

    @log_operacion("Actualizar Alumno")
    def actualizar_alumno(self, id_alumno, nuevo_nombre=None, nuevo_curso=None ,nuevo_promedio=None):
        if id_alumno not in self.alumnos:
            print(f"Error: No se encontró un alumno con el ID {id_alumno}.")
            return False
        
        alumno = self.alumnos[id_alumno]

        try:
            if nuevo_nombre:
                alumno.nombre = nuevo_nombre
            if nuevo_curso:
                alumno.curso = nuevo_curso
            if nuevo_promedio is not None:
                alumno.promedio = nuevo_promedio
            print (f"Alumno ID {id_alumno} actualizado correctamente.")
            return True
        except ValueError as e:
            print(f"Error de validación al actualizar: {e}.")
            return False
        

    @registro_actividad("baja")
    def eliminar_alumno(self, id_alumno):
        if id_alumno in self.alumnos:
            alumno = self.alumnos.pop(id_alumno)
            print(f"Alumno eliminado del sistema: {alumno.nombre}.")
            return True
        else:
            print(f"Error: No se encontró un alumno con el ID {id_alumno}.")
            return False
        
def mostrar_menu():
    print("\n" + "="*35)
    print(" 📚 SISTEMA ABM DE ALUMNOS 📚 ")
    print("="*35)
    print("[1] Agregar Alumno (Alta)")
    print("[2] Mostrar Alumnos (Lectura)")
    print("[3] Actualizar Alumno (Modificación)")
    print("[4] Eliminar Alumno (Baja)")
    print("[5] Salir")
    print("="*35)

def main():
    gestor = GestorAlumnos()

    #Se cargan datos de prueba.
    gestor.agregar_alumno(1, "Juan Carlos Bodoque", "5to B", 7.4)
    gestor.agregar_alumno(2, "Katarina Rostova","3ro A", 9.12)

    while True:
        mostrar_menu()
        opcion = input ("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                id_alumno = int(input("Ingrese ID numérico del alumno: "))
                if id_alumno in gestor.alumnos:
                     print(f"Error: Ya existe un alumno con esta ID: {id_alumno}.")
                     continue
                nombre = input("Ingrese Nombre: ").strip()
                curso = input("Ingrese el Curso: ").strip()
                promedio = float(input("Ingrese el promedio: "))
                gestor.agregar_alumno(id_alumno, nombre, curso, promedio)
            except ValueError:
                print("Error: El ID debe ser entero y el promedio debe ser un número válido.")

        elif opcion == "2":
            gestor.listar_alumnos()

        elif opcion == "3":
            try:
                id_alumno = int(input("Ingrese ID del alumno a modificar: "))
                if id_alumno not in gestor.alumnos:
                    print(f"Error. No se encontró un alumno con ese ID: {id_alumno}.")
                    continue
                nombre = input("Ingrese el Nuevo Nombre para este alumno /(Presione enter para dejar sin cambios): ").strip()
                curso = input("Ingrese el Nuevo Curso para este alumno /(Presione enter para dejar sin cambios): ").strip()
                promedio_str = input ("Ingrese el Nuevo Promedio para este alumno /(Presione enter para dejar sin cambios): ").strip()

                nombre = nombre if nombre else None
                curso = curso if curso else None
                promedio = float(promedio_str) if promedio_str else None

                gestor.actualizar_alumno(id_alumno, nombre, curso, promedio)
            except ValueError:
                print("Error: El ID y Promedio ingresados deben ser valores numéricos válidos.")

        elif opcion == "4":
            try:
                id_alumno = int(input("Ingrese ID del alumno a eliminar del sistema: "))
                gestor.eliminar_alumno(id_alumno)
            except ValueError:
                print("Error: El ID debe ser un número entero.")

        elif opcion == "5":
            print("Saliendo del sistema. Hasta la proxima.")
            break

        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__=="__main__":
    main()