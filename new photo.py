import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import face_recognition

class CameraApp:
    def __init__(self, root, acc):
        self.acc = acc
        self.root = root
        self.root.title("Add/Moodify Face")

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)

        # Create a frame to display the camera feed
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a label to display the camera feed
        self.label = tk.Label(self.frame)
        self.label.pack()

        # Create a button to capture photo
        self.capture_button = tk.Button(self.root, text="Capture Photo", command=lambda: self.capture_photo(self.acc))
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

            # Calculate the center position of the screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - self.root.winfo_width()) // 2
            y = (screen_height - self.root.winfo_height()) // 2
            self.root.geometry("+{}+{}".format(x, y))

            self.root.after(10, self.show_camera_feed)

    def capture_photo(self, number):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB color space
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create a folder with the given number if it doesn't exist
            folder_name = "Face Data/"+str(number)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            
            # Delete old image if exists
            old_image_path = os.path.join(folder_name, "face.jpg")
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            
            # Save the captured image inside the folder
            file_path = os.path.join(folder_name, "face.jpg")
            if file_path:
                # Convert the RGB frame back to BGR before saving
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, frame_bgr) #saving of file
            
            # Release the webcam
            self.cap.release()
             # Create a success screen
            self.success_screen()

    def success_screen(self):
        # Destroy the root window
        self.root.destroy()

        # Create a new Tkinter window for success message
        success_root = tk.Tk()
        success_root.title("Success")

        # Get the screen width and height
        screen_width = success_root.winfo_screenwidth()
        screen_height = success_root.winfo_screenheight()

        # Calculate the x and y position to center the window
        x = (screen_width - 200) / 2
        y = (screen_height - 100) / 2

        # Set the position of the window
        success_root.geometry('200x100+%d+%d' % (x, y))

        # Create label for success message
        success_label = tk.Label(success_root, text="Photo Captured Successfully!")
        success_label.pack(pady=20, padx=20, anchor='center')

        # Run the Tkinter event loop for the success screen
        success_root.mainloop()


# Create the main Tkinter window
root = tk.Tk()

# Replace 'acc_no' with the desired account number
acc_no = 123

# Create an instance of CameraApp
app = CameraApp(root, acc_no)
# Run the Tkinter event loop
root.mainloop()
