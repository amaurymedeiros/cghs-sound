from SimpleCV import *
import liblo, sys


class ToneMatrix(object):
    def __init__(self, width, height):
        self.matrix = [[0 for j in range(width)] for i in range(height)]

    def __str__(self):
        return "\n".join(map(str, self.matrix))

    def enable(self, x, y):
        self.matrix[y][x] = 1

    def disable(self, x, y):
        self.matrix[y][x] = 0

    def check(self, x, y):
        return self.matrix[y][x]

    def generate_message(self):
        message = []
        for row in self.matrix:
            number = int("".join([str(num) for num in row]), 2)
            message.append(number)

        return message

class Segmenter(object):
    THRESHOLD = 220
    THRESHOLD_AVG = 230

    def __init__(self, blocks_x, blocks_y):
        self.blocks_x = blocks_x
        self.blocks_y = blocks_y

    def segment(self, img):
        dx = img.width/self.blocks_x
        dy = img.height/self.blocks_y

        tone_matrix = ToneMatrix(self.blocks_x, self.blocks_y)

        for x in range(self.blocks_x):
            for y in range(self.blocks_y):
                block = tone_matrix.matrix[x][y]
                preenchido = self.check_presence_avg(img, x*dx, y*dy, dx, dy)
                if preenchido:
                    tone_matrix.enable(x, y)
        return tone_matrix 
                

    def check_presence(self, img, base_x, base_y, width, height):
        for i in range(width):
            for j in range(height): 
                if img.getPixel(base_x + i,base_y + j)[0] < self.THRESHOLD:
                    return True

        return False    

    def check_presence_avg(self, img, base_x, base_y, width, height):
        tot = 0
        for i in range(width):
            for j in range(height): 
                tot += img.getPixel(base_x+i,base_y+j)[0]
        return tot/(width*height) <= self.THRESHOLD_AVG
        

class Drawer(object):
    
    def __init__(self, blocks_x, blocks_y):
        self.blocks_x = blocks_x
        self.blocks_y = blocks_y
  
    def draw(self, matrix, img):
        dx = img.width/self.blocks_x
        dy = img.height/self.blocks_y
        self.img = img

        for x in range(self.blocks_x):
            for y in range(self.blocks_y):
                if matrix.matrix[y][x]:
                    img.drawRectangle(x*dx, y*dy, dx, dy, Color.YELLOW, 5)

        return img
                    #self.draw_square(img, 


        #img.show() 

NUM_BLOCKS_X = 16
NUM_BLOCKS_Y = 16

segmenter = Segmenter(NUM_BLOCKS_X, NUM_BLOCKS_Y)
drawer = Drawer(NUM_BLOCKS_X, NUM_BLOCKS_Y)
k = Kinect()

try:
    target = liblo.Address("192.168.10.60", 1234)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

while True:
    depth = k.getDepth().flipHorizontal()
    img = k.getImage().flipHorizontal()

    matrix = segmenter.segment(depth)
#    print matrix
#    print ":::::::::::::"
    bits = matrix.generate_message()
    drawer.draw(matrix, img).show()
    
    msg = liblo.Message("/matrix")
    for number in bits:
        msg.add(number)

    liblo.send(target, msg)
