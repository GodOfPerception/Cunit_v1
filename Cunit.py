# * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Title: Cunit file generatornb                          *
#  Author: Shashank Shrivastav                            *
#  Email: contactshashank10@gmail.com                     *
#  Date: 2023                                             *
#  Code version: 2.0                                      *
#  Availability: https://github.com/GodOfPerceptionn      *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * *



import json
import os
import random
import string
import time
import shutil
import subprocess
global path
path = os.path.join(os.path.expanduser("~"), "")


def process_json(input_json):
    data = json.loads(input_json)

    for item in data.get('item', []):
        name = item.get('name', '')
        response_list = item.get('response', [])
        
        if response_list:
            response_body = response_list[0].get('body', '')
        else:
            response_body = ''

        folder_name = data.get('info', {}).get('name', '')

        folder_path = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/input', folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, f"{name}_endpoint.json"), 'w') as file:
            file.write(response_body)

        folder_pathh = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/output', folder_name)
        if not os.path.exists(folder_pathh):
            os.makedirs(folder_pathh)

        with open(os.path.join(folder_pathh, f"{name}_endpoint.json"), 'w') as file:
            file.write(response_body)
        
    return process_folder(folder_path)








def generate_random_value(data_type):
    
    if data_type == "string":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    elif data_type == "number":
        return random.uniform(0, 100)
    elif data_type == "boolean":
        return random.choice([True, False])
    elif data_type == "null":
        return None
    elif data_type == "list":
        return [generate_random_value("string") for _ in range(3)]
    elif data_type == "object":
        return {"field_" + str(i): generate_random_value("string") for i in range(3)}
    else:
        raise ValueError("Unsupported data type: {}".format(data_type))

def generate_random_json(json_data):
    if isinstance(json_data, dict):
        return {key: generate_random_json(value) for key, value in json_data.items()}
    elif isinstance(json_data, list):
        return [generate_random_json(item) for item in json_data]
    elif isinstance(json_data, str):
        return generate_random_value("string")
    elif isinstance(json_data, int) or isinstance(json_data, float):
        return generate_random_value("number")
    elif isinstance(json_data, bool):
        return generate_random_value("boolean")
    elif json_data is None:
        return generate_random_value("null")
    else:
        return json_data

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r') as file:
                    json_data = json.load(file)
                    
                if not json_data:
                    print(f"Skipping empty file: {filename}")
                    continue

                modified_json_data = generate_random_json(json_data)

                with open(file_path, 'w') as file:
                    json.dump(modified_json_data, file, indent=2)
            except json.JSONDecodeError as e:
                print(f"Error processing file {filename}: {e}")


    return run_bazel_test(bazel_test_target, workspace_path)



def run_bazel_test(target, workspace_path):
    os.chdir(workspace_path)

    command = "/opt/homebrew/bin/bazel test {}".format(target)
    process = subprocess.run(command, shell=True, text=True)

    if process.returncode == 0:
        print("Bazel test successful")
    else:
        print("Error: Bazel test failed")






def copy_files_to_desktop(src_folder, dest_folderr):
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return

    if not os.path.exists(dest_folderr):
        os.makedirs(dest_folderr)
        print(f"Destination folder '{dest_folderr}' created.")

    for filename in os.listdir(src_folder):
        if filename.endswith(".json"):
            src_file_path = os.path.join("/private/var/tmp/", filename)

            if os.path.exists(src_file_path):
                dest_desktop_file_path = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/output', file_name)


                shutil.copy(src_file_path, dest_desktop_file_path)
                print(f"File '{filename}' copied to '{dest_folderr}'.")
            else:
                print(f"JSON file '{filename}' not found in /private/var/tmp/. Skipping.")





bazel_test_target = '//coil:connector-integrations-spec'

workspace_path = f'{path}Fivetran/engineering'


file_name = input("Enter the postman file name: ")
folder_path = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/input', file_name)

with open(f'{path}Desktop/{file_name}.json', 'r') as file:
    json_data = file.read()
process_json(json_data)

time.sleep(2)
folder_path = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/input', file_name)
src_folder = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/output', file_name)
dest_folderr = os.path.join(f'{path}Fivetran/engineering/integrations/coil_connectors/test-resources/output', file_name)

copy_files_to_desktop(src_folder, dest_folderr)


ask = input("Enter yes if file Gnerate output ran succesfully: ")
time.sleep(2)
if ask == "yes":
    run_bazel_test(bazel_test_target, workspace_path)
