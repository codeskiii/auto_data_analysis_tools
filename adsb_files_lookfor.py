import json
import os
import sys

def load_file(name: str) -> dict:
    try:
        with open(name, 'r') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{name}': {e}")
        return None
    except Exception as e:
        print(f"Error loading file '{name}': {e}")
        return None

def get_to_file_dir(file: dict) -> dict:
    file_ = file.copy()
    try:
        for n in ['properties','Attributes','properties']:
            file = file[n]
        return file
    except:
        try:
            for n in ['properties','Attributes','oneOf',0,'properties']:
                print(n)
                file_ = file_[n]
            return file_
        except:
            return "ERROR"

def find_in_file( look_for: str, path: str) -> list:
    file = load_file(path)
    if file is None:
        return []
    file = get_to_file_dir(file)

    if file == "ERROR":
        print(f"error in: {path}")
        sys.exit()
    
    if file is None:
        return []

    where_found = []
    for n in file:
        print(n)
        if isinstance(file[n], dict):
            if look_for in file[n]:
                where_found.append({n: file[n][look_for]})
            else:
                print(f"'{look_for}' not found in {n}")
                where_found.append({n: {}})
        else:
            print(f"Skipping non-dict item in {n}")

    print(f"Results from file '{path}': {where_found}")
    return where_found

def find_in_folder(folder: str, look_for: str) -> None:
    try:
        print('listing ')
        files = os.listdir(folder)
    except Exception as e:
        print(f"Error listing directory '{folder}': {e}")
        return None
    
    print('start for loop')
    container = {}
    print(files)
    for f in files:
        print(f)
        file_path = os.path.join(folder, f)
        if os.path.isfile(file_path) and file_path.endswith('.json'):
            output = find_in_file( look_for, file_path)
            if output:
                tittle_splitted = (f.replace('.', ' ')).split()
                tittle_splitted_c = [tittle_splitted[1], tittle_splitted[2], tittle_splitted[3]]
                tittle = '.'.join(tittle_splitted_c)
                container[tittle] = output
    
    with open('output.json', 'w') as outfile:
        json.dump(container, outfile, indent=4)

if __name__ == '__main__':
    folder = 'assets'
    look_for = 'default'

    find_in_folder(folder, look_for)
