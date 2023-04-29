def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


def parse_data(lines):
    data = {}
    title = ""
    for line in lines:
        # Si la línea empieza por Key to, es un título
        # Ejemplo: Key to Matches
        # Si la linea contiene un =, es una clave con su valor como subelemento del título
        # Ejemplo: Key to Matches
        #   FTHG=Full Time Home Team Goals
        #   FTAG=Full Time Away Team Goals


        if line.startswith("Key to"):
            title = line.strip()[:-1].replace("Key to ", "").replace(" ", "_").lower()
            data[title.strip()] = {}
        elif " = " in line:
            if title == "":
                raise Exception("Error, no se ha encontrado el título")
            # Asegurarse de que sea el primer ' = ' de la línea
            key, clave = line.split(" = ", 1)
            data[title][key.strip()] = clave.strip()
    return data


def view_data_print(data):
    for title, values in data.items():
        print(f"\n{title}:")
        for key, value in values.items():
            print(f"  {key}: {value}")


def view_data_json(data):
    import json
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    file_path = "data/soccer/notes.txt"
    lines = read_file(file_path)
    data = parse_data(lines)
    view_data_print(data)
    view_data_json(data)