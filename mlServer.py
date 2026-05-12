from flask import Flask, request, jsonify
import base64
import numpy as np
from PIL import Image
import io
import os
import uuid
from datetime import datetime

import NeuralNetworkPython as nn

app = Flask(__name__)

max_file = max(os.listdir("models"), key=lambda x: int(x))
network = nn.NeuralNetwork(f"models/{max_file}")

SAVE_FOLDER = "trainingDataFromUser"
os.makedirs(SAVE_FOLDER, exist_ok=True)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Decode the base64 image sent from Node
    image_data = base64.b64decode(data["image"])
    image = Image.open(io.BytesIO(image_data)).convert("L")  # grayscale

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{timestamp}_{unique_id}.png"
    filepath = os.path.join(SAVE_FOLDER, filename)
    image.save(filepath)

    image = image.resize((28, 28))  # MNIST standard size — adjust if yours differs
    pixels = np.array(image).flatten() / 255.0  # normalize to 0-1


    out = network.compute(pixels)
    if (network.is_softmax()):
        out = network.compute_softmax(out)
    result = np.argmax(out)

    return jsonify({"digit": int(result)})


if __name__ == "__main__":
    app.run(port=5000)