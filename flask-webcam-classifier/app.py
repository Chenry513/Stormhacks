from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import json

app = Flask(__name__)

# Load YOLO model
model = YOLO('my_model.pt')

# Load coarse labels (what we want to return)
with open('labels.txt', 'r') as f:
    coarse_labels = [line.strip() for line in f.readlines()]

# Load fine-to-coarse mapping
# with open('fine_to_coarse.json', 'r') as f:
#     fine_to_coarse = json.load(f)



@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """Classify image from webcam"""
    try:
        # Get the image data from request
        data = request.get_json()
        image_data = data['image']
        
        # Remove the data URL prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes)).convert('RGB')

        # Convert to numpy array in BGR format (H, W, C) like OpenCV
        image_rgb = np.array(image)  # PIL gives us RGB
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)  # Convert to BGR
        image_bgr = cv2.resize(image_rgb,(640,480))
        print(f"Image shape: {image_bgr.shape}, dtype: {image_bgr.dtype}, range: [{image_bgr.min()}, {image_bgr.max()}]")

        # Run inference with YOLO model (same as yolo_detect.py)
        results = model(image_bgr, verbose=False)

        print(results)
        # Get predictions from YOLO results
        # YOLO returns a list of results, we take the first one
        result = results[0]

        # Get the class names from the model
        class_names = model.names

        # Initialize coarse category predictions
        coarse_predictions = np.zeros(len(coarse_labels))

        # For YOLO detection models, we use bounding boxes and their confidence scores
        print(f"Number of boxes detected: {len(result.boxes)}")

        # Extract results the same way as yolo_detect.py
        detections = result.boxes
        print(f"Detections type: {type(detections)}")

        if len(detections) > 0:
            print("Processing detections using yolo_detect.py method")
            # Process all detected boxes using the same method as yolo_detect.py
            for i in range(len(detections)):
                # Get bounding box coordinates (same as yolo_detect.py)
                xyxy_tensor = detections[i].xyxy.cpu()
                xyxy = xyxy_tensor.numpy().squeeze()
                xmin, ymin, xmax, ymax = xyxy.astype(int)

                # Get bounding box class ID and name (same as yolo_detect.py)
                class_idx = int(detections[i].cls.item())
                fine_class_name = class_names[class_idx]

                # Get bounding box confidence (same as yolo_detect.py)
                confidence = detections[i].conf.item()

                print(f"Box {i}: {fine_class_name} at ({xmin},{ymin},{xmax},{ymax}) - confidence: {confidence:.3f}")
                coarse_category = fine_class_name
                coarse_idx = coarse_labels.index(coarse_category)
                # Add confidence (can be multiple detections of same category)
                coarse_predictions[coarse_idx] += confidence
        else:
            print("No boxes detected - this might indicate an issue with the model or image")

        #print(coarse_labels)
        # Create results dictionary
        results = []
        for i, label in enumerate(coarse_labels):
            results.append({
                'label': label,
                'confidence': float(coarse_predictions[i])
            })

        # Sort by confidence
        results = sorted(results, key=lambda x: x['confidence'], reverse=True)

        # Get bounding boxes for overlay
        boxes = []
        if len(result.boxes) > 0:
            for box in result.boxes:
                class_idx = int(box.cls.cpu().numpy())
                confidence = float(box.conf.cpu().numpy())
                fine_class_name = class_names[class_idx]

                # Map to coarse category
                coarse_category = fine_class_name
                if coarse_category in coarse_labels:
                    coarse_idx = coarse_labels.index(coarse_category)

                    # Get box coordinates (x1, y1, x2, y2)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                    boxes.append({
                        'x1': float(x1),
                        'y1': float(y1),
                        'x2': float(x2),
                        'y2': float(y2),
                        'confidence': confidence,
                        'class': coarse_category,
                        'fine_class': fine_class_name
                    })

        print(results)

        return jsonify({
            'success': True,
            'predictions': results,
            'boxes': boxes
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
