import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, math
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    bone_names = ["Metacarpal", "Proximal", "Intermediate", "Distal"]
    state_names = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]
    gestures = ["SWIPE_UP", "SWIPE_DOWN", "SWIPE_LEFT", "SWIPE_RIGHT", "COUNT_FINGERS", "DIAL", "FLASH"]

    counter = 0
    maxFrameCount = 150
    frameList = []
    actualTemp = 10
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

    def reset():
        pass

    def getMajorAxis(self,x,y,z):
        if x > y and x > z:
            return 'x'
        elif y > x and y > z:
            return 'y'
        elif z > x and z > y:
            return 'z' 
        
    # Frame Data
    def on_frame(self, controller):
        frame = controller.frame()

        # len(frame.hands), len(frame.fingers))
        frameID = str(frame.id)
        timestamp = str(frame.timestamp)
        lenHands = str(len(frame.hands))
        lenFingers = str(len(frame.fingers))
        fps = frame.current_frames_per_second


        swipeDirection = ""
        for hand in frame.hands:
            self.frameList.append(hand)
            
            numberHands = len(frame.hands)

            # PULSE/PULSE DUO
            self.strengthList.append(hand.grab_strength)
            
            if len(self.strengthList) > 200:
                for i in range(len(self.strengthList)-1):
                    if self.strengthList[i] == 1 and self.strengthList[i+1] < 1:
                        self.counter += 1
                    else:
                        continue
                if self.counter == 1:
                    #print self.counter
                    print "pulse"
                elif self.counter == 2:
                    #print self.counter
                    print "pulse duo"
                else:
                    #print self.counter
                    print "too many"  
                self.strengthList = []   
                self.counter = 0
           
            # Hand Data
            handType = "Left Hand" if hand.is_left else "Right Hand"

            handID = str(hand.id)
            palmPosition = str(hand.palm_position)
            normal = hand.palm_normal
            direction = hand.direction
            handSpeed = hand.palm_velocity
            
            handPitch = (direction.pitch * Leap.RAD_TO_DEG)
            handRoll = (normal.roll * Leap.RAD_TO_DEG)
            handYaw = (direction.yaw * Leap.RAD_TO_DEG)

            # ADJUST VOLUME/TEMPERATURE
            startAngle = self.frameList[0].direction.yaw
            startAngle = startAngle * Leap.RAD_TO_DEG
            endAngle = self.frameList[-1].direction.yaw
            endAngle = endAngle * Leap.RAD_TO_DEG
            
            angles = (startAngle,endAngle)

            difference_angles = endAngle-startAngle

            # Swipe Gesture - Up/Down (z), Left/Right(x)
            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x
            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z
            difference = (end_x - start_x, end_z - start_z)

            absX = abs(difference[0])
            absZ = abs(difference[1])
            
            majorAxis = self.getMajorAxis(absX, 0, absZ)           

            # AMBIENT LIGHTING COLOUR
            if majorAxis == 'x' and absX > 50:
                if difference[0] > 0:
                    swipeDirection = "Right"
                else:
                    swipeDirection = "Left"
            
            # AMBIENT LIGHTING BRIGHTNESS
            elif majorAxis == 'z' and absZ > 50:
                if difference[1] > 0:
                    swipeDirection = "Down"
                else:
                    swipeDirection = "Up"

            # INTENSITY LEVEL OF MASSAGE CHAIR
            extendedFingers = frame.fingers.extended()
            noFingers = len(extendedFingers)
            if noFingers == 1:
                intensityLevel = 1
            elif noFingers == 2:
                intensityLevel =2
            elif noFingers == 3:
                intensityLevel = 3
            elif noFingers == 4:
                intensityLevel = 4
            elif noFingers == 5:
                intensityLevel = 5

            # DRINK
            """
            pinky = hand.fingers.finger_type(4)[0]
            thumb = hand.fingers.finger_type(0)[0]
            index = hand.fingers.finger_type(1)[0]
            middle = hand.fingers.finger_type(2)[0]
            ring = hand.fingers.finger_type(3)[0]

            if index not in extendedFingers and middle not in extendedFingers and ring not in extendedFingers
                if startAngle > 40 and endAngle < 10:
                    champagne_cooler = "OPEN"
            """
            
            # PULSE/PULSE DUO FORMAT
            startFingers = len(self.frameList[0].fingers.extended())
            endFingers = len(self.frameList[-1].fingers.extended())

            if startFingers == 0 and endFingers == 5:
                gesture = "Flash"
            else:
                gesture = ""

            # Grab Strength
            strength = hand.grab_strength
            #if strength == 1:
                #print "grab"
            startStrength = self.frameList[0].grab_strength
            endStrength = self.frameList[-1].grab_strength
 
            # PRINT DETAILS
            if len(self.frameList) > self.maxFrameCount:
                # reset number of frames
                self.frameList = []

            """
                # AIR CONDITIONING
                if difference_angles > 0:
                    temperature = "up"
                elif difference_angles < 0:
                    temperature = "down"
                else:
                    temperature = "same"

                if temperature == "up" and self.actualTemp < 32:
                    if difference_angles < 20:
                        self.actualTemp += 1
                    elif difference_angles >= 20 and difference_angles < 40:
                        self.actualTemp += 2
                    elif difference_angles >= 40 and difference_angles < 80:
                        self.actualTemp += 3
                    elif difference_angles >= 80:
                        self.actualTemp += 5
                elif temperature == "down" and self.actualTemp > 2:
                    if difference_angles > -20:
                        self.actualTemp -= 1
                    elif difference_angles <= -20 and difference_angles > -40:
                        self.actualTemp -= 2
                    elif difference_angles <= -40 and difference_angles > -80:
                        self.actualTemp -= 3
                    elif difference_angles <= -80:
                        self.actualTemp -= 5
                else:
                    continue

                # PULSE/ PULSE DUO
                if gesture == "Flash":
                    print "Flash"
                else:
                    print noFingers
                
                # AMBIENT LIGHTING
                if swipeDirection <> "":
                    print swipeDirection
                else:
                    # HOT STONE MASSAGE
                    print "hold"
            """

            # Arm Data
            arm = hand.arm
            armDirection = str(arm.direction)
            wristPosition = str(arm.wrist_position)
            elbowPosition = str(arm.elbow_position)

            # Finger Data
            for finger in hand.fingers:
                
                fingerType = self.finger_names[finger.type]
                fingerID = str(finger.id)
                fingerLen = str(finger.length)
                fingerWidth = str(finger.width)

                # Bone Data
                for b in range(0,4):
                    bone = finger.bone(b)
                    boneType = self.bone_names[bone.type]
                    boneStartPoint = str(bone.prev_joint)
                    boneEndPoint = str(bone.next_joint)
                    boneDirection = str(bone.direction)
           
        # Tool Data
        for tool in frame.tools:
            toolID = str(tool.id)
            tipPosition = str(tool.tip_position)
            toolDirection = str(tool.direction)

        # Gesture Data
        colIndex = 0
        brightIndex = 0
        for gesture in frame.gestures():
            # Circle Data
            # USED FOR TURNING ON/OFF MASSAGE CHAIR??
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                    #print "Clockwise Circle"
                else:
                    clockwiseness = "counter-clockwise"
                    #print "Counter-Clockwise Circle"

                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous = CircleGesture(controller.frame(1).gesture(circle.id)) 
                    swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                
                circleID = str(circle.id)
                circleProgress = str(circle.progress)
                circleRadius = str(circle.radius)
                circleSweptAngle = str(swept_angle* Leap.RAD_TO_DEG)

                
                if len(extendedFingers) ==5:
                    if circle.progress < 1:
                        print "hello"
                

            # Swipe Data
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)

                swipeID = str(swipe.id)
                swipeState = self.state_names[gesture.state]
                swipePosition = str(swipe.position)
                swipeDirection = str(swipe.direction)
                swipeSpeed = str(swipe.speed)

                # Swipe Up, Down, Left, Right
                swipeDir = swipe.direction
                
                if (swipeDir.x > 0) and math.fabs(swipeDir.x)> math.fabs(swipeDir.y):
                    swipeProperDirection = "Right"
                elif (swipeDir.x < 0) and math.fabs(swipeDir.x)> math.fabs(swipeDir.y):
                     swipeProperDirection = "Left"
                elif (swipeDir.y > 0) and math.fabs(swipeDir.x)< math.fabs(swipeDir.y):
                     swipeProperDirection = "Up"
                elif (swipeDir.y < 0) and math.fabs(swipeDir.x)< math.fabs(swipeDir.y):
                     swipeProperDirection = "Down"

                colours = ["Ultraviolet", "Spark Blue", "Moonlight", "Racing Red", "Electric Blue", "Limelight", "Amber Glow", "Sunset", "Ice White", "Daylight"]
                brightness = ["Low", "Medium", "Bright", "Brightest"]

                if swipeProperDirection == "Right":
                    colIndex = (colIndex+1) % len(colours) 
                    colour = colours[colIndex]
                elif swipeProperDirection == "Left":
                    colIndex = (colIndex-1) % len(colours)
                    colour = colours[colIndex]

                if swipeProperDirection == "Up":
                    brightIndex += 1
                    if brightIndex >= 4:
                        continue
                    else:
                        howBright = brightness[brightIndex]
                elif swipeProperDirection == "Down":
                    brightIndex -= 1
                    if brightIndex < 0:
                        continue
                    else:
                        howBright = brightness[brightIndex]

            # Screen Tap Gesture
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                #print "screen tap"
                """
                if handType == "Right Hand":
                    print "right tap"
                elif handType == "Left Hand":
                    print "left Tap"
                elif handType == "Right Hand" and handType == "Left Hand":
                    print "Double Tap"
                """
                screenTap = ScreenTapGesture(gesture)
                screenTapID = str(gesture.id)
                screenTapState = self.state_names[gesture.state]
                screenTapPosition = str(screenTap.position)
                screenTapDirection = str(screenTap.direction)

            # Key Tap Gesture
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keyTap = KeyTapGesture(gesture)
                
                keyTapID = str(gesture.id)
                keyTapState = self.state_names[gesture.state]
                keyTapPosition = str(keyTap.position)
                keyTapDirection = str(keyTap.direction)

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