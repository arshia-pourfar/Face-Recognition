import cv2

# بارگذاری مدل آماده تشخیص چهره
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# باز کردن دوربین (عدد 0 برای دوربین اصلی لپ‌تاپ)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray , scaleFactor=1.1 , minNeighbors=5, minSize=(30,30))
    
    
    # کشیدن مربع دور چهره‌های شناسایی شده
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    cv2.imshow('Face Detection', frame)
    
    # خروج با فشردن کلید 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()