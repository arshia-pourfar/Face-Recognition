"""Real-time face recognition using reference images from the faces/ directory."""

import os
from pathlib import Path

import cv2
import face_recognition
import numpy as np

# Resolve paths relative to the project root, not the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FACES_DIR = PROJECT_ROOT / "faces"


def load_known_faces(faces_dir=None):
    """Load known face encodings and their labels from reference images."""
    if faces_dir is None:
        faces_dir = DEFAULT_FACES_DIR

    faces_dir = Path(faces_dir)

    if not faces_dir.is_dir():
        raise FileNotFoundError(
            f"Face image directory not found: {faces_dir}\n"
            "Create the folder and add reference images named "
            "'<name>_<anything>.jpg' (for example, 'alex_1.jpg')."
        )

    known_encodings = []
    known_names = []

    for filename in os.listdir(faces_dir):
        image_path = faces_dir / filename

        try:
            image = face_recognition.load_image_file(str(image_path))
            encoding = face_recognition.face_encodings(image)
        except Exception as exc:
            print(f"Warning: skipping '{filename}': {exc}")
            continue

        if len(encoding) > 0:
            known_encodings.append(encoding[0])
            known_names.append(filename.split("_")[0])

    return known_encodings, known_names


def run_face_recognition(faces_dir=None):
    """Recognize faces from the default webcam and display their labels."""
    known_encodings, known_names = load_known_faces(faces_dir)

    if known_encodings:
        print(f"Loaded {len(known_encodings)} reference face(s).")
    else:
        print("Warning: no usable reference faces were found.")
        print("All detected faces will be labeled 'Unknown'.")
        print("Add images to the faces/ directory to recognize people by name.")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        cap.release()
        print("Error: could not open the webcam (camera index 0).")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: could not read a frame from the webcam.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    match_index = np.argmax(matches)
                    name = known_names[match_index]

                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    name,
                    (left, top - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
