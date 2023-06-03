import cv2
import streamlit as st

def capture_and_register():
    global cap
    cap = cv2.VideoCapture(0)
    st.write("Hi, let's register your face")
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Register"):
            cv2.imwrite("registered_face.jpg", frame)
            st.success("Successfully registered your face!")
            break
    cap.release()

def detect():
    st.write("Face detection")
    registered_face = cv2.imread("registered_face.jpg")
    if registered_face is None:
        st.warning("No registered face found. Please register your face first.")
        return
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            try:
                res = cv2.matchTemplate(roi_gray, registered_face, cv2.TM_CCOEFF_NORMED)
                if res > 0.8:
                    st.warning("Unlocked. Face recognized.")
                else:
                    st.warning("Face not recognized.")
            except:
                pass
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Stop"):
            break
    cap.release()

if __name__ == '__main__':
    st.title("Face Recognition")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

    if app_mode == "Homepage":
        st.write("Welcome to Face Recognition")
        st.write("Please select a mode from the menu.")
    elif app_mode == "Register":
        capture_and_register()
    elif app_mode == "Detect":
        detect()


import cv2
import streamlit as st

def capture_and_register():
    global cap
    cap = st.camera_input("Take a picture")
    st.write("Hi, let's register your face")
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Register"):
            try:
                cv2.imwrite("registered_face.jpg", frame)
                st.success("Successfully registered your face!")
            except:
                st.warning("Could not save the registered face. Please try again.")
            break
    cap.release()

def detect():
    st.write("Face detection")
    registered_face = cv2.imread("registered_face.jpg")
    if registered_face is None:
        st.warning("No registered face found. Please register your face first.")
        return
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            try:
                res = cv2.matchTemplate(roi_gray, registered_face, cv2.TM_CCOEFF_NORMED)
                if res > 0.8:
                    st.warning("Unlocked. Face recognized.")
                else:
                    st.warning("Face not recognized.")
            except Exception as e:
                st.warning("An error occurred while recognizing the face: {}".format(str(e)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        if st.button("Stop"):
            break
    cap.release()

if __name__ == '__main__':
    st.title("Face Recognition")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

    if app_mode == "Homepage":
        st.write("Welcome to Face Recognition")
        st.write("Please select a mode from the menu.")
    elif app_mode == "Register":
        capture_and_register()
   
import cv2
import numpy as np
import os
import pickle
import streamlit as st

def register():
    global cap
    cap = st.camera_input("Take a picture")
    st.write("Hi, let's register your face")
    while True:
        if cap is not None:
            ret, frame = cap.read()
        else:
            break
        ret, frame = cap.read()

        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")

        st.write("Vui lòng điền thông tin của bạn")
        name = st.text_input("Tên")
        age = st.number_input("Tuổi")
        gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
        if not name or not age or not gender:
            st.write("Vui lòng điền đầy đủ thông tin!")
            continue
        st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Đăng ký")
        image = st.image([])
        if st.button("Đăng ký"):
            image.image(frame)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            if len(face_locations) > 0:
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0] 
                df = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender], "Encoding": [encoding]})
                if os.path.exists("data.csv"):
                    df.to_csv("data.csv", mode="a", header=False, index=False)
                else:
                    df.to_csv("data.csv", index=False)
                st.write("Đăng ký thành công!")
                cap.release()
                break

    cap.release()
def register():
    global cap
    cap = st.camera_input("Take a picture")
    st.write("Hi, let's register your face")
    while True:
        if cap is not None:
            ret, frame = cap.read()
        else:
            break
        if not ret:
            st.warning("Could not read from the camera. Please try again.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, use_column_width=True, channels="RGB")
        st.write("Vui lòng điền thông tin của bạn")
        name = st.text_input("Tên")
        age = st.number_input("Tuổi")
        gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
        if not name or not age or not gender:
            st.write("Vui lòng điền đầy đủ thông tin!")
            continue
        st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Đăng ký")
        image = st.image([])
        if st.button("Đăng ký"):
            image.image(frame)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            if len(face_locations) > 0:
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0] 
                df = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender], "Encoding": [encoding]})
                if os.path.exists("data.csv"):
                    df.to_csv("data.csv", mode="a", header=False, index=False)
                else:
                    df.to_csv("data.csv", index=False)
                st.write("Đăng ký thành công!")
                try:
                    cap.release()
                except AttributeError:
                    pass 
                break
    try:
        cap.release()
    except AttributeError:
        pass  


    
def recognize():
    registered_users = []
    for filename in os.listdir("registered_users"):
        with open(os.path.join("registered_users", filename), "rb") as f:
            user_data = pickle.load(f)
            registered_users.append(user_data)
    
    # Lấy ảnh từ camera
    st.write("Hãy điều chỉnh camera sao cho mặt của bạn nằm giữa khung hình và bấm nút Nhận diện")
    image = st.image([])

    if st.button("Nhận diện"):
        cap = st.camera_input("Take a picture")
        _, frame = cap.read()
        cap.release()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            st.write("Không tìm thấy khuôn mặt trong ảnh. Vui lòng thử lại.")
        else:
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))
                face_img = face_img.reshape(1, -1)
########################################################################################### sử dụng model pickle
                label = model.predict(face_img)[0]
                confidence = model.predict_proba(face_img)[0][label]

                # Hiển thị thông tin người dùng
                if confidence > 0.7:
                    found_user = False
                    for user in registered_users:
                        if user["label"] == label:
                            found_user = True
                            st.write("Xin chào, {}! Tuổi của bạn là {} và giới tính là {}.".format(user["name"], user["age"], user["gender"]))
                            st.write("Tỉ lệ khớp: {:.2f}%".format(confidence * 100))
                            break
                    if not found_user:
                        st.write("Không tìm thấy thông tin người dùng. Vui lòng đăng ký trước khi sử dụng tính năng này.")
                else:
                    st.write("Không tìm thấy thông tin người dùng. Vui lòng đăng ký trước khi sử dụng tính năng này.")
if __name__ == '__main__':
    st.title("Face Recognition")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Register", "Detect"])

    if app_mode == "Homepage":
        st.write("Welcome to Face Recognition")
        st.write("Please select a mode from the menu.")
    elif app_mode == "Register":
        register()
    elif app_mode == "Detect":
        recognize()


import os
import io
import cv2
import numpy as np
import streamlit as st
import face_recognition as fr
from supabase import create_client

class AIFaceReg:
    
    folder_path = f'thongtinnguoidangky/cacheimage'
    bucket_path = 'face_reg_database/FaceImage'
    known_encoding = []
    known_id = []
    
    def __init__(self) -> None:
        url = st.secrets['connect-supabase']['url']
        key = st.secrets['connect-supabase']['key']
        self.cursor = create_client(url,key)

    def FetchData(self) -> None:
        file_list = self.cursor.storage.from_('face_reg_database').list(self.bucket_path)
        st.write(file_list)
        for file in file_list:
            if file['name'].endswith('.jpg'):
                img_file_byte = self.cursor.storage.from_('face_reg_database').download(f'{self.bucket_path}/{file["name"]}')
                img_file = cv2.imdecode(np.frombuffer(img_file_byte, np.uint8), cv2.IMREAD_COLOR)

                tmp_encoding = fr.face_encodings(img_file)[0]
                self.known_encoding.append(tmp_encoding)
                self.known_id.append(int(file['name'].replace('.jpg','')))

    def QueueUpdate(self,img_buffer,id) -> tuple:
        try:
            if img_buffer is None: return (False,'')

            img_path = f'{self.folder_path}/{id}.jpg'
            img_file_byte = img_buffer.getvalue()
            img_file = cv2.imdecode(np.frombuffer(img_file_byte, np.uint8), cv2.IMREAD_COLOR)

            face_loc = fr.face_locations(img_file)
            if len(face_loc) == 0:
                return (False,'Không nhận khuôn mặt')
            elif len(face_loc) > 1:
                return (False,'Có nhiều hơn 1 khuôn mặt')
            
            if os.path.isfile(img_path):
                os.remove(img_path)
            cv2.imwrite(img_path,img_file)
            return (True,'Thành công')
        except:
            return (False,'Đã xảy ra lỗi. Vui lòng thử lại')
        
    def UpdateStorage(self) -> None:
        img_name_list = os.listdir(self.folder_path)
        _bucket_file_list = self.cursor.storage.from_('face_reg_database').list(self.bucket_path)
        _bucket_file_list = [file['name'] for file in _bucket_file_list]
        for img_name in img_name_list:
            img_path = f'{self.folder_path}/{img_name}'
            img_save_path = f'{self.bucket_path}/{img_name}'

            if img_name in _bucket_file_list: # Remove if exist
                self.cursor.storage.from_('face_reg_database').remove(img_save_path)
            
            self.cursor.storage.from_('face_reg_database').upload(img_save_path,img_path,
                                                                {"content-type": "image/jpg"})

    def ClearCache(self) -> None:
        img_name_list = os.listdir(self.folder_path)
        for img_name in img_name_list:
            img_path = f'{self.folder_path}/{img_name}'
            os.remove(img_path)

    def CaptureImage(self) -> None:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                img_name = f"{st.text_input('Name')}_{st.number_input('Age')}_{st.selectbox('Gender', ['Male', 'Female'])}.jpg"
                cv2.imwrite(f"{self.folder_path}/{img_name}", roi_gray)
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.color, self.thickness)
                cv2.putText(frame, img_name, (x, y - 10), self.font, 0.7, self.color, self.thickness)
            cv2.imshow('Capture', frame)
            if cv2.waitKey(1) == 27 or st.button('Clear Photo'):
                break
        cap.release()
        cv2.destroyAllWindows()
def RecognizeImage(self) -> None:
    st.write('### Recognize Your Photo')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            label, confidence = face_recognizer.predict(roi_gray)
            name = os.path.splitext(label)[0]
            if confidence > 100:
                continue
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.color, self.thickness)
            cv2.putText(frame, f'{name}, {confidence:.2f}%', (x, y - 10), self.font, 0.7, self.color, self.thickness)
            st.write(f'Name: {name}')
            st.write(f'Confidence: {confidence:.2f}%')
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 27: # Nhấn phím Esc để thoát khỏi vòng lặp
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    st.set_page_config(page_title='Face Recognition App')
    app = FaceRecognitionApp()
    app.RecognizeImage()

import os
import cv2
import streamlit as st

class FaceRecognizer:
    def __init__(self, recognizer_type='Eigen'):
        self.recognizer_type = recognizer_type
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.color = (255, 0, 0)
        self.thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.face_recognizer = None

    def LoadRecognizer(self, dir_path) -> None:
        if self.recognizer_type == 'Eigen':
         if cv2.__version__.startswith('4'):
             self.face_recognizer = cv2.face.EigenFaceRecognizer_create()
         else:
             self.face_recognizer = cv2.createEigenFaceRecognizer()

        elif self.recognizer_type == 'Fisher':
            self.face_recognizer = cv2.face.FisherFaceRecognizer_create()
        elif self.recognizer_type == 'LBPH':
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read(dir_path + '/face_recognizer.xml')

    def RecognizeImage(self, image) -> tuple:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]
            label, confidence = self.face_recognizer.predict(roi_gray)
            name = os.path.splitext(label)[0]
            if confidence > 100:
                continue
            cv2.rectangle(image, (x, y), (x + w, y + h), self.color, self.thickness)
            cv2.putText(image, f'{name}, {confidence:.2f}%', (x, y - 10), self.font, 0.7, self.color, self.thickness)
            return name, confidence
        return None, None

class RegisterForm:
    def __init__(self):
        self.name = ''
        self.age = ''
        self.gender = ''
        self.image = None
        self.is_registered = False

    def Register(self) -> None:
        if self.name and self.age and self.gender and self.image is not None:
            cv2.imwrite(f'{self.name}_{self.age}_{self.gender}.jpg', self.image)
            st.write('Register done!')
            self.is_registered = True
        else:
            st.write('Please fill in all fields before registering.')

    def ClearForm(self) -> None:
        self.name = ''
        self.age = ''
        self.gender = ''
        self.image = None
        self.is_registered = False

face_recognizer = FaceRecognizer()
register_form = RegisterForm()

st.write('# Face Recognition Demo')

if st.button('Take Photo'):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        register_form.image = frame
        st.write('### Preview Photo')
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels='BGR')
        st.write('### Register Information')
        register_form.name = st.text_input('Name')
        register_form.age = st.text_input('Age')
        register_form.gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        if st.button('Register'):
         register_form.Register()
        if st.button('Clear'):
         register_form.ClearForm()

        if st.button('Load Recognizer'):
           dir_path = st.text_input('Directory path')
           recognizer_type = st.selectbox('Recognizer Type', ['Eigen', 'Fisher', 'LBPH'])
           face_recognizer = FaceRecognizer(recognizer_type=recognizer_type)
           face_recognizer.LoadRecognizer(dir_path)
           st.write('Recognizer loaded!')

        if st.button('Recognize'):
           if face_recognizer.face_recognizer is None:
            st.write('Please load recognizer before recognizing.')
           elif register_form.is_registered is False:
            st.write('Please register before recognizing.')
           else:
            name, confidence = face_recognizer.RecognizeImage(register_form.image)
           if name is None:
            st.write('No face detected.')
           else:
              st.write(f'{name} recognized with {confidence:.2f}% confidence.')
              st.write('### Preview Photo')
              st.image(cv2.cvtColor(register_form.image, cv2.COLOR_BGR2RGB), channels='BGR')

face_recognizer = FaceRecognizer()
face_recognizer.LoadRecognizer('face_recognizer')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if ret:
        name, confidence = face_recognizer.RecognizeImage(frame)
        if name is not None:
            st.write(f'### Recognized Face: {name} ({confidence:.2f}%)')
        else:
            st.write('### Face not recognized')
        cv2.imshow('frame', frame)
    if st.button('Stop'):
        break

    cv2.imshow('frame', frame)
cap.release()


