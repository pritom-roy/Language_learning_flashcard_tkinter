from tkinter import Tk, PhotoImage, Button, Canvas
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv(filepath_or_buffer="data/yet_to_learn")
except pandas.errors.EmptyDataError or FileNotFoundError:
    data = pandas.read_csv(filepath_or_buffer="data/french_words.csv")

data = data.to_dict(orient="records")

new_card = {}


def next_card():
    if len(data) != 0:
        global new_card, timer
        window.after_cancel(timer)
        new_card = random.choice(data)
        canvas.itemconfig(upper_text, text="French", fill="black")
        canvas.itemconfig(lower_text, text=new_card["French"], fill="black")
        canvas.itemconfig(beckground, image=front_img)
        timer = window.after(ms=3000, func=flip_card)
    else:
        window.after_cancel(timer)


def flip_card():
    canvas.itemconfig(beckground, image=back_img)
    canvas.itemconfig(upper_text, text="English", fill="white")
    canvas.itemconfig(lower_text, text=new_card["English"], fill="white")


def know_that_card():
    try:
        data.remove(new_card)
    except:
        canvas.itemconfig(upper_text, text="Wow", fill="black")
        canvas.itemconfig(lower_text, text="You know every word in the list", fill="black",
                          font=("Verdana", 25, "bold"))
    unknown_word = pandas.DataFrame(data)
    unknown_word.to_csv("data/yet_to_learn", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(padx=20, pady=20, background=BACKGROUND_COLOR)

front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
button_right_img = PhotoImage(file="images/right.png")
button_wrong_img = PhotoImage(file="images/wrong.png")

canvas = Canvas(height=526, width=800)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
beckground = canvas.create_image(400, 263, image=front_img)
upper_text = canvas.create_text(400, 150, text="", font=("Verdana", 30, "italic"))
lower_text = canvas.create_text(400, 263, text="", font=("Verdana", 50, "bold"))
canvas.grid(column=1, row=1, columnspan=2)

known_button = Button(image=button_right_img, highlightthickness=0, command=know_that_card)
known_button.grid(column=1, row=2)

unknown_button = Button(image=button_wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=2, row=2)

timer = window.after(ms=3000, func=flip_card)
next_card()
window.mainloop()
