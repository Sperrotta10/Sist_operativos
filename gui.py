import tkinter as tk
import random
from metodos import MemoryManager



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