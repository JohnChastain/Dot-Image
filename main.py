from PIL import Image
import turtle as t
import random
import numpy as np
import copy

class DotImage:
  def __init__(self, image_str, dot_width):
    img = Image.open(image_str, 'r')
    img = img.convert('RGB')
    self.image = img.load()
    self.image_height = img.height
    self.image_width = img.width
    self.aspect_ratio = self.image_height/self.image_width
    self.num_x_dots = dot_width
    self.num_y_dots = int(self.num_x_dots * self.aspect_ratio)
    self.total_dots = self.num_x_dots * self.num_y_dots
    self.canvas_width = 300
    self.canvas_height = self.canvas_width * self.aspect_ratio
    self.dot_height = self.image_height/self.num_y_dots
    self.dot_width = self.image_width/self.num_x_dots
    self.dot_diameter = np.sqrt((self.canvas_height/self.num_y_dots)**2 + (self.canvas_width/self.num_x_dots)**2) *1.1
    self.dot_image = []
    for i in range(self.num_x_dots):
      for j in range(self.num_y_dots):
        avg_r = 0
        avg_g = 0
        avg_b = 0
        num_pix = 0
        #Cycles through each pixel in a chunk
        for k in range(int(self.dot_width)):
          for l in range(int(self.dot_height)):
            avg_r += self.image[i*(self.dot_width) + k, j*(self.dot_height) + l][0]
            avg_g += self.image[i*(self.dot_width) + k, j*(self.dot_height) + l][1]
            avg_b += self.image[i*(self.dot_width) + k, j*(self.dot_height) + l][2]
            num_pix += 1
        avg_r = int(avg_r/num_pix)
        avg_g = int(avg_g/num_pix)
        avg_b = int(avg_b/num_pix)
        self.dot_image.append([(i+1) * (self.canvas_width/self.num_x_dots) -140, (-j+1) * (self.canvas_height/self.num_y_dots)+120, avg_r, avg_g, avg_b])
    self.modified_image = self.dot_image
    
  def display(self, modified=True):
    if modified == True:
      dot_image_copy = copy.deepcopy(self.modified_image)
    else: 
      dot_image_copy = copy.deepcopy(self.dot_image)
    num_dots = 0
    update_interval = int(self.total_dots/100)
    if update_interval < 25: 
      update_interval = 25
    t.clear()
    while True:
      t.penup()
      if len(dot_image_copy) == 0:
        break
      index = random.randint(0, len(dot_image_copy)-1)
      point = dot_image_copy[index]
      t.goto(point[0], point[1])
      t.pendown()
      t.dot(self.dot_diameter, (int(point[2]),int(point[3]),int(point[4])))
      dot_image_copy.pop(index)
      num_dots += 1
      if num_dots % update_interval == 0:
        print(f'Percentage: {int((num_dots/self.total_dots) * 100)}%', end = '\r')
        t.update()
    t.goto(1000,1000)
    t.update()
    print()
    
  def invert(self, modified = False):
    match modified:
      case False:
        for i, image in enumerate(self.dot_image):
          self.modified_image[i][2] = 255- image[2]
          self.modified_image[i][3] = 255- image[3]
          self.modified_image[i][4] = 255- image[4]
      case True:
        for i, image in enumerate(self.modified_image):
          self.modified_image[i][2] = 255- image[2]
          self.modified_image[i][3] = 255- image[3]
          self.modified_image[i][4] = 255- image[4]
          
  def color_filter(self, color = None, strength = 50, modified = False):
    if modified == False:
      image = copy.deepcopy(self.dot_image)
    else:
      image = copy.deepcopy(self.modified_image)
    match color:
      case 'Red'| 'red'| 'r'| 'R':
        var = 2
      case 'Green'| 'green'| 'g'| 'G':
        var = 3
      case 'Blue'| 'blue'| 'b'| 'B':
        var = 4
    for pixel in image:
          if pixel[var] < 255-strength and pixel[var] + strength> 0:
            pixel[var]  +=  strength
          elif pixel[var] + strength <0:
            pixel[var] = 0
          else: 
            pixel[var]= 255
    self.modified_image = image
    
  def many_color_filter(self, color = 'Red', strength = 100, modified = False):
    match color:
      case 'Red' | 'red' | 'r' | 'R':
        self.color_filter(color = 'Red', strength = strength, modified = modified)
      case 'Blue' | 'blue' | 'b' | 'B':
        self.color_filter(color = 'Blue', strength = strength, modified = modified)
      case 'Green' | 'green' | 'g' | 'G':
        self.color_filter(color = 'Green', strength = strength, modified = modified)
      case 'Yellow' | 'yellow' | 'y' | 'Y':
        self.color_filter(color = 'Red', strength = strength, modified = modified)
        self.color_filter(color = 'Green', strength = strength, modified = modified)
      case 'Magenta' | 'magenta' | 'Purple' | 'purple' | 'magenta' | 'm' | 'M' | 'p' | 'P':
        self.color_filter(color = 'Red', strength = strength, modified = modified)
        self.color_filter(color = 'Blue', strength = strength, modified = modified)
      case 'Cyan' | 'cyan' | 'c' | 'C':
        self.color_filter(color = 'Green', strength = strength, modified = modified)
        self.color_filter(color = 'Blue', strength = strength, modified = modified)

  def contrast(self, strength = 1.3, modified = False):
    if modified == False:
      image = copy.deepcopy(self.dot_image)
    else:
      image = copy.deepcopy(self.modified_image)
    for pixel in image:
      for j in range(2,5):
        if pixel[j] >= 255/2:
          pixel[j] = int(pixel[j] + .2*(255 - pixel[j]))
        else: 
          pixel[j] = int(pixel[j] + .2*(0 - pixel[j]))
    self.modified_image = image

    
  def noise(self, strength = 80, modified = False):
    if modified == False:
      image = copy.deepcopy(self.dot_image)
    else:
      image = copy.deepcopy(self.modified_image)
    for pixel in image:
      for j in range(2,5):
        pixel[j] += random.randint(int(-strength), int(strength))
        if pixel[j] <0:
          pixel[j] = 0
        if pixel[j] >255:
          pixel[j] = 255
    self.modified_image = image
  def group(self, strength = 128, modified = False):
    if modified == False:
      image = copy.deepcopy(self.dot_image)
    else:
      image = copy.deepcopy(self.modified_image)
    for i in range(len(image)):
      for j in range(2,5):
        image[i][j] = strength* (image[i][j]//strength) 
    self.modified_image = image


t.tracer(0,0)
t.colormode(255)
t.speed(0)

image_dictionary = {1: ['Forest', 'Images/forest.png'], 2 : ['Milky Way Galaxy', 'Images/milky_way.jpg'], 3 : ['Grassy Field', 'Images/field.png'], 4 : ['Cat', 'Images/cat.jpg'], 5: ['Dog', 'Images/dog.jpg'], 6 : ['House', 'Images/house.jpg'], 7 : ['North Central', 'Images/north_central.webp'], 8 : ['Eye Test', 'Images/eyetest.jpg'], 9 : ['Test', 'Images/test.png'], 10 : ['Mona Lisa', 'Images/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg.webp']}

print('This program takes in an image and draws that image with a selected number of dots')
while True:
  print('Choose an image and input its corresponding number')
  for item in image_dictionary:
    print(f'{item}: {image_dictionary[item][0]}')
  print('Or input 0 if you would like to import your own image')
  print()
  image_choice = int(input('Input your number: '))
  if image_choice == 0:
    image_path = input('If you have already imported your image into replit and re-ran the \ncode, type the file name. If you have not done either of\nthose things, import your image and rerun the code. : ')
  else:
    image_path = image_dictionary[image_choice][1]
  dot_width = int(input('How many dots wide would you like the image to be (It is recommended\nnot to exceed 150): '))
  image = DotImage(image_path, dot_width)
  image.display()
  while True: 
    print()
    q1 = int(input('Enter 1 if you would like to apply a filter or 0 if you would like to try a new image: '))
    if q1 == 0:
      break
    color = input('Enter one of the following filters: Invert, Contrast, Noise, Group, Red, Blue, Green, Yellow, Magenta, Cyan: ')
    modified = int(input('Enter 1 if you would like to apply this to the current image, 0 for the\noriginal (Choose current if you want to apply multiple filters): '))
    if modified == 1:
      modified = True
    else:
      modified = False
    if color == 'Invert' or color == 'invert' or color == 'i':
      image.invert(modified = modified)
    elif color == 'Contrast' or color == 'contrast' or color == 'c':
      image.contrast(modified = modified)
    elif color == 'noise' or color == 'Noise' or color == 'n':
      image.noise(modified = modified)
    elif color == 'group' or color == 'Group':
      image.group(modified = modified)
    else:
      image.many_color_filter(color = color, modified = modified)
    image.display()
