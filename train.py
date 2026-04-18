import face_recognition
import os
import pickle

known_faces = []
known_names = []

dataset_path = "dataset"

for person in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_faces.append(encodings[0])
            known_names.append(person)
        else:
            print("Face not detected in:", image_path)

with open("trainer/encodings.pkl", "wb") as f:
    pickle.dump((known_faces, known_names), f)

print("Training Complete")