def add_unique_element(name):
    # Obtener números usados en el formato base_name-<número>
    used_numbers = [
        int(element.split('-')[-1])
        for element in elements
        if element.startswith(f"{name}-") and element.split('-')[-1].isdigit()
    ]
    
    # Determinar el siguiente número disponible
    if used_numbers:
        next_number = max(used_numbers, default=0) + 1
    
    # Crear y añadir el nuevo nombre
        name = f"{name}-{next_number}"
    elements.append(name)
    return name

# Lista inicial
elements = ["Server-1", "Server-2", "Other-1", "Server-14"]

# Ejemplo de uso
new_server = add_unique_element("Server")
print(f"Nuevo servidor: {new_server}")
print(f"Lista actualizada: {elements}")
