import cv2
import face_recognition
import numpy as np
import os

# مسیر پوشه‌ای که عکس‌های خودت داخلشه
KNOWN_FACES_DIR = "faces"

# لیست چهره‌های شناخته‌شده و نام‌ها
known_encodings = []
known_names = []

# پردازش تصاویر چهره‌های شناخته‌شده
for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) > 0:
        known_encodings.append(encoding[0])
        known_names.append(filename.split("_")[0])  # استخراج نام از فایل

# باز کردن دوربین
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # تبدیل تصویر به RGB برای face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # پیدا کردن چهره‌ها در فریم جاری
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = np.argmax(matches)  # پیدا کردن بهترین تطابق
            name = known_names[match_index]

        # کشیدن مربع دور چهره و نمایش نام
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # نمایش خروجی
    cv2.imshow("Face Recognition", frame)

    # خروج با کلید 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
