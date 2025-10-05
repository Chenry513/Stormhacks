# Webcam Garbage Classifier

A Flask web application that uses your webcam and a TensorFlow Lite model to classify garbage items in real-time.

## Features

- Real-time webcam capture
- TensorFlow Lite model inference
- Classification of 6 types of waste:
  - Cardboard
  - Glass
  - Metal
  - Paper
  - Plastic
  - Trash
- Beautiful, responsive UI with confidence scores

## Prerequisites

- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Installation

1. Navigate to the project directory:
```bash
cd flask-webcam-classifier
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Click "Start Camera" to activate your webcam

4. Point your camera at a garbage item


## Usage Tips

- Ensure good lighting for better classification results
- Position the object clearly in the center of the camera view
- Try to avoid cluttered backgrounds
- The model works best when the object takes up a significant portion of the frame

## Project Structure

```
flask-webcam-classifier/
├── templates/                 # HTML templates for the Flask web app
├── README.md                  # Project documentation
├── app.py                      # Main Flask application file (runs the web server)
├── fine_to_coarse.json         # JSON file mapping fine-grained classes to broader categories
├── labels.txt                  # List of class labels used by the classifier
├── model.ipynb                 # Jupyter notebook for model training and experimentation
├── my_model.pt                 # Saved PyTorch model weights for inference
├── requirements.txt            # Python dependencies required to run the project
├── tempCodeRunnerFile.py       # Temporary file used during development/debugging
├── yolo_detect.py              # YOLO-based object detection script (for bounding boxes)
└── ...                          # Additional files as needed
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **ML Framework**: TensorFlow Lite
- **Image Processing**: OpenCV, Pillow, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Webcam API**: MediaDevices Web API

## Troubleshooting

### Camera not working
- Ensure you've granted camera permissions to your browser
- Check if another application is using the camera
- Try refreshing the page or restarting the browser

### Classification errors
- Ensure all required packages are installed correctly
- Check that model.tflite and labels.txt are in the correct directory
- Verify Python version compatibility

### Import errors
- Ensure you're in the virtual environment
- Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`

## License

This project uses a garbage classification model for educational purposes.
