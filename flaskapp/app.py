import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/getFolderStructure", methods=["GET"])
def get_folder_structure():
    root_directory = "D:\\Documents\\DocumentHarborRoot"
    folder_structure = generate_folder_structure(root_directory)
    return jsonify(folder_structure)

def generate_folder_structure(directory):
    folder_structure = {
        "name": os.path.basename(directory),
        "subFolders": []
    }

    for subdirectory in os.listdir(directory):
        subdirectory_path = os.path.join(directory, subdirectory)
        
        if os.path.isdir(subdirectory_path):
            subfolder_structure = generate_folder_structure(subdirectory_path)
            folder_structure["subFolders"].append(subfolder_structure)
    
    return folder_structure

@app.route("/uploadImage", methods=["POST"])
def upload_image():
    pass

@app.route("/sendEndSignal", methods=["POST"])
def send_end_signal():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
