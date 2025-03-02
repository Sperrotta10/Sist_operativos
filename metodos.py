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