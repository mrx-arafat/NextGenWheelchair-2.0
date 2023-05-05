import base64
import io
import json
from PIL import Image
import cv2
import dlib
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat')


def get_head_orientation(shape):
    # Define the 3D model of the face
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (0.0, -330.0, -65.0),  # Chin
        (-225.0, 170.0, -135.0),  # Left eye left corner
        (225.0, 170.0, -135.0),  # Right eye right corner
        (-150.0, -150.0, -125.0),  # Left mouth corner
        (150.0, -150.0, -125.0)  # Right mouth corner
    ])

    # Extract 2D landmarks from the shape
    image_points = np.array([
        (shape.part(30).x, shape.part(30).y),  # Nose tip
        (shape.part(8).x, shape.part(8).y),  # Chin
        (shape.part(36).x, shape.part(36).y),  # Left eye left corner
        (shape.part(45).x, shape.part(45).y),  # Right eye right corner
        (shape.part(48).x, shape.part(48).y),  # Left mouth corner
        (shape.part(54).x, shape.part(54).y)  # Right mouth corner
    ], dtype="double")

    # Camera internals
    size = img.shape
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    mat = np.hstack((rotation_matrix, translation_vector))
    _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(mat)

    return euler_angles


@app.route('/')
def index():
    return render_template('head-move.html')


@app.route('/process_frame', methods=['POST'])
def process_frame():
    data_url = request.form['image']
    im_data = base64.b64decode(data_url)
    im_file = io.BytesIO(im_data)
    img = Image.open(im_file).convert('RGB')
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Detect faces
    faces = detector(img)

    if len(faces) > 0:
        # Get the landmarks for the first detected face
        shape = predictor(img, faces[0])

        # Calculate head orientation
        euler_angles = get_head_orientation(shape)
        pitch, yaw, roll = euler_angles

        # Determine motion direction based on head orientation
        if abs(yaw) > abs(pitch) and abs(yaw) > abs(roll):
            motion_direction = 'Left' if yaw > 0 else 'Right'
        elif abs(pitch) > abs(roll):
            motion_direction = 'Up' if pitch < 0 else 'Down'
        else:
            motion_direction = 'N/A'

        motion_angle = f'Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Roll: {roll:.2f}'
    else:
        motion_direction = 'N/A'
        motion_angle = 'N/A'

    return jsonify({'motion_direction': motion_direction, 'motion_angle': motion_angle})


if __name__ == '__main__':
    app.run(debug=True)

