import os

file_path = 'requirements.txt'
try:
    with open(file_path, 'r', encoding='utf-16le') as f:
        content = f.read()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("requirements.txt convertido exitosamente a UTF-8.")
    print("Contenido:")
    print(content)
except Exception as e:
    print(f"Error: {e}")
