import os
import configparser
from flask import Flask, jsonify, request

# Retrive root directory specified in the config.ini
# This will be the root directory sent to the app, it sees all under this
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config", "config.ini"))
root_directory = config.get("ServerConfig", "root_directory")

app = Flask(__name__)

# Just for checking on webbrowser / ignore
@app.route("/")
def hello_world():
    return "Hello, World!"

# Called by the app to refresh its knowledge of the current directory structure
@app.route("/getFolderStructure", methods=["GET"])
def get_folder_structure():
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

# Recieves and saves files during photo session, no processing
@app.route("/uploadImage", methods=["POST"])
def upload_image():
    try:
        photo_name = request.form.get("photoName")
        photo_data = request.files.get("file").read()

        save_image(photo_name, photo_data)
        
        print(f"Received photo with name: {photo_name}")
        
        return "Upload successful", 200

    except Exception as e:
        print("error")
        
        return "Upload failed", 500
    
def save_image(photo_name, image_data):
    folders = photo_name.split('/')

    image_path = os.path.join(root_directory, *folders[1:])

    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)

# Signal to begin processing on the images in the photo session
@app.route("/sendEndSignal", methods=["POST"])
def send_end_signal():
    try:
        json_payload = request.get_json()

        identifier = json_payload.get("identifier")
        processing_method = json_payload.get("processingMethod")

        # Do shit here
        print(identifier)
        print(processing_method)

        return "Success", 200
    except Exception as e:
        print("error")

        return "Failure", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
