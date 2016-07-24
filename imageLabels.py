from tkinter import *
from PIL import Image, ImageTk

class ImageLabels():
    def __init__(self, *args): # Args should be strings of images, ex: 'name.jpg'
        self.labels = [] # List of Label objects
        self.images = args # List of image names

    def displayImages(self, position):
        for i in range(len(self.labels)):
            self.labels[i].pack(side=position)

    # Creates image label and appends it to the list
    def labelImage(self, frame, index):
        self.labels.append(makeImgLabel(frame, self.images[index]))

    def length(self):
        return len(self.images)

def makeImgLabel(frame, photo):
    img = ImageTk.PhotoImage(Image.open(photo))
    imgLabel = Label(frame, image=img)
    imgLabel.image = img # Must keep a reference!
    return imgLabel