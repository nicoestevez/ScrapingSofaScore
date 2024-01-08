ids = []

anno = 2023

# Abrir el archivo para lectura
with open(f"links/links_{anno}.txt", 'r') as file:
    for row in file:
        elements = row.split("#id:")
        ids.append(elements[1].strip())

with open(f"ids/ids_{anno}.txt", 'w') as file:
    for id in ids:
        file.write(id + "\n")
