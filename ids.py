ids = []

# Abrir el archivo para lectura
with open('links.txt', 'r') as file:
    for row in file:
        elements = row.split("#id:")
        ids.append(elements[1].strip())

with open('ids.txt', 'w') as file:
    for id in ids:
        file.write(id + "\n")
