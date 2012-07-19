#! /usr/bin/python

from openni import *
import liblo, sys

context = Context()
context.init()

maior = [0, 0, 0]
menor = [0, 0, 0]
batido = False

try:
    target = liblo.Address("192.168.10.60", 1234)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

depth_generator = DepthGenerator()
depth_generator.create(context)
depth_generator.set_resolution_preset(RES_VGA)
depth_generator.fps = 30

gesture_generator = GestureGenerator()
gesture_generator.create(context)
gesture_generator.add_gesture('Wave')
#gesture_generator.add_gesture('Click')

hands_generator = HandsGenerator()
hands_generator.create(context)

# Declare the callbacks
# gesture
def gesture_detected(src, gesture, id, end_point):
    print "Detected gesture:", gesture
    hands_generator.start_tracking(end_point)
# gesture_detected

def gesture_progress(src, gesture, point, progress): pass
# gesture_progress

def create(src, id, pos, time):
    print 'Create ', id, pos
# create

def update(src, id, pos, time):
    msg = liblo.Message("/foo%d" % (id - 1 % 4))
    msg.add(-pos[0])
    msg.add(pos[1])
    msg.add(pos[2])
    global batido


    if pos[2] > 1000:
        msg.add(1)
        batido = True
    else:
        msg.add(0)

    for i in range(3):
        if pos[i] < menor[i]: menor[i] = pos[i]
        if pos[i] > maior[i]: maior[i] = pos[i]

    liblo.send(target, msg)
    
    print 'Update ', id, pos

# update

def destroy(src, id, time):
    print 'Destroy ', id
    print maior
    print menor
# destroy

# Register the callbacks
gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

# Start generating
context.start_generating_all()

print 'Make a Wave to start tracking...'

while True:
    context.wait_any_update_all()
# while
