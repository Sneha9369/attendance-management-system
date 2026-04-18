import cv2
import os
from database import cursor

student_id = input("Enter Student ID: ")

cursor.execute("SELECT name FROM students WHERE student_id=?", (student_id,))
data = cursor.fetchone()

if data is None:
    print("Student ID not found")
    exit()

name = data[0]
print("Registering Face for:", name)

path = f"dataset/{student_id}"
os.makedirs(path, exist_ok=True)

cam = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Register Face", frame)
    cv2.imwrite(f"{path}/{count}.jpg", frame)
    count += 1

    if count == 50:
        break

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()

print("Face Registered Successfully")