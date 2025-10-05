# Webcam Garbage Classifier

EcoSortAR tackles the issue of recycling contamination, a major problem in North America where only about 25–27% of recyclable waste is properly diverted, resulting in billions of dollars in unnecessary costs—over $20 million in extra expenses for Toronto alone and more than $3.5 billion across the U.S. due to manual sorting, lost material value, and landfilling rejected loads. Our app uses machine learning to identify waste items in real time and leverages augmented reality to show users what type of material they’re disposing of, helping them learn proper sorting habits over time. Powered by a YOLO deep learning model trained on 1,000 images categorized into e-waste, organics, plastic, cardboard, and paper, EcoSortAR analyzes the camera feed to instantly classify waste and provide sorting guidance. Looking ahead, we aim to reduce sorting errors by 10–20%, customize sorting rules to each user’s city, introduce gamified rewards for consistent accuracy, and eventually add an AR feature that overlays step-by-step disposal guidance directly on the detected item in the camera view.

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

5. Click "Classify Image" to get predictions

## Usage Tips

- Ensure good lighting for better classification results
- Position the object clearly in the center of the camera view
- Try to avoid cluttered backgrounds
- The model works best when the object takes up a significant portion of the frame

## Project Structure

```
flask-webcam-classifier/
├── app.py                 # Flask backend application
├── model.tflite          # TensorFlow Lite model
├── labels.txt            # Classification labels
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Frontend HTML/CSS/JavaScript
└── README.md            # This file
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
