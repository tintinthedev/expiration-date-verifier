import cv2
from CTkMessagebox import CTkMessagebox
import pytesseract
import datetime
import re


class Camera:
    def __init__(self):
        self.camera_capture: None | cv2.VideoCapture = None

    def activate_camera(self):
        self.check_for_cameras()

        while True:
            ret, frame = self.camera_capture.read()

            if not ret:
                # TODO: Warn the user about the disconnected camera
                self.camera_capture.release()
                break

            grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_text = pytesseract.image_to_string(grayscale_frame)
            self.find_expiration_date_in_text(frame_text)
            # print(frame_text)

            cv2.imshow("frame", grayscale_frame)

            if cv2.waitKey(1) == ord("q"):
                break

    def check_for_cameras(self):
        self.camera_capture = cv2.VideoCapture(0)

        if not self.camera_capture.isOpened():
            no_camera_answer = CTkMessagebox(
                title="ERROR",
                message="No camera available. Please connect a camera.",
                option_1="Quit",
                option_2="Ok",
            )

            if no_camera_answer.get() == "Quit":
                exit()

            self.check_for_cameras()

    def find_expiration_date_in_text(self, text: str):
        # TODO: Add the possibility for the user to choose the date format
        # on the app's menu

        print(text)

        # TODO: Maybe find a better way to get the exp. date using regex
        expiration_date = re.findall(
            r"\b(?:val|VAL)\s+(\d{2})/(\d{2})/(\d{2}|\d{4})\b", text
        )

        if len(expiration_date) == 0:
            return

        # [('21', '10', '24')]
        expiration_day = expiration_date[0][0]
        expiration_month = expiration_date[0][1]
        expiration_year = expiration_date[0][2]

        # FIX: Find a way to make it work without hard coding the first 2 digits of the year
        if len(expiration_year) == 2:
            expiration_year = f"20{expiration_year}"

        today = datetime.date.today()
        expiration_date = datetime.date(
            int(expiration_year), int(expiration_month), int(expiration_day)
        )

        print(today, expiration_date)

        if expiration_date == today:
            print("EXPIRES TODAY")
        elif expiration_date > today:
            print("DID NOT EXPIRE")
        else:
            print("EXPIRED")
