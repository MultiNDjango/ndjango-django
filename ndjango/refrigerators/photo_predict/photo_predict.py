from flask import Flask, request, jsonify
from tensorflow import keras
from tensorflow.keras.preprocessing import image
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
    images = np.vstack([x])
    pred = model.predict(images, batch_size=32)
    label = np.argmax(pred, axis=1)

    # Convert the prediction to a list of dictionaries
    result = {'name': class_names_kor[label[0]], 'score':float(pred[0][label])}

    # Return the prediction in JSON format
    return jsonify({'result': result})

if __name__ == '__main__':
    # Load the machine learning model
    model = keras.models.load_model('./best-cnn-model.h5')
    
    class_names = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber',
                   'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 
                   'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'radish', 'soy beans', 'spinach', 
                   'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon']
    
    class_names_kor = {
        0: '사과', 1: '바나나', 2: '비트', 3: '파프리카', 4: '양배추', 5: '당근', 6: '컬리플라워', 7: '고추', 8: '옥수수', 9: '오이',
        10: '가지', 11: '마늘', 12: '생강', 13: '포도', 14: '할라피뇨', 15: '키위', 16: '레몬', 17: '양상추', 18: '망고', 19: '양파',
        20: '오렌지', 21: '파프리카', 22: '배', 23: '완두콩', 24: '파인애플', 25: '석류', 26: '감자', 27: '무', 28: '콩', 29: '시금치',
        30: '초당옥수수', 31: '고구마', 32: '토마토', 33: '순무', 34: '수박'
    }
    
    app.run()
