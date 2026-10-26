"""Face detection demo using OpenCV's Haar cascade (no identity recognition)."""

import cv2


def run_face_detection():
    """Detect faces from the default webcam and draw bounding boxes."""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if face_cascade.empty():
        print("Error: could not load the Haar cascade face detector.")
        return

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

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Face Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
