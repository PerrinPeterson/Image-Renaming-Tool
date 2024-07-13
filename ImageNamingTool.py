import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Tk, Entry, Button, Label, ttk

PATH = "Infinitode 2\\temp\\"


# Function to display the next image
def display_next_image():
    global image_index
    if image_index < len(image_files):
        image = Image.open(PATH + image_files[image_index])
        img = image.resize((image.width * 3, image.height * 3))
        my_image = ImageTk.PhotoImage(img)
        label.configure(image=my_image)
        label.image = my_image
        update_progress_bar()
        update_current_name_box()
    else:
        root.quit()

def update_current_name_box():
    global image_index
    currentName["text"] = image_files[image_index].split("(")[0]

def update_progress_bar():
    global image_index, progress
    progress["value"] = image_index
    root.update_idletasks()

def back_one(*args):
    global image_index
    if image_index > 0:
        image_index -= 1
    display_next_image()

# Function to save the image with the entered number
def save_image(*args):
    #TODO: Handle images with the same number
    global image_index, image_files
    number = entry.get()
    current_name = image_files[image_index]
    #If the number is empty, we don't change the name
    if number == "":
        image_index += 1
        entry.delete(0, 'end')
        display_next_image()
        return
    new_name = PATH + number + "().png"
    # try to rename the file, if it fails, we add a number to the name
    i = 1
    try:
        os.rename(PATH + current_name, new_name)
    except:
        while True:
            new_name = PATH + number + "(" + str(i) + ").png"
            try:
                os.rename(PATH + current_name, new_name)
                break
            except:
                i += 1
    #Now we change the name in the list
    image_files[image_index] = new_name.split("\\")[-1] #for the back button functionality
    image_index += 1
    entry.delete(0, 'end')
    display_next_image()
    



def open_image():
    global image_index
    image = Image.open(PATH + image_files[image_index])
    image.show()
    image_index += 1

# Get the list of image files in the LiveTestData folder
image_files = [f for f in os.listdir(PATH) if f.endswith(".png")]


# Initialize variables
image_index = 0
image = None

# Create the GUI
root = Tk()
root.title("Image Naming Tool")
root.geometry("600x400")

#image box
image = Image.open(PATH + image_files[image_index])
img = image.resize((300, 300))
my_image = ImageTk.PhotoImage(img)
label = tk.Label(root, image=my_image)
label.pack()

back = tk.PhotoImage()
currentName = Label(root, text=image_files[image_index], image=back, width=300, height=100, compound="c", bg = "grey", padx=10, pady=10, font=("Arial", 40))
currentName.pack()


entry = Entry(root)
entry.pack()
entry.bind("<Return>", save_image)

backButton = Button(root, text="Back", command=back_one)
backButton.pack()

button = Button(root, text="Save", command=save_image)
button.pack()




#TODO: add a progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress["value"] = 0
progress["maximum"] = len(image_files)
progress.pack()


# Display the first image
display_next_image()

# Start the GUI event loop
root.mainloop()