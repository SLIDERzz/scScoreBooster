import ctypes
import json
from tkinter import *


#
#
#           KAN VARA LIKA OSTABILT SOM MITT EX OCH ALLA TALKING STAGES.
#        GJORDE 'getPosTool.py' SOM LÖSNING. SKRIVA IN POSITIONERNA SJÄLV
#
#

class ScreenCrop:
    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.snip_surface = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.master_screen = Tk()

        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

        self.create_screen_canvas()

    def create_screen_canvas(self):
        self.master_screen.deiconify()

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', 0.5)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.master_screen.destroy()
        return event

    def on_button_press(self, event):
        self.start_x = int(self.snip_surface.canvasx(event.x))
        self.start_y = int(self.snip_surface.canvasy(event.y))
        self.end_x = int(self.snip_surface.canvasx(event.x))
        self.end_y = int(self.snip_surface.canvasy(event.y))
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=5, fill="maroon3")

    def on_snip_drag(self, event):
        self.end_x = int(event.x)
        self.end_y = int(event.y)
        self.snip_surface.coords(1, self.start_x, self.start_y, self.end_x, self.end_y)


def getPos():
    """
    Får användaren att völja kamera ui på snapchat.
    Skapar en fil med alla knappar och deras position i det markerade området.
    Sparar alla knappars position i en JSON fil.
    """
    while True:
        canvas = ScreenCrop()
        canvas.master_screen.mainloop()
        print(f"Selected cameraUI coords:\n"
              f"Top-Left:    {canvas.start_x}x{canvas.start_y}\n"
              f"Bottom-Right: {canvas.end_x}x{canvas.end_y}")
        if "y" in input(f'{"_" * 21}\n'
                        'Confirm selected area\n'
                        '["n" to redo / "y" to continue]\n>'
                        '>'):
            break

    w_width = canvas.end_x - canvas.start_x
    w_height = canvas.end_y - canvas.start_y

    # Relative positions (just examples, använd dina korrekta värden)
    takePhoto: tuple[float, float] = (208 / 415, 683 / 738)
    sendToButton: tuple[float, float] = (315 / 415, 704 / 738)
    usernameInputField: tuple[float, float] = (200 / 415, 100 / 738)
    topResults: tuple[float, float] = (375 / 415, 200 / 738)
    sendButton: tuple[float, float] = (209 / 415, 702 / 738)

    positions = {
        "takePhoto": (canvas.start_x + int(w_width * takePhoto[0]),
                      canvas.start_y + int(w_height * takePhoto[1])),
        "sendToButton": (canvas.start_x + int(w_width * sendToButton[0]),
                         canvas.start_y + int(w_height * sendToButton[1])),
        "usernameInputField": (canvas.start_x + int(w_width * usernameInputField[0]),
                               canvas.start_y + int(w_height * usernameInputField[1])),
        "topResults": (canvas.start_x + int(w_width * topResults[0]),
                       canvas.start_y + int(w_height * topResults[1])),
        "sendButton": (canvas.start_x + int(w_width * sendButton[0]),
                       canvas.start_y + int(w_height * sendButton[1]))
    }

    file_name = "ButtonPosition.json"
    with open(file_name, "w") as positionFile:
        json.dump(positions, positionFile)
    print("Positions saved as:", file_name)


if __name__ == '__main__':
    input("Select the CameraUI on snapchat.\n"
          "Press ENTER to start\n> ")
    print("Starting", end="\r")
    getPos()
    print(" " * 10, end="\r")