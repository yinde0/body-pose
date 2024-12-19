from flask import  Flask, request, render_template_string
import os
from pose import *
import tensorflow as tf
import base64



app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Upload an image</title>
    </head>
    <body>
        <h1>Upload your image here</h1>
        <form method=post enctype=multipart/form-data action="/upload_images">
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
    </body>
    </html>
    ''')

@app.route('/upload_images', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = os.path.join('uploads', file.filename)
    file.save(filename)

    # Process the image
    image = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image)

    processed_image_encoded = draw_skeleton(image)
    
    
    # Convert images to display on HTML
    original_image_encoded = base64.b64encode(open(filename, "rb").read()).decode('ascii')

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Image Upload</title>
        <style>
            .image-container {
                display: flex;
                justify-content: space-around;
                align-items: center;
            }
            .image-container img {
                margin: 10px;
                height: 224px; /* Maintain the same height for both images */
            }
        </style>
    </head>
    <body>
        <h1>Uploaded Image and Processed Image</h1>
        <div class="image-container">                         
            <div>
                <h2>Original Image:</h2>
                <img src="data:image/jpeg;base64,{{ original_image }}" style="width:560px; height:560px;" alt="Original Image">
            </div>
            <div>
                <h2>Processed Image:</h2>
                <img src="data:image/jpeg;base64,{{ processed_image }}" style="width:560px; height:560px;" alt="Processed Image">
            </div>
        </div>                          
        <a href="/">Upload another image</a>
    </body>
    </html>
    ''', original_image=original_image_encoded, processed_image=processed_image_encoded)


if __name__ == '__main__':
    app.run(debug=True)
