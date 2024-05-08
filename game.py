from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label
import time
import tkinter.messagebox
import random
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets game\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
window = Tk()
window.geometry("1920x1080")

window.configure(bg = "#FFFFFF")
BASE_DELAY = 3000
BASE_SPEED = 10
BACKGROUND_SPEED = 1
GRAVITY = 0.9
INITIAL_VELOCITY = 29
is_jumping = False
vertical_velocity = 0
paused = False 
canvas = Canvas(window,bg = "#FFFFFF",height = 1080,width = 2483,bd = 0, highlightthickness = 0, relief = "ridge")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(1241.0, 540.0, image=image_image_1)
image_2 = canvas.create_image(3723.0, 540.0, image=image_image_1)

def move_background():
    speed_increment = min(krest_count, 10) + 0.1
    canvas.move(image_1, BACKGROUND_SPEED + speed_increment, 0)
    canvas.move(image_2, BACKGROUND_SPEED + speed_increment, 0)
    x1, y1 = canvas.coords(image_1)
    x2, y2 = canvas.coords(image_2)
    image_width = image_image_1.width()
    
    if x1 >= canvas.winfo_width() + image_width / 2:
        canvas.coords(image_1, x2 - image_width, 540.0)
    if x2 >= canvas.winfo_width() + image_width / 2:
        canvas.coords(image_2, x1 - image_width, 540.0)
    
    window.after(1, move_background)
    

canvas.place(x = 0, y = 0)
def toggle_fullscreen(event):
    if window.attributes('-fullscreen'):
        window.attributes('-fullscreen', False)
        window.overrideredirect(False)
    else:
        window.attributes('-fullscreen', True)
        window.overrideredirect(True)
canvasWidth=1920

def jump(event):
    global is_jumping, vertical_velocity
    if not is_jumping:
        is_jumping = True
        vertical_velocity = INITIAL_VELOCITY
        animate_jump()

def animate_jump():
    global is_jumping, vertical_velocity
    if is_jumping:
        y_position = canvas.coords(pers)[1] - vertical_velocity
        canvas.coords(pers, 1561.0, y_position)
        
        vertical_velocity -= GRAVITY
        
        if y_position >= 724.0:
            canvas.coords(pers, 1561.0, 724.0)
            is_jumping = False
            vertical_velocity = 0
        else:
            window.after(10, animate_jump)  




def create_and_move_krest():
    if not paused:
        y_coord = random.choice([random.randint(340, 430), random.randint(700, 800)])  
        krest = canvas.create_image(0, y_coord, image=image_image_3)
        move_krest(krest)
        delay = max(500, 3000 - 75 * min(krest_count, 20))
        window.after(delay, create_and_move_krest)

krest_count_label = Label(window, text="пройдено: 0", bg="#FFFFFF", fg="#800080", font=("Helvetica", 16))
krest_count_label.place(x=10, y=10)
krest_count = 0
def move_krest(krest):
    global is_jumping, paused, krest_count
    if paused:
        return
    speed_increment = min(krest_count, 25) + 0.5 
    canvas.move(krest, BASE_SPEED + speed_increment, 0)
    krest_bbox = canvas.bbox(krest)
    pers_bbox = canvas.bbox(pers)

    krest_rect = [krest_bbox[0], krest_bbox[1], krest_bbox[2], krest_bbox[3]]
    pers_rect = [pers_bbox[0], pers_bbox[1], pers_bbox[2]-80, pers_bbox[3]]

    if check_collision(krest_rect, pers_rect):
        paused = True
        game_over()
        return

    if krest_bbox[2] < 1920:
        window.after(10 , move_krest, krest)
    else:
        canvas.delete(krest)
        krest_count += 1
        krest_count_label.config(text=f"пройдено: {krest_count}")
image_image_4 = PhotoImage(file=relative_to_assets("image_2.png"))

def create_and_move_image_2():
    image_2 = canvas.create_image(0, 540, image=image_image_4)  
    move_image_2(image_2)

    window.after(10000, create_and_move_image_2)

def move_image_2(image):
    canvas.move(image, 10, 0)
    x, y = canvas.coords(image)
    
    if x < canvas.winfo_width():
        window.after(1, move_image_2, image)  #
    else:
        canvas.delete(image)

create_and_move_image_2()
def game_over():
    choice = tkinter.messagebox.askquestion("Игра закончена", "Хотите заново?")
    if choice == "yes":
        # Если выбрано "да", начинаем игру зановоя
        # restart_game()
        print('пока')
        window.destroy()
    else:
        # Если выбрано "нет"?
        window.destroy()
def check_collision(rect1, rect2):
    """Проверяет столкновение между двумя прямоугольниками"""
    if (rect1[0] < rect2[2] and 
        rect1[2] > rect2[0] and 
        rect1[1] < rect2[3] and 
        rect1[3] > rect2[1]):
        return True
    return False



image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_image_5 = PhotoImage(file=relative_to_assets("image_4.png"))
pers = canvas.create_image(1561.0,724.0,image=image_image_5)

toggle_fullscreen(event=toggle_fullscreen)
window.bind("<Escape>", toggle_fullscreen)
move_background()
window.after(10, create_and_move_krest)
window.bind("<Escape>", toggle_fullscreen)
window.bind("<space>", jump)
window.resizable(False, False)
window.mainloop()
