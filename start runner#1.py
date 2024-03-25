from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\alexp\OneDrive\desktop\build\build\build\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1000x563")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 563,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    500.0,
    281.0,
    image=image_image_1
)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(500.0, 281.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(210.0, 402.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(788.0, 444.0, image=image_image_3)
def jump(event):
    global y_position, direction
    if event.keysym == "space":
        canvas.move(image_2, 0, direction)
        y_position += direction
        if y_position <= 30:
            direction = 10
        elif y_position >= 452:
            direction = -10
canvas.place(x = 0, y = 0)
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    210.0,
    402.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    788.0,
    444.0,
    image=image_image_3
)
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(184.0, 342.0, image=image_image_2)

direction = 1
y_position = 342
def move_image():
    canvas.move(image_3, -5, 0)
    window.after(25, move_image)

move_image()


window.bind("<KeyPress>", jump)
window.resizable(False, False)
window.mainloop()
