import subprocess
import re
import os
import shutil
import argparse

def sanitize_filename_MF(name):
    name = name.replace(":latest", "")
    return re.sub(r'[<>:"/\\|?*.]', '-', name)

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True, encoding='utf-8')
    output_text, error_text = process.communicate()
    return output_text.strip()

def create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder):
    template_command = f'ollama show --template {model_name}'
    template = run_command(template_command)
    
    if not template:
        print(f"Error: model '{model_name}' not found or the template is empty. Please check the model name and try again.")
        return
    
    parameters_command = f'ollama show --parameters {model_name}'
    parameters = run_command(parameters_command)
    
    system_command = f'ollama show --system {model_name}'
    system_message = run_command(system_command)
    
    modelfile_command = f'ollama show --modelfile {model_name}'
    modelfile_message = run_command(modelfile_command)
    
    model_name = sanitize_filename_MF(model_name)
    new_folder_path = os.path.join(BackUp_Folder, model_name)

    if os.path.exists(new_folder_path) and os.path.isdir(new_folder_path):
        print(f"Model: '{model_name}' already exists in the backup folder, so it will be skipped.")
        return

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Created folder: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    
    model_content = f"""FROM {model_name}.gguf
TEMPLATE """ + '"""' + f"""{template}""" + '"""' + "\n"
    
    for line in parameters.splitlines():
        model_content += f'PARAMETER {line}\n'
    
    model_content += f'system "{system_message}"\n'
    
    print(model_content)
    
    with open(os.path.join(new_folder_path, output_file), 'w', encoding='utf-8') as file:
        file.write(model_content)
    
    print(f'Model file created: {output_file}')
    
    modelfile_message = modelfile_message.strip()
    # Handle path formatting for regex matching
    model_path = str(Ollama_Model_Folder).replace('\\', '/')
    # Use the detected model path in the regex pattern
    ollama_models_dir = detect_ollama_model_folder()
    model_path = str(ollama_models_dir).replace('\\', '/')
    pattern = fr'FROM\s+["\']?({re.escape(model_path)}/[^"\'\s]+)["\']?'
    model_file_location_match = re.search(pattern, modelfile_message)

    if not model_file_location_match:
        print(f"Debug - Modelfile content:\n{modelfile_message}")
        print(f"Debug - Search pattern used: {pattern}")
        print(f"Debug - Ollama models directory: {ollama_models_dir}")
    extracted_model_file_location = model_file_location_match.group(1) if model_file_location_match else "Model_file_location_not_found"
    
    print(f"Model gguf file found: {extracted_model_file_location}")
    
    new_model_file_name = f"{model_name}.gguf"
    new_model_file_path = os.path.join(new_folder_path, new_model_file_name)

    if os.path.exists(extracted_model_file_location):
        shutil.copy2(extracted_model_file_location, new_model_file_path)
        print(f"Copied and renamed model file to: {new_model_file_path}")
    else:
        print(f"Model file not found at: {extracted_model_file_location}")

def scan_folder(path):
    for root, dirs, files in os.walk(path):
        if any(file.endswith('.gguf') for file in files):
            folder_name = os.path.basename(root)
            print(fr'Import model: {folder_name}')
            cmd = f'ollama create {folder_name} -f modelfile'
            subprocess.run(cmd, shell=True, cwd=root)

def extract_names(data):
    lines = data.strip().split('\n')
    names = [line.split()[0] for line in lines[1:]]
    return ';;;'.join(names)

def detect_ollama_model_folder():
    system_paths = [
        "/usr/share/ollama/.ollama/models",
        "/usr/local/share/ollama/.ollama/models"
    ]
    for path in system_paths:
        if os.path.exists(path):
            return path
    return os.path.join(os.path.expanduser("~"), ".ollama", "models")

def process_models(model_names):
    for model_name in model_names:
        model_name = model_name.strip()
        print(model_name)
        output_file = "ModelFile"
        Ollama_Model_Folder = detect_ollama_model_folder()
        BackUp_Folder = os.path.join(".", "llama_backup")
        if not os.path.exists(BackUp_Folder):
            os.makedirs(BackUp_Folder)
            print(f"Created backup folder: {BackUp_Folder}")
        create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder)

def parse_args():
    parser = argparse.ArgumentParser(description='Ollama Model Manager')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for backup
    backup_parser = subparsers.add_parser('backup', help='Backup all models')

    # Subparser for export
    export_parser = subparsers.add_parser('export', help='Export a model')
    export_parser.add_argument('model_name', help='Name of the model to export')

    # Subparser for import
    import_parser = subparsers.add_parser('import', help='Import models from backup')
    import_parser.add_argument('folder_path', help='Path to the backup folder')

    return parser.parse_args()

def main():
    args = parse_args()

    if args.command == 'backup':
        data = run_command("ollama list")
        model_names_string = extract_names(data)
        model_names = model_names_string.split(";;;")
        process_models(model_names)
    elif args.command == 'export':
        model_name = args.model_name.strip()
        output_file = "ModelFile"
        Ollama_Model_Folder = detect_ollama_model_folder()
        BackUp_Folder = os.path.join(".", "llama_backup")
        if not os.path.exists(BackUp_Folder):
            os.makedirs(BackUp_Folder)
            print(f"Created backup folder: {BackUp_Folder}")
        create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder)
    elif args.command == 'import':
        backup_folder = args.folder_path
        scan_folder(backup_folder)
    else:
        # Fallback to interactive menu if no arguments provided
        print("1. Backup all models")
        print("2. Export a model")
        print("3. Import models from backup")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            data = run_command("ollama list")
            model_names_string = extract_names(data)
            model_names = model_names_string.split(";;;")
            process_models(model_names)
        elif choice == "2":
            model_name = input("Enter model name: ")
            model_name = model_name.strip()
            output_file = "ModelFile"
            Ollama_Model_Folder = detect_ollama_model_folder()
            BackUp_Folder = os.path.join(".", "llama_backup")
            if not os.path.exists(BackUp_Folder):
                os.makedirs(BackUp_Folder)
                print(f"Created backup folder: {BackUp_Folder}")
            create_ollama_model_file(model_name, output_file, BackUp_Folder, Ollama_Model_Folder)
        elif choice == "3":
            backup_folder = input("Enter backup folder path: ")
            scan_folder(backup_folder)
        else:
            print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()