from PIL import Image, ImageTk
import io

class Movie:
  def __init__(self, title, image_data):
    self.title = title
    self.image_data = image_data

  def resize_image(self, width, height):
    img = Image.open(io.BytesIO(self.image_data))
    img = img.resize((width, height))
    return ImageTk.PhotoImage(img)
