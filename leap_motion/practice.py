import sys
sys.path.insert(0, "C:\Users\murph\Documents\Uni\Year 4\LeapDeveloperKit_4.1.0+52211_win\LeapDeveloperKit_4.1.0+52211_win\LeapSDK\lib")
import leap

controller = Leap.Controller()

controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
controller.set_policy(Leap.Controller.POLICY_IMAGES)
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)

frame = controller.frame()
hands = frame.hands
pointables = frame.pointables
fingers = frame.fingers
tool = frame.tools

pointables = hand.pointables
fingers = hand.fingers

if (pointable.is_tool):
    tool = Leap.Tool(pointable)
else:
    finger = Leap.Finger(pointable)

if (controller.is_connected):
    frame = controller.frame()
    previous = controller.frame(1)
    