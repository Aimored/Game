

from pathlib import Path
import subprocess

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\alexp\OneDrive\desktop\runner\assets menu\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("720x480")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 480,
    width = 720,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    365.3076970693364,
    244.51054739952087,
    image=image_image_1
)



def open_game():
    window.destroy()
    subprocess.Popen(['python', 'game.py'])
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_game,
    relief="flat"
)
button_1.place(
    x=363.0,
    y=187.0,
    width=319.0,
    height=71.0
)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=360.0,
    y=283.0,
    width=317.0,
    height=66.0
)

def close_window():
    window.destroy()


button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=close_window,
    relief="flat"
)
button_3.place(
    x=359.0,
    y=373.0,
    width=317.0,
    height=65.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    218.0,
    237.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    329.0,
    62.0,
    image=image_image_3
)
window.resizable(False, False)
window.mainloop()
