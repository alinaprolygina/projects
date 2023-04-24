import tkinter as tk
import tkinter.filedialog as filedialog
import pydicom
import os
from PIL import Image, ImageTk

class DicomViewer:
    def __init__(self, root):
        self.root = root
        self.images = []
        self.current_image = 0
        self.folder_path = ""

        self.title = root.title("DICOM Viewer")

        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        

        # Create canvas to display images
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.scale = tk.Scale(self.root, from_=1, to=10, orient="horizontal", command=self.zoom)
        self.canvas.create_window(self.canvas.winfo_width() - 50, self.canvas.winfo_height() - 50, window=self.scale, anchor='ne')
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw")

        # Create frame to hold image buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=2, sticky="nsew")

        # Create button to select folder
        self.select_button = tk.Button(self.button_frame, text="Load folder", font=("Helvetica", 20), command=self.select_folder)
        self.select_button.pack(side="top", padx=10, pady=10)

        # Create button to display previous image
        self.previous_button = tk.Button(self.button_frame, text="Previous", font=("Helvetica", 20), command=self.previous_image)
        self.previous_button.pack(side="left", padx=10, pady=0)

        # Create button to display next image
        self.next_button = tk.Button(self.button_frame, text="Next", font=("Helvetica", 20), command=self.next_image)
        self.next_button.pack(side="right", padx=10, pady=0)

        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.root.bind("<Configure>", self.on_window_resize)
        
    def select_folder(self):
        # Ask user to select folder
        self.folder_path = tk.filedialog.askdirectory()

        # Load DICOM files from folder
        self.load_images()

    def load_images(self):
        # Clear canvas and images list
        self.canvas.delete("all")
        self.images = []

        # Load DICOM files from folder
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".dcm"):
                # Load DICOM file
                dicom_file = pydicom.dcmread(file_path)
                
                # Convert DICOM image to PIL image
                image = Image.fromarray(dicom_file.pixel_array)
                
                image = image.convert("RGB")
                image = image.resize((812, 812), resample=Image.LANCZOS)

                # Add PIL image to images list
                #self.images.append(ImageTk.PhotoImage(image))
                # Convert PIL image to PhotoImage
                photo_image = ImageTk.PhotoImage(image)
                print(photo_image)

            # Add PhotoImage to images list
            self.images.append(photo_image)
                
        # Display first image
        if len(self.images) > 0:
            self.current_image = 0
            self.canvas.config(width=self.images[self.current_image].width(), height=self.images[self.current_image].height())
            self.canvas.create_image(0, 0, image=self.images[self.current_image], anchor="nw")
            

    def previous_image(self):
        # Display previous image
        if self.current_image > 0:
            self.current_image -= 1
            self.canvas.create_image(0, 0, image=self.images[self.current_image], anchor="nw")

    def next_image(self):
        # Display next image
        if self.current_image < len(self.images) - 1:
            self.current_image += 1
            self.canvas.create_image(0, 0, image=self.images[self.current_image], anchor="nw")

    def on_canvas_configure(self, event):
        # Update scroll region of canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def zoom(self, value):
        image = self.images[self.current_image]
        old_pil_image = image._PhotoImage__photo
        new_pil_image = Image.fromarray(old_pil_image)
        new_pil_image = new_pil_image.resize((new_pil_image.width * int(value), new_pil_image.height * int(value)))
        new_photo_image = ImageTk.PhotoImage(new_pil_image)
        self.canvas.itemconfig(self.image_on_canvas, image=new_photo_image)
        self.images[self.current_image] = new_photo_image
        del old_pil_image




    def on_window_resize(self, event):
        # Get current image
        image = self.images[self.current_image]
        # Get old PIL image
        old_pil_image = image._PhotoImage__photo
        # Create new PIL image by resizing the old one
        new_pil_image = old_pil_image.copy()
        new_pil_image = new_pil_image.resize((new_pil_image.width * int(value), new_pil_image.height * int(value)))
        # Create new PhotoImage from the new PIL image
        new_image = ImageTk.PhotoImage(new_pil_image)
        # Update the canvas item with the new image
        self.canvas.itemconfig(self.image_on_canvas, image=new_image)
        # Replace the current image in the images list with the new image
        self.images[self.current_image] = new_image
        # Delete the old PIL image to avoid memory leak
        del old_pil_image

if __name__ == "__main__":
    root = tk.Tk()
    app = DicomViewer(root)
    root.mainloop()

