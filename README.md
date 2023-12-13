# DocumentHarbor
DocumentHarbor is a two-part solution for efficient document digitization. It consists of a server component and an Android app designed to streamline the process of capturing, organizing, and processing images of documents.

The current state of the project is that it is still in active development. It requires users to have some knowledge of programming to get running on their device or a lot of time to figure it out.
> This Server code is meant to accompany the corresponding Android app code which can be found [here](https://github.com/tyson-01/DocumentHarbor_App)

  

## Overview
DocumentHarbor is built to address the need for a fast, lightweight, and privacy-focused solution for document digitization over a local network. Existing solutions I have tried either do much of the processing on the mobile-device and/or send them to a cloud server where you then must migrate and save the files post-capture.

DocumentHarbor takes advantage of the latent information that exists in the physical layout of the documents you wish to digitize to speed up this process. Simply define the name of the final PDF you would like to produce, navigate the app's interface to select the folder on your computer where you would like the pdf to end up, then start taking pictures uninterrupted.

In addition to generating a single PDF from the documents, you also have the ability to save every image in the series of photos as individual PDFs, or leave them in their original .jpg format. In these cases the series of images will be suffixed with a number to indicate its index in the series of images, retaining that latent information about document order in their new digitized form (eg. myImage1.jpg, myImage2.jpg, etc.).

## Key Features
-  **Local Processing:** All image processing is performed locally on the computer where the server is ran, and data is only sent over the local network.
-  **Organized Digitization:** Leverage the latent structure of your physical documents for efficient digitization that retains the organization of their physical counterparts.
-  **Flexible Processing Methods:** Choose between leaving the images in their .jpg format, converting to individual PDFs, or merging them into one continuous PDF file.
-  **Automatic Document Cropping** (Experimental)**:** Automatically crop and realign your documents from the captured images before converting to pdf. [Must be enabled in the DocumentHarbor_server's config.ini file.]

## Server Setup
### Prerequisites
- Python 3.10 or later installed on your computer.
### Installation
1. Clone the server repository: [DocumentHarbor Server](https://github.com/tyson-01/DocumentHarbor_Server)
2. Edit the config.ini file located in flaskapp\config\config.ini to set your root folder. The app will only have access to this folder and its subfolders. Currently it is set as "D:\Documents\DocumentHarborRoot", replace this placeholder with your desired root folder.
3. navigate to the local repository and run "runApp" script. This sets up the virtual environment and installs any needed dependencies, as well as running the server.
4. Note the IP address and port the server is running on as this will be required for the app setup below. From an example output snippet from the server terminal we would need to extract the information "192.168.1.39:5000":
>...
>  \* Running on all addresses (0.0.0.0)
>  \* Running on `http://127.0.0.1:5000`
>  \* Running on `http://192.168.1.39:5000`
> Press CTRL+C to quit
> ...

## App Setup
### Prerequisites
- Android Studio installed on your computer to configure the app and load the app onto your android device.
### Installation
1. Clone the app repository: [DocumentHarbor App](https://github.com/tyson-01/DocumentHarbor_App)
2. Open the project in Android Studio.
3. In the file app\java\com\example\documentharbor\servercommunication\ApiClient.java set the variable "BASE_URL" to the IP address and port noted in step 4 of the server installation. Currently it is set to the placeholder in the example.
4. Build and run the app on your android device.

## Use
1. Start server by navigating to where you downloaded DocumentHarbor_Server and run the runApp.bat script.
2. Start the app on your android device.
3. Define a session name/document name.
4. Navigate to where you wish to store your new document(s).
5. Begin photo session, selecting the processing method desired.
6. Take images of your documents one by one. Click "done" when all documents captured.
7. View resulting document(s) in the defined file on the server's computer.

## Future Directions
- Improve on the auto-cropping for pdf generation (Currently in experimental options, modify the server's config.ini file to enable). As well as create a means to efficiently manually crop images which it failed to do automatically.
- Add the option to turn on document enhancement. Image brightening/normalization and increase contrast to create a more readable digital document.
- UI alterations/overhaul to enhance intuitive use.
- Add the option to additionally generate text files of the documents context using optical character recognition.
- (eventually) Package the server as a downloadable program and publish app on the android app store to make more accessible.