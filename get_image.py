import requests
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def get_top_image_links(query, num_images, api_key, cx):
    # Define the API endpoint and parameters
    api_endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image",
        "num": num_images
    }

    # Send the API request and get the response JSON
    response = requests.get(api_endpoint, params=params).json()
    # Extract the image URLs from the response JSON
    image_links = [item["link"] for item in response["items"]]

    # Return the list of image links
    return image_links

if __name__ == "__main__":
    # Define the query you want to search for and the number of images to retrieve
    query = "Once upon a time, in a far away land, there lived a young prince."
    num_images = 5
    api_key = "AIzaSyBpNwt6Hjnn1CJs92Asun5YA6RU-XKTYKs"
    cx = "73b9cacaa96374f09"

    # Get the top image links for the query
    image_links = get_top_image_links(query, num_images, api_key, cx)
    print(image_links)

    # create a Tkinter window
    root = Tk()
    root.title("Image Grid")

    # create a 2D grid of Label widgets to hold the images
    labels = [[None for _ in range(3)] for _ in range(2)]
    for i in range(2):
        for j in range(3):
            labels[i][j] = Label(root)
            labels[i][j].grid(row=i, column=j)
    
    # loop through the URLs and draw each image in a Label widget
    # images = [] 
    # for url in image_links:
    #     response = requests.get(url)
    #     images.append(Image.open(BytesIO(response.content)))
    # plt.imshow(images)
    # plt.show()

    for i, url in enumerate(image_links):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((200, 200))
        plt.imshow(img)
        plt.show()
        photo = ImageTk.PhotoImage(img)
        row = i // 3
        col = i % 3
        labels[row][col].configure(image=photo)
        labels[row][col].image = photo
    
    # start the Tkinter main loop
    # root.mainloop()