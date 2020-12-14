import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    state_names = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]

    maxFrameCount = 150
    frameList = []
    strengthList = []
    handNo = 0

    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"
    
    def getMajorAxis(self,x,y,z):
        if x > y and x > z:
            return 'x'
        elif y > x and y > z:
            return 'y'
        elif z > x and z > y:
            return 'z' 

    def massageChairOn():
        return True

    def massageChairOff():
        return False
    
    def pulse(self, frame):
        for hand in frame.hands:
            self.strengthList.append(hand.grab_strength)


    def pulseDuo(self, frame):
        lHand = frame.hands[1]
        rHand = frame.hands[0]

        if lHand.grab_strength == 1 and rHand.grab_strength == 1:
            self.strengthList.append(lHand.grab_strength)
        elif lHand.grab_strength == 1 and rHand.grab_strength != 1:
            continue
        elif lHand.grab_strength != 1 and rHand.grab_strength == 1:
            continue
        else:
            self.strengthList.append(lHand.grab_strength)
        
    def wave():
        pass

    def hotStone():
        pass

    def combination():
        pass

    def intensityLevel():
        pass

    def volume():
        pass

    def temperature():
        pass

    def champagneCooler():
        pass

    def ambientLighting():
        pass

    def brightnessLevel():
        pass

    def circleDetected():
        pass

    def reset():
        self.frameList = []


    def on_frame(self, controller):
        frame = controller.frame()
        
        swipeDirection = ""
        numberHands = len(frame.hands)

        for hand in frame.hands:
            # add each frame into a list when there is a hand present
            self.frameList.append(hand)

            # FINGERS
            thumb = hand.fingers.finger_type(0)[0]
            index = hand.fingers.finger_type(1)[0]
            middle = hand.fingers.finger_type(2)[0]
            ring = hand.fingers.finger_type(3)[0]
            pinky = hand.fingers.finger_type(4)[0]

            extendedFingers = frame.fingers.extended()
            noFingers = len(extendedFingers)

            # HAND YAW - for dial
            startAngle = (self.frameList[0].direction.yaw) * Leap.RAD_TO_DEG
            endAngle = (self.frameList[-1].direction.yaw) * Leap.RAD_TO_DEG

            angles = (startAngle,endAngle)
            angleDifference = endAngle-startAngle

            # PALM POSITIONS - X & Z
            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x
            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z

            palmDifference = (end_x - start_x, end_z - start_z)

            # differences as a positive number
            absX = abs(difference[0])
            absZ = abs(difference[1])

            majorAxis = self.getMajorAxis(absX, 0, absZ)

            if majorAxis == 'x':
                ambientLighting()
            elif majorAxis == 'z':
                brightnessLevel()


            # Reset FrameList
            if len(self.frameList) > self.maxFrameCount:
                self.reset()

            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        clockwiseness = "clockwise"
                        mChair = massageChairOn()
                    else:
                        clockwiseness = "counter-clockwise"
                        mChair = massageChairOff()
            
            
                
def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # Set up all the features
    frame = controller.frame()
    previous = controller.frame(1)
    hands = frame.hands
    pointables = frame.pointables
    fingers = frame.fingers
    tools = frame.tools

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()