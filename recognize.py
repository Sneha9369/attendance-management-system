import cv2
import face_recognition
import pickle
from datetime import datetime
import sqlite3

# DB connect (direct — no circular import)
conn = sqlite3.connect("ams.db", check_same_thread=False)
cursor = conn.cursor()

def take_attendance():

    with open("trainer/encodings.pkl", "rb") as f:
        known_faces, known_names = pickle.load(f)

    cam = cv2.VideoCapture(0)
    marked = False

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for face_encoding in encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            if True in matches:
                match_index = matches.index(True)
                student_id = known_names[match_index]

                now = datetime.now()
                date = now.strftime("%Y-%m-%d")

                # ✅ FIXED INSERT (ONLY 4 columns)
                cursor.execute(
                    "INSERT INTO attendance (student_id, subject, date, status) VALUES (?,?,?,?)",
                    (student_id, "Face", date, "Present")
                )
                conn.commit()

                print(student_id, "Attendance Marked")
                marked = True
                break

        cv2.imshow("Attendance", frame)

        if cv2.waitKey(1) == 27 or marked:
            break

    cam.release()
    cv2.destroyAllWindows()


# TEST CAMERA
def detect_face():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    take_attendance()