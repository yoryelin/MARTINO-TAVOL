import os

file_path = 'requirements.txt'
try:
    with open(file_path, 'r', encoding='utf-16le') as f:
        content = f.read()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    with open('scratch/req_out.txt', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Success")
except Exception as e:
    with open('scratch/req_out.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}")
