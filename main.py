from flask import  Flask, request, render_template_string,send_from_directory
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

    output_filename = "output_" + file.filename
    processed_image_encoded = draw_skeleton(image, os.path.join("uploads", output_filename))
    
    
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
                <br>
                <a href="/download/{{ output_filename }}">Download Processed Image</a>
            </div>
        </div>                          
        <a href="/">Upload another image</a>
    </body>
    </html>
    ''', original_image=original_image_encoded, processed_image=processed_image_encoded, output_filename=output_filename)

@app.route("/download/<filename>", methods =['GET'])
def download_image(filename):
    print(filename)
    return send_from_directory("uploads", filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
