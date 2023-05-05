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

