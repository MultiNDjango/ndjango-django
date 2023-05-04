from flask import Flask, request, jsonify
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image from the request
    image_path = 'temp.jpg'  # choose a temporary file path
    request.files['image'].save(image_path)  # save the uploaded file

    # Use the machine learning model to make a prediction
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    prediction = decode_predictions(preds, top=3)[0]

    # Convert the prediction to a list of dictionaries
    results = []
    for pred in prediction:
        results.append({'name': pred[1], 'score': float(pred[2])})

    # Return the prediction in JSON format
    return jsonify({'results': results})

if __name__ == '__main__':
    # Load the machine learning model
    model = keras.models.load_model('./resnet50.h5')
    
    app.run()
