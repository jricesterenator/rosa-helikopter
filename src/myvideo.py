import time
import numpy as np

class MyVideoPane:

    #Stretch the video pane this much when standard def to be fullscreen.
    SD_STRETCH=2.0
#    TRAINSET = "/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml"
    TRAINSET = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
    DOWNSCALE = 4

    def __init__(self, fullscreen=False):
        self.daemon = True

        global cv2
        import cv2

        self.drone = None
        self.running = False
        self.fullscreen = fullscreen

        self.classifier = cv2.CascadeClassifier(self.TRAINSET)

    def enable_drone_video(self, drone):
        self.drone = drone
        print "Drone is HD?", self.drone.isHD()

    def start(self):
        #Init a blank picture
        if not self.drone:
            print "Creating blank picture"
            width, height = (640, 480)
            img = np.zeros((height, width,3), np.uint8)
#            img[:,0:width] = (255,255,255) #set white

        self.running = True
        video_waiting = False
        while self.running:
            time.sleep(.0001)

            if self.drone:
                try:
                    img = self.drone.get_image()
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        #JRTODO - dont get this everytime
                        cv2.putText(img, "Battery:%s%%" % self.drone.get_battery() , (10,320), cv2.FONT_HERSHEY_SIMPLEX,\
                            fontScale=.8, color=(0,0,255), thickness=2, lineType=cv2.CV_AA,\
                            bottomLeftOrigin=False)


                        #JRTODO face recognition. again, dont do this every frame
                        # detect faces and draw bounding boxes
                        frame=img
                        minisize = (frame.shape[1]/self.DOWNSCALE,frame.shape[0]/self.DOWNSCALE)
                        miniframe = cv2.resize(frame, minisize)
                        faces = self.classifier.detectMultiScale(miniframe)
                        for f in faces:
                            x, y, w, h = [ v*self.DOWNSCALE for v in f ]
                            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))

                        if self.fullscreen and not self.drone.isHD():
                            img = cv2.resize(img, (0,0), fx=self.SD_STRETCH, fy=self.SD_STRETCH)
                        cv2.imshow("Drone camera", img)
                        cv2.waitKey(1)
                except NameError, e:
                    raise e
                except Exception, e:
                    raise e
#                    if not video_waiting:
#                        print "Video will display when ready"
#                    video_waiting = True
            else:
                #Line type can be: 4, 8, CV_AA
                cv2.putText(img, "Hello World!", (100,100), cv2.FONT_HERSHEY_SIMPLEX, \
                            fontScale=.8, color=(255,255,255), thickness=2, lineType=cv2.CV_AA, \
                            bottomLeftOrigin=False)
                cv2.imshow("Drone camera", img)

    def stop(self):
        self.running = False

    def destroy(self):
        self.stop()



####Get navdata
#try:
#    navdata = drone.get_navdata()
#
#    print 'Emergency landing =', navdata['drone_state']['emergency_mask']
#    print 'User emergency landing = ', navdata['drone_state']['user_el']
#    print 'Navdata type= ', navdata['drone_state']['navdata_demo_mask']
#    print 'Altitude= ', navdata[0]['altitude']
#    print 'video enable= ', navdata['drone_state']['video_mask']
#    print 'vision enable= ', navdata['drone_state']['vision_mask']
#    print 'command_mask= ', navdata['drone_state']['command_mask']
#except:
#    pass

#
#print "Asking for configuration..."
#drone.at(at_ctrl, 5)
#time.sleep(0.5)
#drone.at(at_ctrl, 4)


if __name__ == '__main__':
    vid = MyVideoPane(fullscreen=True)
    vid.start()