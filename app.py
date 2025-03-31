

def replicate_path(path_file: str) -> None:
    """
    Replicate the given path file.
    """
    folder_path = f'replicated_paths/{os.path.basename(path_file).split(".")[0]}'
    with open(path_file, 'r') as f:
        data = json.load(f)
    if not os.path.exists(f'{folder_path}'):
        os.makedirs(f'{folder_path}')
    else:
        print(f"Directory {os.path.basename(path_file).split('.')[0]} already exists")
        #return
    failed = []
    destination_path = os.path.join(os.getcwd(), folder_path)
    for item in data:
        try:
            if item["type"] == "file":
                if os.path.dirname(os.path.join(destination_path, item['path'])):
                    os.makedirs(os.path.dirname(os.path.join(destination_path, item['path'])), exist_ok=True)
                with open(f"{os.path.join(destination_path, item['path'])}", 'w') as f:
                    pass
            elif item["type"] == "directorie":
                os.makedirs(os.path.join(destination_path, item['path']))

        except Exception as e:
            failed.append(item)
    if failed:

        print("Failed to replicate the following paths:")
        for item in failed:
            print(f"Path: {item['path']} - Type: {item['type']}")


def extract_path_to_list(path: str) -> list:
    """
    Extract the path from the given string.
    """
    l = []
    dir_files = os.listdir(path)
    e={"type":"directorie", "path":path}
    l.append(e)
    for file in dir_files:
        if not os.path.isdir(os.path.join(path, file)):
            e={"type":"file", "path":os.path.join(path, file)}
            l.append(e)
        else:
            l+=extract_path_to_list(os.path.join(path, file))
        
    return l

def filter_path(path: str,extracted_list: list) -> list:
    """
    Filter the path from the given string.
    """
    l = []
    for item in extracted_list:
        mod_path=item["path"].replace(path, "")
        if mod_path=="":
            continue
        if mod_path.startswith("\\"):
            mod_path=mod_path[1:]
        l.append({"type":item["type"], "path":mod_path})
    return l

def extract_path(path: str) -> list:
    l=[]
    
    l+=extract_path_to_list(path)
    l=filter_path(path, l)
    l.insert(0,{"type":"src", "path":path})
    return l
    

def show_available_paths() -> None:
    """
    Show the available paths in the extracted_paths directory.
    """
    print("Available paths:")
    for file in os.listdir('extracted_paths'):
        if file.endswith('.json'):
            print(f"- {file}")

def create_save_directorie_and_replicated() -> None:
    """
    Create a save directorie for the extracted paths.
    """
    if not os.path.exists('extracted_paths'):
        os.makedirs('extracted_paths')
    if not os.path.exists('replicated_paths'):
        os.makedirs('replicated_paths')

if __name__ == '__main__':
    
    import os
    import json
    
    create_save_directorie_and_replicated()
    while True:
        res=input("extract path? (y/n/exit) : ")
        if res.lower() in ["y","n","exit"]:
            break
    if res.lower()=="y":
        dir_path = input("Enter the path to extract: ")
    #dir_path=r"E:\bilel\NVIDIA Videos"
        extracted_paths = extract_path(dir_path)
        with open(f'extracted_paths/{os.path.basename(dir_path)}.json', 'w') as f:
            json.dump(extracted_paths, f, indent=4)
    elif res.lower()=="n":
        while True:
            res=input("replicate path? (y/n/exit) : ")
            if res.lower() in ["y","n","exit"]:
                break
        if res.lower()=="y":
            show_available_paths()
            file_name = input("Enter the name of the file to replicate: ")
            if not file_name.endswith('.json'):
                file_name += '.json'
            dir_path = os.path.join('extracted_paths', file_name)
            if not os.path.exists(dir_path):
                print(f"File {file_name} does not exist in extracted_paths.")
                exit(1)
            else:
                replicate_path(dir_path)
