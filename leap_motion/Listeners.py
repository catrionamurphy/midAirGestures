import Leap
from Leap import CircleGesture

class Dial(Leap.Listener):
    def on_init(self, controller):
        print "initialised"
    def on_connect(self, controller):
        print "Motion Sensor Connected"
    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"
    def on_exit(self, controller):
        print "Exit"

    def on_frame(self, controller):
        frame = controller.frame()

class Drink(Leap.Listener):
    maxFrameCount = 150
    frameList = []
    def on_frame(self, controller):
        frame = controller.frame()
        #print "drinking"
        for hand in frame.hands:
            self.frameList.append(hand)
            pinky = hand.fingers.finger_type(4)[0]
            thumb = hand.fingers.finger_type(0)[0]
            index = hand.fingers.finger_type(1)[0]
            middle = hand.fingers.finger_type(2)[0]
            ring = hand.fingers.finger_type(3)[0]

            extendedFingers = frame.fingers.extended()

            startAngle = self.frameList[0].direction.yaw
            startAngle = startAngle * Leap.RAD_TO_DEG
            endAngle = self.frameList[-1].direction.yaw
            endAngle = endAngle * Leap.RAD_TO_DEG
            
            angles = (startAngle,endAngle)

            difference_angles = endAngle-startAngle

            if index not in extendedFingers and middle not in extendedFingers and ring not in extendedFingers:
                if startAngle > 40 and endAngle < 10:
                    champagne_cooler = "OPEN"

            if len(self.frameList) > 150:
                self.frameList = []

class Circle_Listener(Leap.Listener):
    def on_frame(self, controller):
        frame = controller.frame()

class Swipe_Listener(Leap.Listener):
    def on_frame(self, controller):
        frame = controller.frame()