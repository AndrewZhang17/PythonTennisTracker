import cv2
import numpy as np

BALLSIZE = 0.067

class Tracker(object):
    def __init__(self, src):
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        self.video = cv2.VideoCapture(src)
        self.fps = self.video.get(cv2.CAP_PROP_FPS) 
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.positions = {}
    
    def __del__(self):
        self.video.release()
        
    def analyze_frame(self, num, relX, relY):
        print(num, relX, relY)
        self.video.set(cv2.CAP_PROP_POS_FRAMES, num-1)
        success, frame = self.video.read()
        
        x = int(relX*self.width)
        y = int(relY*self.height)
        print(self.width, self.height, frame.shape)


        fgMask = self.backSub.apply(frame)
        th, im_th = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)

        im_floodfill = im_th.copy()

        h, w = im_th.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)

        cv2.floodFill(im_floodfill, mask, (0, 0), 255)
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        im_out = im_th | im_floodfill_inv

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        im_out = cv2.erode(im_out,kernel,iterations = 3)
        cv2.imwrite("test.jpg", fgMask)

        contours, hierarchy = cv2.findContours(im_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True)[:100]

        frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        frame = cv2.circle(frame, (x,y), 1, (255, 0, 0), -1)


        # cv2.imshow("FG Mask", im_out)
            
        # keyboard = cv2.waitKey(1)
        # while keyboard not in [ord('n'), ord('q'), 27] and clicked == False:
        # keyboard = cv2.waitKey(1)
        # if clicked == True:
        suc = False
        for c in contours:
            found = cv2.pointPolygonTest(c, (x, y), False)
            if found > 0:
                suc = True
                print("success!")
                ballMask = np.zeros(im_out.shape[:2], dtype = np.uint8)
                ballMask = cv2.drawContours(ballMask, [c], -1, 255, -1)

                dst = cv2.distanceTransform(ballMask, cv2.DIST_L2, 5)
                pos = np.unravel_index(np.argmax(dst), dst.shape)[::-1]
                rad = dst.max()

                # ball = cv2.fitEllipse(c)
                # fnum = cap.get(cv2.CAP_PROP_POS_FRAMES)
                self.positions[num] = {
                    "pos": pos,
                    "rad": rad
                }
                print(self.positions)
                # cv2.ellipse(frame, ball, (255, 0, 0), 2)
                # cv2.circle(frame, (int(ball[0][0]), int(ball[0][1])), 3, (0, 0, 255), 2)
                cv2.circle(frame, pos, rad, (0, 0, 255))
                cv2.imshow("Frame", frame)
                cv2.waitKey(0)
        if suc == False:
            print("fail, lmao")
        # clicked = False            

        # if keyboard == ord('q') or keyboard == 27:
        # break

        # else:
        # break
    
    def calcSpeed(self):
        avgRad = 0
        for i in self.positions.values():
            avgRad += i["rad"]
        avgRad /= len(self.positions)
        print(avgRad)

        metersPerPx = BALLSIZE/(avgRad*2)

        speeds = []

        frames = list(self.positions.keys())

        for i in range(len(frames)-1):
            d = np.sqrt((self.positions[frames[i+1]]["pos"][0] - self.positions[frames[i]]["pos"][0])**2 + (self.positions[frames[i+1]]["pos"][1] - self.positions[frames[i]]["pos"][1])**2)
            d *= metersPerPx
            t = (frames[i+1] - frames[i])/self.fps
            print(d/t*2.237)
            speeds.append(d/t)
        
        return np.average(speeds)*2.237







# mouseX = 0
# mouseY = 0
# clicked = False

# def mousecallback(event,x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN: 
#         global mouseX, mouseY, clicked
#         clicked = True
#         mouseX = x
#         mouseY = y

# def calcSpeed(positions, fps):
#     avgRad = 0
#     for i in positions.values():
#         avgRad += i["rad"]
#     avgRad /= len(positions)
#     print(avgRad)

#     metersPerPx = BALLSIZE/(avgRad*2)

#     speeds = []

#     frames = list(positions.keys())

#     for i in range(len(frames)-1):
#         d = np.sqrt((positions[frames[i+1]]["pos"][0] - positions[frames[i]]["pos"][0])**2 + (positions[frames[i+1]]["pos"][1] - positions[frames[i]]["pos"][1])**2)
#         print("d in px:", d)
#         d *= metersPerPx
#         print("d in m:", d)
#         t = (frames[i+1] - frames[i])/fps
#         print("fps:", fps)
#         print("t:", t)
#         print(d/t*2.237)
#         speeds.append(d/t)

# if __name__=="__main__":
#     cap = cv2.VideoCapture("tennis.mp4")
#     fps = cap.get(cv2.CAP_PROP_FPS) 

#     positions = {}
#     backSub = cv2.createBackgroundSubtractorMOG2()

#     cv2.namedWindow("Frame")
#     cv2.setMouseCallback("Frame", mousecallback)

#     if not cap.isOpened:
#         print("Unable to open")
#         exit(0)

#     while cap.isOpened:
#         ret, frame = cap.read()
               

#         if ret == True:
#             fgMask = backSub.apply(frame)
#             th, im_th = cv2.threshold(fgMask, 250, 255, cv2.THRESH_BINARY)

#             im_floodfill = im_th.copy()

#             h, w = im_th.shape[:2]
#             mask = np.zeros((h+2, w+2), np.uint8)

#             cv2.floodFill(im_floodfill, mask, (0, 0), 255)
#             im_floodfill_inv = cv2.bitwise_not(im_floodfill)

#             im_out = im_th | im_floodfill_inv

#             kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#             im_out = cv2.erode(im_out,kernel,iterations = 3)

#             contours, hierarchy = cv2.findContours(im_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True)[:100]

#             frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

#             cv2.imshow("Frame", frame)
#             cv2.imshow("FG Mask", im_out)
            
#             keyboard = cv2.waitKey(1)
#             while keyboard not in [ord('n'), ord('q'), 27] and clicked == False:
#                 keyboard = cv2.waitKey(1)
#             if clicked == True:
#                 suc = False
#                 for c in contours:
#                     r = cv2.pointPolygonTest(c, (mouseX, mouseY), False)
#                     if r > 0:
#                         suc = True
#                         print("success!")
#                         ballMask = np.zeros(im_out.shape[:2], dtype = np.uint8)
#                         ballMask = cv2.drawContours(ballMask, [c], -1, 255, -1)

#                         dst = cv2.distanceTransform(ballMask, cv2.DIST_L2, 5)
#                         pos = np.unravel_index(np.argmax(dst), dst.shape)[::-1]
#                         rad = dst.max()

#                         # ball = cv2.fitEllipse(c)
#                         fnum = cap.get(cv2.CAP_PROP_POS_FRAMES)
#                         positions[fnum] = {
#                             "pos": pos,
#                             "rad": rad
#                         }
#                         # cv2.ellipse(frame, ball, (255, 0, 0), 2)
#                         # cv2.circle(frame, (int(ball[0][0]), int(ball[0][1])), 3, (0, 0, 255), 2)
#                         cv2.circle(frame, pos, rad, (0, 0, 255))
#                         cv2.imshow("Frame", frame)
#                         cv2.waitKey(0)
#                 if suc == False:
#                     print("fail, lmao")
#                 clicked = False            

#             if keyboard == ord('q') or keyboard == 27:
#                 break

#         else:
#             break
#     print(positions)
#     calcSpeed(positions, fps)
