strengthList = []
counter = 0

def pulseDuo():
    pass

def pulse():
    pass

def on_frame(self, controller):
    frame = controller.frame()

    for hand in frame.hands:
        self.strengthList.append(hand.grab_strength)
    
        if len(self.strengthList) > 200:
            for i in range(len(self.strengthList)-1):
                if self.strengthList[i] == 1 and self.strengthList[i+1] < 1:
                    self.counter += 1
                else:
                    continue
            if self.counter == 1:
                pulse()
            elif self.counter == 2:
                pulseDuo()
            else:
                continue  
            self.strengthList = []              

