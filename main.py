# Flashcard GUI for viewing flashcards

from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
BLACK = '#000000'
CURRENT_CARD = {}
TO_LEARN = {}

try:
    data = pandas.read_csv("./data/Spanish_words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/spanish_words.csv")
    TO_LEARN = original_data.to_dict(orient='records')
else:
    TO_LEARN = data.to_dict(orient='records')

# -------------------------- Flashcard Functions -------------------------- #


# Turning to the next card
def next_card():

    global CURRENT_CARD, flip_timer
    window.after_cancel(flip_timer)  # cancels flip timer
    CURRENT_CARD = random.choice(TO_LEARN)
    # call new 'language' word to flashcard
    FlashCard.itemconfig(card_title, text='Spanish', fill=BLACK)
    FlashCard.itemconfig(card_word, text=CURRENT_CARD['Spanish'], fill=BLACK)
    FlashCard.itemconfig(card_background, image=flashcard_front)
    # runs timer to flip card after 5 seconds
    flip_timer = window.after(5000, func=flip_card)


# Flips card and then calls new word to flashcard
def flip_card():

    FlashCard.itemconfig(card_title, text='English', fill=WHITE)
    FlashCard.itemconfig(card_word, text=CURRENT_CARD['English'], fill=WHITE)
    FlashCard.itemconfig(card_background, image=flashcard_back)


# Function tied to green checkmark
# Removes word from bank once if it is known
def is_known():

    TO_LEARN.remove(CURRENT_CARD)
    words = pandas.DataFrame(TO_LEARN)
    words.to_csv('./data/Spanish_words_to_learn.csv', index=False)
    next_card()  # moves to the next card

# -------------------------- UI Section -------------------------- #


window = Tk()
window.title("Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(5000, func=flip_card)

# Flashcards setup front and back
flashcard_front = PhotoImage(file='./images/card_front.png')
flashcard_back = PhotoImage(file='./images/card_back.png')
FlashCard = Canvas(height=526, width=800, highlightthickness=0,
                   highlightbackground=BACKGROUND_COLOR, bg=BACKGROUND_COLOR)
card_background = FlashCard.create_image(400, 265, anchor='center', image=flashcard_front)
card_title = FlashCard.create_text(400, 150, text='', anchor='center', fill=BLACK, font=('Arial', 45, 'italic'))
card_word = FlashCard.create_text(400, 280, text='', anchor='center', fill=BLACK, font=('Arial', 60, 'bold'))
FlashCard.grid(row=0, column=0, columnspan=2)

# red x button config and setup
red_x = PhotoImage(file='./images/wrong.png')
x_button = Button(image=red_x, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_card)
x_button.grid(row=1, column=0)

# green check button config and setup
green_check = PhotoImage(file='./images/right.png')
green_button = Button(image=green_check, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=is_known)
green_button.grid(row=1, column=1)

# runs next card
next_card()


window.mainloop()
