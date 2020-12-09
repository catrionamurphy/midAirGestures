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

    minFrameCount = 50
    maxFrameCount = 200
    frameList = []


    def on_init(self, controller):
        print "Initialised"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exit"

    # Frame Data
    def on_frame(self, controller):
        frame = controller.frame()

        # len(frame.hands), len(frame.fingers))
        frameID = str(frame.id)
        timestamp = str(frame.timestamp)
        lenHands = str(len(frame.hands))
        lenFingers = str(len(frame.fingers))
        
        fps = frame.current_frames_per_second

        for hand in frame.hands:
            self.frameList.append(hand)
            
            # Hand Data
            handType = "Left Hand" if hand.is_left else "Right Hand"

            handID = str(hand.id)
            palmPosition = str(hand.palm_position)
            normal = hand.palm_normal
            direction = hand.direction
            handSpeed = hand.palm_velocity
            
            handPitch = str(direction.pitch * Leap.RAD_TO_DEG)
            handRoll = str(normal.roll * Leap.RAD_TO_DEG)
            handYaw = str(direction.yaw * Leap.RAD_TO_DEG)

            #Flash?

            strength = hand.grab_strength
            if strength == 1:
                #print "pulse"
                pass

            # New Swipe Stuff
            start_x = self.frameList[0].palm_position.x
            end_x = self.frameList[-1].palm_position.x

            start_y = self.frameList[0].palm_position.y
            end_y = self.frameList[-1].palm_position.y

            start_z = self.frameList[0].palm_position.z
            end_z = self.frameList[-1].palm_position.z

            if len(self.frameList) > self.maxFrameCount:
                #print "Too Big"
                self.frameList = []
                

            # Potential swipe up down?
            # takes first frame and compares the hand position
            prev_frame = controller.frame()
            hand = prev_frame.hands[0]
            current_frame = controller.frame(1)
            current_hand = current_frame.hands[0]
            
            left_pos = -220
            right_pos = 250

            swipe_right = False
            start_left = False
            end_right = False

            """
            if hand.palm_position.x = left_pos:
                start_left = True
                print "start: " + str(start_left)
            if current_hand.palm_position.x >= right_pos:
                end_right = True
                print "end: " + str(end_right)
            
            if start_left == True and end_right == True:
                swipe_right = True
                print "You Swiped Right"
            """

            up_pos = 0
            down_pos = 0

            forward_pos = 0
            backwards_pos = 0

            """
            print "%d, %d"%(hand.palm_position.y,current_hand.palm_position.y)

            if(hand.palm_position.y-current_hand.palm_position.y > 1):
                print "Backwards"
            elif(hand.palm_position.y-current_hand.palm_position.y <-1):
                print "Forwards"
            """
            """
            
            print "%d, %d"%(hand.palm_position.x,current_hand.palm_position.x)

            if(hand.palm_position.x-current_hand.palm_position.x > 1):
                print "Right"
            elif(hand.palm_position.x-current_hand.palm_position.x <-1):
                print "Left"
            """

            """
            print "%d, %d"%(hand.palm_position.z,current_hand.palm_position.z)

            if(hand.palm_position.z-current_hand.palm_position.z > 1):
                print "Down"
            elif(hand.palm_position.z-current_hand.palm_position.z <-1):
                print "Up"
            
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

                extended = frame.fingers.extended()
                noFingers = len(extended)

                #print noFingers



                #print fingerType

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
                    #print "You have swiped right"
                elif (swipeDir.x < 0) and math.fabs(swipeDir.x)> math.fabs(swipeDir.y):
                     swipeProperDirection = "Left"
                     #print "You have swiped left"
                elif (swipeDir.y > 0) and math.fabs(swipeDir.x)< math.fabs(swipeDir.y):
                     swipeProperDirection = "Up"
                     #print "You have swiped up"
                elif (swipeDir.y < 0) and math.fabs(swipeDir.x)< math.fabs(swipeDir.y):
                     swipeProperDirection = "Down"
                     #print "You have swiped down"

                colours = ["Ultraviolet", "Spark Blue", "Moonlight", "Racing Red", "Electric Blue", "Limelight", "Amber Glow", "Sunset", "Ice White", "Daylight"]
                brightness = ["Low", "Medium", "Bright", "Brightest"]

                if swipeProperDirection == "Right":
                    colIndex = (colIndex+1) % len(colours) 
                    colour = colours[colIndex]
                    #print "The Colour of the ambient lighting is " + colour
                elif swipeProperDirection == "Left":
                    colIndex = (colIndex-1) % len(colours)
                    colour = colours[colIndex]
                    #print "The Colour of the ambient lighting is " + colour

                if swipeProperDirection == "Up":
                    brightIndex += 1
                    if brightIndex >= 4:
                        continue
                        #print "You are at the brightest level"
                    else:
                        howBright = brightness[brightIndex]
                       # print "Brightness level is: " + howBright
                elif swipeProperDirection == "Down":
                    brightIndex -= 1
                    if brightIndex < 0:
                        continue
                        #print "You are at the lowest brightness level"
                    else:
                        howBright = brightness[brightIndex]
                        #print "Brightness level is: " + howBright

            # Screen Tap Gesture
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screenTap = ScreenTapGesture(gesture)
                #print "You have performed a screen tap"
                screenTapID = str(gesture.id)
                screenTapState = self.state_names[gesture.state]
                screenTapPosition = str(screenTap.position)
                screenTapDirection = str(screenTap.direction)

            # Key Tap Gesture
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keyTap = KeyTapGesture(gesture)

                #print "You have performed a key tap"
                keyTapID = str(gesture.id)
                keyTapState = self.state_names[gesture.state]
                keyTapPosition = str(keyTap.position)
                keyTapDirection = str(keyTap.direction)



def main():
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Set Up all the features
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
