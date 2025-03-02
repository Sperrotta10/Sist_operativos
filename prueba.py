import tkinter as tk
import random

# Clase para representar un bloque de memoria
class MemoryBlock:
    def __init__(self, size, is_free=True):
        self.size = size         # Tamaño del bloque de memoria
        self.is_free = is_free   # Indicador de si el bloque está libre o ocupado
        self.process = None      # Proceso asociado al bloque (None si está libre)

    def __repr__(self):
        return f"{'Free' if self.is_free else 'Used'} Block of size {self.size} KB"

# Clase para gestionar la memoria, asignación y liberación de bloques
class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size   # Tamaño total de la memoria disponible
        self.memory = [MemoryBlock(total_size)]  # Inicializa la memoria con un único bloque grande
        self.used_memory = 0            # Memoria usada actualmente

    # Asigna un bloque de memoria para un proceso
    def allocate(self, size, process_name):
        for block in self.memory:
            # Buscar un bloque libre que sea lo suficientemente grande
            if block.is_free and block.size >= size:
                if block.size > size:
                    # Fragmentación interna: crear un bloque extra para el espacio sobrante
                    remaining_size = block.size - size
                    block.size = size  # Reducir el tamaño del bloque a la necesidad del proceso
                    # Crear un nuevo bloque libre con el espacio sobrante
                    self.memory.append(MemoryBlock(remaining_size, is_free=True))

                # Asignar el bloque al proceso
                block.is_free = False
                block.process = process_name
                self.used_memory += size
                return f"Process {process_name} allocated {size} KB of memory"
        
        # Si no se encontró un bloque adecuado
        return "No suitable block found for allocation"

    # Libera la memoria ocupada por un proceso
    def free(self, process_name):
        for block in self.memory:
            # Encontrar el bloque ocupado por el proceso especificado
            if not block.is_free and block.process == process_name:
                block.is_free = True   # Marcar el bloque como libre
                block.process = None   # Liberar el proceso
                self.used_memory -= block.size  # Reducir la memoria usada
                return f"Process {process_name} freed {block.size} KB of memory"
        
        # Si no se encuentra el proceso
        return "Process not found"

    # Obtiene el estado actual de la memoria
    def get_memory_status(self):
        # Calcular la memoria libre sumando los tamaños de los bloques libres
        free_memory = sum([block.size for block in self.memory if block.is_free])
        return {
            "total_memory": self.total_size,
            "used_memory": self.used_memory,
            "free_memory": free_memory,
            "blocks": self.memory  # Lista de bloques de memoria
        }

    # Realiza una compactación de la memoria para reducir la fragmentación externa
    def compact(self):
        compacted_memory = []  # Lista para almacenar los bloques compactados
        free_space = 0  # Espacio libre acumulado

        for block in self.memory:
            if block.is_free:
                free_space += block.size  # Acumular el espacio libre
            else:
                compacted_memory.append(block)  # Añadir bloques ocupados al inicio
        
        # Agregar el bloque de memoria libre al final
        if free_space > 0:
            compacted_memory.append(MemoryBlock(free_space, is_free=True))

        self.memory = compacted_memory  # Reemplazar la memoria actual por la compactada
        print("Memory compacted")

    # Simula el swapping de procesos cuando la memoria está llena
    def swap(self):
        # Si la memoria usada es mayor al 50% de la capacidad total
        if self.used_memory > self.total_size // 2:
            for block in self.memory:
                # Buscar un bloque ocupado y liberar su espacio
                if not block.is_free:
                    print(f"Swapping out process {block.process} to disk...")
                    block.is_free = True  # Marcar el bloque como libre
                    block.process = None  # Eliminar el proceso
                    self.used_memory -= block.size  # Reducir la memoria usada
                    break

# Interfaz gráfica con Tkinter para gestionar visualmente la memoria
class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Manager")
        self.root.configure(bg="lightblue")  # Fondo azul claro
        self.manager = MemoryManager(1000)  # Crear un gestor de memoria con 1000 KB

        # Configurar la grilla principal para que se expanda
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear un canvas para mostrar la memoria
        self.canvas = tk.Canvas(root, width=600, height=200, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Etiqueta de estado de la memoria
        self.info_label = tk.Label(root, text="Memory Status", font=("Arial", 12))
        self.info_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Contenedor para los botones
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_frame.config(bg="lightblue")  # Configurar el color de fondo
        
        # Configurar la grilla del contenedor de botones
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Botones
        self.add_process_button = tk.Button(self.button_frame, text="Add Process", command=self.add_process, bg="#a8cbff", width=12, height=2, border=3.5, relief="groove")
        self.add_process_button.grid(row=0, column=0, padx=8, pady=5)

        self.free_process_button = tk.Button(self.button_frame, text="Free Process", command=self.free_process, bg="#a8cbff", width=12, height=2, border=3.5, relief="groove")
        self.free_process_button.grid(row=0, column=1, padx=8, pady=5)

        self.compact_button = tk.Button(self.button_frame, text="Compact Memory", command=self.compact_memory, bg="#a8cbff", width=12, height=2, border=3.5, relief="groove")
        self.compact_button.grid(row=0, column=2, padx=8, pady=5)

        self.swap_button = tk.Button(self.button_frame, text="Swap Process", command=self.swap_memory, bg="#a8cbff", width=12, height=2, border=3.5, relief="groove")
        self.swap_button.grid(row=0, column=3, padx=8, pady=5)

        # Etiqueta y lista de procesos
        self.process_info_label = tk.Label(root, text="Processes:", font=("Arial", 12), bg="lightblue")
        self.process_info_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.process_listbox = tk.Listbox(root, height=6)
        self.process_listbox.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        # Permitir que la lista de procesos se expanda correctamente
        self.root.grid_rowconfigure(4, weight=1)

        # Actualizar la representación inicial de la memoria
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        x = 10  # Coordenada inicial en X
        total_width = 580  # Ancho total del canvas

        for block in self.manager.memory:
            width = (block.size / self.manager.total_size) * total_width
            color = "green" if block.is_free else "red"

            self.canvas.create_rectangle(x, 50, x + width, 150, fill=color, outline="black")
            if not block.is_free:
                self.canvas.create_text(x + width / 2, 100, text=block.process, fill="white")
            x += width  

        # Actualizar etiqueta de memoria
        memory_status = self.manager.get_memory_status()
        self.info_label.config(text=f"Total: {memory_status['total_memory']} KB, Used: {memory_status['used_memory']} KB, Free: {memory_status['free_memory']} KB", bg="lightblue")

        # Actualizar lista de procesos
        self.process_listbox.delete(0, tk.END)
        for block in self.manager.memory:
            if not block.is_free:
                self.process_listbox.insert(tk.END, f"{block.process} - {block.size} KB")

    def add_process(self):
        size = random.randint(50, 300)
        process_name = f"P{random.randint(1, 100)}"
        self.manager.allocate(size, process_name)
        self.update_canvas()

    def free_process(self):
        for block in self.manager.memory:
            if not block.is_free:
                self.manager.free(block.process)
                break
        self.update_canvas()

    def compact_memory(self):
        self.manager.compact()
        self.update_canvas()

    def swap_memory(self):
        self.manager.swap()
        self.update_canvas()

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()




"""
Visualización:

- Los bloques se muestran en verde para los libres y rojos para los ocupados. Los procesos se etiquetan dentro de los bloques ocupados.
- La fragmentación interna se ve cuando un bloque es más grande de lo necesario para un proceso.
- ompactación mueve bloques y agrupa los libres al final.
- Swapping muestra cómo se mueve un proceso fuera de la memoria.

"""