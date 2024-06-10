from pathlib import Path
from tkinter import Tk, Canvas, Label, PhotoImage
import tkinter.messagebox
import random
import time
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets game\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

krest_count = 0
BASE_DELAY = 3000
BASE_SPEED = 10
BACKGROUND_SPEED = 1
GRAVITY = 0.9
INITIAL_VELOCITY = 29
is_jumping = False
vertical_velocity = 0
paused = False
is_protected = False
protect_timer = None

canvas = Canvas(window, bg="#FFFFFF", height=1080, width=2483, bd=0, highlightthickness=0, relief="ridge")

image_image_1 = PhotoImage(file=relative_to_assets("fon.png"))
fon_1 = canvas.create_image(1241.0, 540.0, image=image_image_1)
fon_2 = canvas.create_image(3723.0, 540.0, image=image_image_1)

image_image_5 = PhotoImage(file=relative_to_assets("pers.png"))
walk_images = [
    PhotoImage(file=relative_to_assets("pers.png")),
    PhotoImage(file=relative_to_assets("Walk_2.png")),
    PhotoImage(file=relative_to_assets("Walk_3.png")),
    PhotoImage(file=relative_to_assets("Walk_4.png")),
    PhotoImage(file=relative_to_assets("Walk_3.png")),
    PhotoImage(file=relative_to_assets("Walk_2.png")),
]
nviz_images = [
    PhotoImage(file=relative_to_assets("nviz.png")),
    PhotoImage(file=relative_to_assets("nviz_2.png")),
    PhotoImage(file=relative_to_assets("nviz_3.png")),
    PhotoImage(file=relative_to_assets("nviz_4.png")),
    PhotoImage(file=relative_to_assets("nviz_3.png")),
    PhotoImage(file=relative_to_assets("nviz_2.png")),
]
protect_image = PhotoImage(file=relative_to_assets("protect.png"))
pers = canvas.create_image(1561.0, 724.0, image=image_image_5)

def move_background():
    if paused:
        return
    speed_increment = min(krest_count, 10) + 0.1
    canvas.move(fon_1, BACKGROUND_SPEED + speed_increment, 0)
    canvas.move(fon_2, BACKGROUND_SPEED + speed_increment, 0)
    x1, y1 = canvas.coords(fon_1)
    x2, y2 = canvas.coords(fon_2)
    image_width = image_image_1.width()
    
    if x1 >= canvas.winfo_width() + image_width / 2:
        canvas.coords(fon_1, x2 - image_width, 540.0)
    if x2 >= canvas.winfo_width() + image_width / 2:
        canvas.coords(fon_2, x1 - image_width, 540.0)
    
    window.after(5, move_background)

canvas.place(x=0, y=0)
window.attributes('-fullscreen', True)


canvasWidth = 1920

def jump(event):
    global is_jumping, vertical_velocity
    if not is_jumping and not paused:
        is_jumping = True
        vertical_velocity = INITIAL_VELOCITY
        animate_jump()

def animate_jump():
    global is_jumping, vertical_velocity
    if is_jumping and not paused:
        y_position = canvas.coords(pers)[1] - vertical_velocity
        canvas.coords(pers, canvas.coords(pers)[0], y_position)
        
        vertical_velocity -= GRAVITY
        
        if y_position >= 724.0:
            canvas.coords(pers, canvas.coords(pers)[0], 724.0)
            is_jumping = False
            vertical_velocity = 0
        else:
            window.after(5, animate_jump)

def create_and_move_krest():
    if not paused:
        y_coord = random.choice([random.randint(340, 430), random.randint(700, 800)])  
        krest = canvas.create_image(0, y_coord, image=image_image_3)
        move_krest(krest)
        delay = max(500, 3000 - 75 * min(krest_count, 20))
        window.after(delay, create_and_move_krest)

def create_and_move_shield():
    if not paused:
        y_coord = random.randint(20, 900)  
        shield = canvas.create_image(0, y_coord, image=image_image_4)
        move_shield(shield)
        delay = random.randint(10000, 15000)  
        window.after(delay, create_and_move_shield)

krest_count_label = Label(window, text="пройдено: 0", bg="#FFFFFF", fg="#800080", font=("Helvetica", 16))
krest_count_label.place(x=10, y=10)

def move_krest(krest):
    global is_jumping, paused, krest_count, is_protected
    if paused:
        return
    speed_increment = min(krest_count, 25) + 0.5 
    canvas.move(krest, BASE_SPEED + speed_increment, 0)
    krest_bbox = canvas.bbox(krest)
    pers_bbox = canvas.bbox(pers)

    krest_rect = [krest_bbox[0], krest_bbox[1], krest_bbox[2], krest_bbox[3]]
    pers_rect = [pers_bbox[0], pers_bbox[1], pers_bbox[2]-80, pers_bbox[3]]

    current_image = canvas.itemcget(pers, "image")

    if current_image == str(protect_image):
        if check_collision(krest_rect, pers_rect):
            canvas.delete(krest)
            krest_count += 1
            krest_count_label.config(text=f"пройдено: {krest_count}")
            return
    elif current_image in [str(img) for img in nviz_images]:
        if krest_bbox[2] < 1920:
            window.after(5, move_krest, krest)
        else:
            canvas.delete(krest)
        return
    else:
        if check_collision(krest_rect, pers_rect):
            paused = True
            game_over()
            return

    if krest_bbox[2] < 1920:
        window.after(5, move_krest, krest)
    else:
        canvas.delete(krest)
        krest_count += 1
        krest_count_label.config(text=f"пройдено: {krest_count}")

def move_shield(shield):
    global paused, is_protected, protect_timer
    if paused:
        return
    canvas.move(shield, BASE_SPEED + 5, 0)
    shield_bbox = canvas.bbox(shield)
    pers_bbox = canvas.bbox(pers)

    shield_rect = [shield_bbox[0], shield_bbox[1], shield_bbox[2], shield_bbox[3]]
    pers_rect = [pers_bbox[0], pers_bbox[1], pers_bbox[2]-80, pers_bbox[3]]

    if check_collision(shield_rect, pers_rect):
        canvas.delete(shield)
        if not is_protected:
            canvas.itemconfig(pers, image=protect_image)
            is_protected = True
            if protect_timer:
                window.after_cancel(protect_timer)
            protect_timer = window.after(8000, reset_protection)
        return

    if shield_bbox[2] < 1920:
        window.after(5, move_shield, shield)
    else:
        canvas.delete(shield)

image_image_4 = PhotoImage(file=relative_to_assets("shield.png"))

def game_over():
    tkinter.messagebox.showinfo("Игра закончена", f"Пройдено крестов: {krest_count}")
    global paused
    paused = True
    for item in canvas.find_all():
        if item != pers:
            canvas.delete(item)
    window.after(0, end_game)

def end_game():
    window.destroy()
    subprocess.Popen(['python', 'menu.py'])

def check_collision(rect1, rect2):
    """Проверяет столкновение между двумя прямоугольниками"""
    if (rect1[0] < rect2[2] and 
        rect1[2] > rect2[0] and 
        rect1[1] < rect2[3] and 
        rect1[3] > rect2[1]):
        return True
    return False

ctrl_pressed = False
ctrl_timer = None
last_change_time = 0
RECHARGE_TIME = 5

def change_image(event):
    global ctrl_pressed, ctrl_timer, last_change_time
    if is_protected:
        return
    current_time = time.time()
    if current_time - last_change_time >= RECHARGE_TIME:
        if not ctrl_pressed:
            ctrl_pressed = True
            canvas.itemconfig(pers, image=nviz_images[0])
            ctrl_timer = window.after(2000, reset_image)
            last_change_time = current_time

def reset_image():
    global ctrl_pressed, is_protected
    if ctrl_pressed:
        ctrl_pressed = False
        if not is_protected:
            canvas.itemconfig(pers, image=image_image_5)

def release_ctrl(event):
    global ctrl_pressed, ctrl_timer
    if ctrl_pressed:
        ctrl_pressed = False
        if not is_protected:
            canvas.itemconfig(pers, image=image_image_5)
        if ctrl_timer:
            window.after_cancel(ctrl_timer)
            ctrl_timer = None

def reset_protection():
    global is_protected, protect_timer
    if is_protected:
        is_protected = False
        canvas.itemconfig(pers, image=image_image_5)
    if protect_timer:
        window.after_cancel(protect_timer)
        protect_timer = None

image_image_3 = PhotoImage(file=relative_to_assets("krest.png"))

# Функция для анимации
current_walk_image_index = 0
current_nviz_image_index = 0

def animate_walk():
    global current_walk_image_index, current_nviz_image_index
    if not paused:
        current_image = canvas.itemcget(pers, "image")
        if current_image == str(image_image_5):  # Проверяем, что изображение не является nviz_image или protect_image
            canvas.itemconfig(pers, image=walk_images[0])
            current_walk_image_index = 1
        elif current_image == str(protect_image):
            pass
        else:
            if current_image in [str(img) for img in nviz_images]:  # Изменяем анимацию во время невидимости
                canvas.itemconfig(pers, image=nviz_images[current_nviz_image_index])
                current_nviz_image_index = (current_nviz_image_index + 1) % len(nviz_images)
            else:  # Меняем изображение только при обычной ходьбе
                canvas.itemconfig(pers, image=walk_images[current_walk_image_index])
                current_walk_image_index = (current_walk_image_index + 1) % len(walk_images)
        window.after(200, animate_walk)


window.bind("<space>", jump)
window.bind("<Control_L>", change_image)
window.bind("<Control_R>", change_image)
window.bind("<KeyRelease-Control_L>", release_ctrl)
window.bind("<KeyRelease-Control_R>", release_ctrl)

move_background()
window.after(10, create_and_move_krest)
window.after(10000, create_and_move_shield)
animate_walk()

window.resizable(False, False)
window.mainloop()
