import os
import configparser
from flask import Flask, jsonify, request
from PIL import Image, ImageOps
from PyPDF2 import PdfMerger



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
        
        log(f"Received photo with name: {photo_name}")
        
        return "Upload successful", 200

    except Exception as e:
        log(f"error {e}")
        
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
        log(identifier)
        processing_method = json_payload.get("processingMethod")
        log(processing_method)

        match processing_method:
            case "LEAVE_AS_IMAGES":
                processing_method_leave_as_images(identifier)
            case "CREATE_PDFS":
                processing_method_create_pdfs(identifier)
            case "MERGE_PDFS":
                processing_method_merge_pdfs(identifier)
            case _:
                print(f"Invalid processing method: {processing_method}")
                return "Failure", 500
        
        return "Success", 200
    
    except Exception as e:
        log(f"error: {e}")

        return "Failure", 500

def processing_method_leave_as_images(identifier):
    pass

def processing_method_create_pdfs(identifier):
    folders = identifier.split('/')
    path = os.path.join(root_directory, *folders[1:-1])
    image_name_root = folders[-1]

    image_files = [f for f in os.listdir(path) if f.startswith(image_name_root) and f.lower().endswith(".jpg")]

    for image_file in image_files:
        image_path = os.path.join(path, image_file)
        log(f"Converting: {image_path}")
        jpg_to_pdf(image_path)

def processing_method_merge_pdfs(identifier):
    processing_method_create_pdfs(identifier)

    folders = identifier.split('/')
    path = os.path.join(root_directory, *folders[1:-1])
    image_name_root = folders[-1]

    merged_pdf_path = os.path.join(path, f"{image_name_root}.pdf")
    merger = PdfMerger()

    pdf_files = [f for f in os.listdir(path) if f.startswith(image_name_root) and f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(path, pdf_file)
        merger.append(pdf_file_path)
    
    merger.write(merged_pdf_path)
    merger.close()
    
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(path, pdf_file)
        os.remove(pdf_file_path)

def jpg_to_pdf(path):
    try:
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        pdf_path = path.replace(".jpg", ".pdf")
        image.save(pdf_path, "PDF", resolution=100.0)

        os.remove(path)
    except Exception as e:
        print(f"Error converting {path} to PDF: {e}")



def log(message):
    print(message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
