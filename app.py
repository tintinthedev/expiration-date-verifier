import customtkinter as ctk
from camera import Camera


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.camera = Camera()

        self.geometry("600x600")
        self.title("Expiration date verifier")

        self.create_widgets()
        self.draw_widgets()

        self.mainloop()

    def create_widgets(self):
        self.activate_camera_button = ctk.CTkButton(
            self, text="Activate camera", command=self.camera.activate_camera
        )

    def draw_widgets(self):
        self.activate_camera_button.place(relx=0.5, rely=0.5, anchor="center")
