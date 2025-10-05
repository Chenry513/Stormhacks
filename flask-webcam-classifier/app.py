from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
# import torch
import onnxruntime as ort
import numpy as np

app = Flask(__name__)

# Load ONNX model
onnx_session = ort.InferenceSession('ecoar.onnx')

# Get input and output names
input_name = onnx_session.get_inputs()[0].name
output_name = onnx_session.get_outputs()[0].name

# Get input shape
input_shape = onnx_session.get_inputs()[0].shape

def softmax(vector):
    """
    Computes the softmax of a given vector.

    Args:
        vector (numpy.ndarray or list): The input vector.

    Returns:
        numpy.ndarray: The softmax output, which is a probability distribution.
    """
    # Convert input to a NumPy array if it's a list
    vector = np.array(vector)

    # Subtract the maximum value for numerical stability to prevent overflow
    # when calculating exponentials of large numbers.
    stable_vector = vector - np.max(vector)

    # Calculate the exponential of each element
    e_x = np.exp(stable_vector)

    # Divide by the sum of exponentials to normalize into a probability distribution
    return e_x / np.sum(e_x)

# Load labels
with open('labels.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for ONNX model"""
    # Resize image
    image = image.resize(target_size)
    # Convert to array and normalize
    img_array = np.array(image, dtype=np.float32)
    # Normalize to [0, 1]
    img_array = img_array / 255.0
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # ONNX models typically expect NCHW format (batch, channels, height, width)
    # Transpose from NHWC to NCHW
    img_array = np.transpose(img_array, (0, 3, 1, 2))

    return img_array

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
        
        print(image)
        # Preprocess image
        input_data = preprocess_image(image)
        
        # Run inference with ONNX Runtime
        outputs = onnx_session.run([output_name], {input_name: input_data})
        
        
        print(outputs)
        # Get predictions
        predictions = softmax(outputs[0][0])
                
        # probs = torch.softmax(predictions, dim=1)[0]
        # pred_idx = torch.argmax(probs).item()

        # print("Prediction:", labels[pred_idx])
        # print("Probabilities:", {labels[i]: float(p) for i,p in enumerate(probs)})
    
        # print(softmax(predictions))
        
        # Create results dictionary
        results = []
        for i, label in enumerate(labels):
            results.append({
                'label': label,
                'confidence': float(predictions[i])
            })
        
        # Sort by confidence
        results = sorted(results, key=lambda x: x['confidence'], reverse=True)
        
        return jsonify({
            'success': True,
            'predictions': results
        })
        sleep(1)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
