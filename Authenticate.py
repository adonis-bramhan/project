import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition

class CameraApp:
    def __init__(self, root, account_number):
        self.root = root
        self.root.title("Authentication App")
        self.account_number = account_number

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)

        # Create a frame to display the camera feed
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a label to display the camera feed
        self.label = tk.Label(self.frame)
        self.label.pack()

        # Create a button to capture photo
        self.capture_button = tk.Button(self.root, text="Capture Photo", command=self.capture_photo)
        self.capture_button.pack(pady=10)

        # Show camera feed
        self.show_camera_feed()

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert frame to PIL format
            img = Image.fromarray(frame)
            # Convert PIL image to Tkinter format
            img_tk = ImageTk.PhotoImage(image=img)
            # Update label with the new image
            self.label.img_tk = img_tk
            self.label.config(image=img_tk)
            self.root.after(10, self.show_camera_feed)

    def authenticate(self):
        try:
            folder_path = os.path.join("Face Data", str(self.account_number))
            known_image = face_recognition.load_image_file(os.path.join(folder_path, "face.jpg"))
            unknown_image = face_recognition.load_image_file(os.path.join(folder_path, "test.jpg"))

            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            if results == [True]:
                return 1
            else:
                return 0
        except IndexError:
            return 0

    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB color space
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create folder for the account number if it doesn't exist
            folder_path = os.path.join("Face Data", str(self.account_number))
            if not os.path.exists(folder_path):
                pass
            
            # Save the captured image inside the folder
            file_path = os.path.join(folder_path, "test.jpg")
            if file_path:
                # Convert the RGB frame back to BGR before saving
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, frame_bgr) #saving of file
            
            # Release the webcam and close the window
            self.cap.release()
            self.root.destroy()
    


# Create the main Tkinter window
root = tk.Tk()
# Replace 'account_number' with the desired account number
account_number = 123  
# Create an instance of CameraApp
app = CameraApp(root, account_number)
# Run the Tkinter event loop
root.mainloop()

ans = app.authenticate()
print(ans)
