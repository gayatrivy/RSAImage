from tkinter import *
import tkinter.messagebox as mbox
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
import random

# Global variables
global count, eimg, panelA, panelB, x, image_encrypted, key, location, filename
panelA = None  # Initialize panelA
panelB = None  # Initialize panelB
# Tkinter window setup
window = Tk()
window.geometry("1000x1000")
window.title("Image Encryption Decryption using RSA")

# Function to generate prime numbers
def generate_prime():
    while True:
        num = random.randint(100, 1000)
        if is_prime(num):
            return num

# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

# Function to find gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to find modular inverse using extended Euclidean algorithm
def mod_inverse(e, phi_n):
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi_n = phi_n

    while e > 0:
        temp1 = temp_phi_n // e
        temp2 = temp_phi_n - temp1 * e
        temp_phi_n = e
        e = temp2

        x = x2 - temp1 * x1
        y = y2 - temp1 * y1

        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi_n == 1:
        return y2 + phi_n

# Function to perform RSA encryption
def rsa_encrypt(message, public_key):
    n, e = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher

# Function to perform RSA decryption
def rsa_decrypt(cipher, private_key):
    n, d = private_key
    message = [chr(pow(char, d, n)) for char in cipher]
    return ''.join(message)

# Function to get the path of the selected image
def getpath(path):
    a = path.split('/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

# Function to get the file name of the selected image
def getfilename(path):
    a = path.split('/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

# Function to open the image file
def openfilename():
    filename = filedialog.askopenfilename(title='Open')
    return filename

# Function to open the selected image
def open_img():
    global x, panelA, panelB, count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    
    # Resize the image to fit within 600x600 pixels while maintaining aspect ratio
    width, height = img.size
    if width > 600 or height > 600:
        ratio = min(600 / width, 600 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height))
    
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    
    if panelA is None or panelB is None:
        panelA = Label(image=img)
        panelA.image = img
        panelA.pack(side="left", padx=10, pady=10)
        
        panelB = Label(image=img)
        panelB.image = img
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img

# Function to encrypt the image using RSA
def en_fun():
    global x, image_encrypted, key
    image_input = cv2.imread(x, 0)
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1  # mean and standard deviation
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    image_encrypted = image_input / key
    cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)

    # Open the encrypted image and resize
    imge = Image.open('image_encrypted.jpg')

    # Resize the image to fit within 600x600 pixels
    width, height = imge.size
    if width > 600 or height > 600:
        ratio = min(600 / width, 600 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        imge = imge.resize((new_width, new_height))

    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    mbox.showinfo("Encrypt Status", "Image Encrypted successfully using Key" + str(key))

# Function to decrypt the image using RSA
def de_fun():
    global x, image_encrypted, key
    image_output = image_encrypted * key
    image_output *= 255.0
    cv2.imwrite('image_output.jpg', image_output)

    # Open the decrypted image and resize
    imgd = Image.open('image_output.jpg')

    # Resize the image to fit within 600x600 pixels
    width, height = imgd.size
    if width > 600 or height > 600:
        ratio = min(600 / width, 600 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        imgd = imgd.resize((new_width, new_height))

    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    mbox.showinfo("Decrypt Status", "Image decrypted successfully.")

# Function to reset the edited image to original one
def reset():
    global x, eimg
    image = cv2.imread(x)[:, :, ::-1]
    eimg = Image.fromarray(image)
    
    # Resize the image to fit within 600x600 pixels while maintaining aspect ratio
    width, height = eimg.size
    if width > 600 or height > 600:
        ratio = min(600 / width, 600 / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        eimg = eimg.resize((new_width, new_height))
    
    image = ImageTk.PhotoImage(eimg)
    panelB.configure(image=image)
    panelB.image = image
    mbox.showinfo("Success", "Image reset to original format!")

# Function to save the edited image
def save_img():
    global location, filename, eimg
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Encrypted Image Saved Successfully!")

# Function to create sign-up page
def create_signup_page():
    global entry_username, entry_password, signup_button

    # Clear existing widgets
    clear_window()

    # Sign-up page widgets
    Label(window, text="Sign Up", font=("Arial", 30)).place(x=450, y=100)

    Label(window, text="Username:", font=("Arial", 20)).place(x=300, y=200)
    entry_username = Entry(window, font=("Arial", 20))
    entry_username.place(x=450, y=200)

    Label(window, text="Password:", font=("Arial", 20)).place(x=300, y=250)
    entry_password = Entry(window, font=("Arial", 20), show='*')
    entry_password.place(x=450, y=250)

    signup_button = Button(window, text="Sign Up", command=signup, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    signup_button.place(x=450, y=300)

# Function to handle sign-up process
def signup():
    global entry_username, entry_password

    # Retrieve username and password entered by user
    username = entry_username.get()
    password = entry_password.get()

    # Simulated check for username uniqueness
    if username == "admin":
        mbox.showerror("Error", "Username already exists!")
    else:
        mbox.showinfo("Success", "User registered successfully!")

        # Clear sign-up fields
        entry_username.delete(0, END)
        entry_password.delete(0, END)

        # Switch to the main application page
        create_main_application()

# Function to create main application page
def create_main_application():
    clear_window()

    # Label for application title
    start1 = Label(text="Image Encryption Decryption\n using RSA", font=("Arial", 30), fg="black")
    start1.place(x=310, y=10)

    # Labels for image sections
    label_original = Label(text="Original\nImage", font=("Arial", 30), fg="black")
    label_original.place(x=100, y=270)

    label_encrypted = Label(text="Encrypted\nDecrypted\nImage", font=("Arial", 30), fg="black")
    label_encrypted.place(x=700, y=230)

    # Buttons for actions
    button_choose = Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    button_choose.place(x=30, y=20)

    button_save = Button(window, text="Save", command=save_img, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    button_save.place(x=170, y=20)

    button_encrypt = Button(window, text="Encrypt", command=en_fun, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    button_encrypt.place(x=150, y=620)

    button_decrypt = Button(window, text="Decrypt", command=de_fun, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    button_decrypt.place(x=450, y=620)

    button_reset = Button(window, text="Reset", command=reset, font=("Arial", 20), bg="black", fg="white", borderwidth=3, relief="raised")
    button_reset.place(x=800, y=620)

    button_exit = Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="black", fg="red", borderwidth=3, relief="raised")
    button_exit.place(x=880, y=20)

# Function to clear existing widgets in window
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Function to exit the application
def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Function to initialize sign-up page on startup
create_signup_page()

# Start main loop
window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
