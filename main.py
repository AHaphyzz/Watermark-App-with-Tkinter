from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO

# initialize tk screen
app = Tk()
app.title("Image Watermark App")
app.geometry("700x700")
app.configure(bg="#2c3e50")

# setting global variables
image_on_screen = None
my_image = None
text = None


# ------------------Functions--------------
def get_web_image():
    try:
        web_link = url.get("1.0", "end")
        response = requests.get(web_link, "")
        response.raise_for_status()
        target_width, target_height = 440, 300
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        resized_img = img.resize((target_width, target_height),
                                 Image.Resampling.LANCZOS)  # to resize with high quality
        return resized_img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def upload_image():
    """upload directly from desktop"""
    file_path = filedialog.askopenfilename(title="Upload from desktop",
                                           filetypes=[("image file", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    img = Image.open(file_path)
    target_width, target_height = 440, 300
    resized_img = img.resize((target_width, target_height),
                             Image.Resampling.LANCZOS)  # to resize with high quality

    global my_image
    my_image = resized_img
    if my_image is not None:
        my_photo = ImageTk.PhotoImage(my_image)
        canvas.config(width=440, height=300)
        canvas.create_image(my_photo.width() // 2, my_photo.height() // 2, image=my_photo)
        canvas.image = my_photo  # saves the canvas image
        return my_photo
    else:
        print("Failed to load image. Please check the URL.")


def display_image():
    global image_on_screen, my_image
    my_image = get_web_image()
    if my_image is not None:
        my_photo = ImageTk.PhotoImage(my_image)
        canvas.config(width=440, height=300)
        canvas.create_image(my_photo.width() // 2, my_photo.height() // 2, image=my_photo)
        canvas.image = my_photo  # saves the canvas image
        return my_photo
    else:
        print("Failed to load image. Please check the URL.")


def add_watermark():
    global text
    text = wtm_text.get("1.0", "end").strip()
    # canvas.create_rectangle(150, 180, 250, 220, fill="black", outline="", stipple="gray75")
    canvas.create_text(70, 270, text=text, font=("Helvetica", 16, "normal"), fill="white")


def save_image():
    global my_image
    if my_image is None:
        return

    if text is None:
        return

    try:
        wtm_image = my_image.copy()
        draw = ImageDraw.Draw(wtm_image)
        # Use Pillow's default font if the specific font is unavailable
        try:
            font = ImageFont.truetype("arial.ttf", 20)  # Adjust font size or file as needed
        except IOError:
            font = ImageFont.load_default()  # Use default font if the specified one is not found

        text_position = (70, 230)  # Adjust based on canvas layout
        draw.text(text_position, text=text, fill="white", font=font)

        # Save the final watermarked image
        save_path = "watermarked_image22.png"
        wtm_image.save(save_path)
        print(f"Image saved as {save_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


# ----------------------------GUI--------------------------
# Title
title_frame = Frame(app, bg="#2c3e50")
title_frame.pack(pady=20)
title_label = Label(title_frame, text="Add Watermark to Your Image", fg="#ecf0f1",
                    bg="#2c3e50", font=("Arial", 18, "bold"))
title_label.pack()

# URL text
add_text_frame = Frame(app, bg="#2c3e50")
add_text_frame.pack(pady=10)
add_text_label = Label(add_text_frame, text="Image URL:", fg="#ecf0f1",
                       bg="#2c3e50", font=("Arial", 12, "bold"))
add_text_label.pack(side=LEFT, pady=5, padx=(40, 10))

url = Text(add_text_frame, height=1, width=52)
url.config(bg="#34495e", fg="#ecf0f1", relief=FLAT)
url.pack(side=LEFT, pady=5)

get_img_btn = Button(add_text_frame, text="Get Image", bg="#2980b9", width="14", fg="white", pady=4, padx=4, relief=FLAT,
                     font=("Arial", 10, "bold"), command=display_image)
get_img_btn.pack(side=LEFT, pady=5, padx=(10, 40))

# upload frame
upload_frame = Frame(app, bg="#2c3e50")
upload_frame.pack(pady=10)
upload_btn = Button(upload_frame, text="Upload from Desktop", bg="#2980b9", width="20", fg="white", pady=4, padx=4,
                    relief=FLAT, font=("Arial", 10, "bold"), command=upload_image)
upload_btn.pack(side=LEFT, pady=5, padx=10)

# Canvas frame
canvas_frame = Frame(app, bg="#2c3e50")
canvas_frame.pack(pady=20)
canvas = Canvas(canvas_frame, width=440, height=300, bg="#7f8c8d", highlightthickness=0)
canvas.pack()

# Watermark frame
wtm_text_frame = Frame(app, bg="#2c3e50")
wtm_text_frame.pack(pady=10)
wtm_text_label = Label(wtm_text_frame, text="Watermark text:", fg="#ecf0f1",
                       bg="#2c3e50", font=("Arial", 12, "bold"))
wtm_text_label.pack(side=LEFT, pady=5, padx=10)

wtm_text = Text(wtm_text_frame, height=1, width=36)
wtm_text.config(bg="#34495e", fg="#ecf0f1", relief=FLAT)
wtm_text.pack(side=LEFT, pady=5)

# save frame
save_wtm_frame = Frame(app, bg="#2c3e50")
save_wtm_frame.pack(pady=20)
wtm_btn = Button(save_wtm_frame, text="Add Watermark", bg="#27ae60", fg="white", width="14", pady=4, padx=4,
                 font=("Arial", 10, "bold"), relief=FLAT, command=add_watermark)
wtm_btn.pack(side=LEFT, pady=5, padx=10)

save_wtm_btn = Button(save_wtm_frame, text="Save Image", bg="#e74c3c", fg="white", width="14", pady=4, padx=4,
                      font=("Arial", 10, "bold"), relief=FLAT, command=save_image)
save_wtm_btn.pack(side=LEFT, pady=5, padx=10)

app.mainloop()
