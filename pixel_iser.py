import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import matplotlib.image as IM



#load image in question
"""
#If there is a lot of images you can list them here by putting them in a
#folder called 'art/'.
files = os.listdir("art/")
i = 0
for f in files:
    print(i,": ",f)
    i+=1

n =  int(input("\n"))
file = files[n]

image = plt.imread("art/"+file)
"""

fname = input("What is the path to the image file (include .png or .jpeg as necessary\npath: ")

#load image
image = plt.imread(fname)

#get image dimensions
height = image.shape[0]
width = image.shape[1]

#create a second, entirely blank image
im2 = np.zeros([height,width,3])

if image.shape[2] == 4:
    print("Image uses RGBA")
    #takes into account the possibility that it uses [rgba] not [rgb]
    #and crudley removes the a value. Could definitley be improved
    for h in np.arange(height):
        for w in np.arange(width):
            r = image[h][w][0]
            g = image[h][w][1]
            b = image[h][w][2]
            im2[h][w] = [r,g,b]
    image = im2

#make the size of the initial shape half of the smallest side of the image
if height > width:
    size = int(width/2)
else:
    size = int(height/2)

#create empty array
im = np.zeros([height,width,3])

#check the old image and the new image have the same shape
assert im.shape == image.shape

#init figure
fig = plt.figure()
ax1 = fig.add_subplot(131) #pixel image
ax2 = fig.add_subplot(132) #original
ax3 = fig.add_subplot(133) #Similarity tracker
ax2.imshow(image)


def rand_colour():
    "returns a random colour"
    r = random.random()
    g = random.random()
    b = random.random()
    c = [r,g,b]
    return(c)

def draw_square(im,centre,size,colour):
    "draws a square onto the image"
    x0,y0 = centre
    size = size*2
    
    #bottom corner
    x1 = int(x0 - size/2)
    y1 = int(y0 - size/2)

    #top corner
    x2 = int(x0 + size/2)
    y2 = int(y0 + size/2)
    
    im[y1:y2,x1:x2] = colour
    return(im)

def distance(x1,y1,x2,y2):
    "calculates the distance between (x1,y1) and (x2,y2) coordinates."
    del_x = x2 - x1
    del_y = y2 - y1
    a = del_x**2 + del_y**2
    return(np.sqrt(a))

def pos(lst):
    return([x for x in lst if x>=0] or None)

def draw_circle(im,centre,size,colour):
    "draws circles with radius size"
    n = 0
    x0,y0 = centre
    #size = size*2

    #limit the function to the square with side length 2*size
    #bottom corner
    x1 = int(x0 - size)
    y1 = int(y0 - size)

    #top corner
    x2 = int(x0 + size)
    y2 = int(y0 + size)
    
    x_range = pos(np.arange(x1,x2))
    y_range = pos(np.arange(y1,y2))

    #change the pixel value for all points within the circle
    for x in x_range:
        for y in y_range:
            d = distance(x0,y0,x,y)
            if d <= size:
                try:
                    im[y][x] = colour
                except:
                    pass
    
    #im[y0][x0] = [1,0,0]
    return(im)


def similairity(im1,im2 = image,scale = True):
    if scale == True:
        im1 = im1*255 #the new image is in 0-1 RGB while the original is 0-255
    "a crude function to calculate the difference between two images"
    diff = np.subtract(im1,im2)
    return(np.abs(np.mean(diff)))


init = similairity(im)
goal = similairity(image,scale = False)
print(init, goal)
a = 0
A = [0]
S = [0]

def animate_rand(i,im,height,width,size,init,f = 20):
    if size - i > height//f:
        
        size -= i
        #as i increases (more iterations) the shapes become smaller
    else:
        #return()
        size = height//f #replace "return" with this to make it run indefinitley
    
    for x in np.arange(1):

        #pick a random spot and pick out that pixels colour
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)
        c = image[y][x]
        c = c/255 #ensure rgb values are 0<x<1

        #draw a shape on the new image (change function to change shape)
        im = draw_square(im,(x,y),size,colour = c)

        #calculate similarity
        s = 100*(1-similairity(im)/255) ##not convinced this is accurate but it's hardly important
        a = A[-1]
        a += 1
        A.append(a)
        S.append(s)
        
        ax1.clear()#to stop overlapping plots and causing unnecessary render issues
        
        ax1.imshow(im)
        
        ax3.clear()
        ax3.set_xlabel(f'iteration {i}')
        ax3.set_ylabel(f'max accuracy {max(S):.2f}%')
        ax3.set_title(f'{s:.2f}% similair')
        ax3.plot(S)

ax1.set_title("new")
ax2.set_title("original")
fig.tight_layout()
ani = animation.FuncAnimation(fig,animate_rand,interval = 1,fargs = (im,height,
                                                                     width,size,init,
                                                                     35))
plt.show()

#save the image
fname = "output/"+input("What would you like to call it?")+".png"
IM.imsave(fname,im)
