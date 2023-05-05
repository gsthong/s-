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
