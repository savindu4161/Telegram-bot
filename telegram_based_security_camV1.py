import telepot
import numpy as np
import cv2
import datetime
import random
import time
import os
import sys

def handle(msg):
  global sendPhoto
  global sendVideo
  global chat_id
  
  chat_id = msg['chat']['id']
  command = msg['text']
  
  print('Message received from ' + str(chat_id))
  
  
  if command == '/start':
    sendPhoto = True
    print(command) 
    bot.sendMessage(chat_id, "Hello, I'm your secutity assistance sir...Survailance started")
    
  elif command == '/stop':
    print(command)
    sendPhoto = False
    bot.sendMessage(chat_id, "Survailance stoped")
      
      
  elif command == '/video':
    print(command)
    sendVideo =True


  else:
    bot.sendMessage(chat_id, 'Invalid command.')

         
def capture():
  sendPhoto = False
  camera = cv2.VideoCapture(0)
  fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)
  ret, frame = camera.read() # captures image
  frameCount = 0
    
  while(1):
    
    ret, frame = camera.read() # captures image    
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    frameCount += 1

    # Resize the frame
    resizedFrame = cv2.resize(frame,(0, 0), fx=1, fy=1)
        
    # Get the foreground mask
    fgmask = fgbg.apply(resizedFrame)
  
    # Count all the non zero pixels within the mask
    count = np.count_nonzero(fgmask)

    #print('Frame: %d, Pixel Count: %d' % (frameCount, count))
    cv2.imshow("Mask", fgmask) # displays captured image
    cv2.imshow('Security Feed', resizedFrame)
    if (frameCount > 1 and count > 5000):# Determine how many pixels do you want to detect to be considered "movement"
      
            cv2.putText(resizedFrame, 'Alert...!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                
            cv2.imwrite('photo.jpg',resizedFrame)
            bot.sendMessage(chat_id, 'Unknown movement detected.Take a necessary action')
            print('Sending photo to ' + str(chat_id))
            bot.sendPhoto(chat_id, photo = open('photo.jpg', 'rb'))
                
            #print('Capturing photo...')

    else:
         sendPhoto = cv2.waitKey(1) & 0xff
         if sendPhoto == False:
           break
        
  camera.release()
  cv2.destroyAllWindows()
  


def record():
  fps = 24
  width = 864
  height = 640
  camera = cv2.VideoCapture(0)
  ret = camera.set(3, 864)
  ret = camera.set(4, 480)
  video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")
  name = random.randint(0, 1000)
  print(name)
  if os.path.isdir(str(name)) is False:
    name = random.randint(0, 1000)
    name = str(name)

    name = os.path.join(os.getcwd(), str(name))
    print("ALl logs saved in dir:", name)
    os.mkdir(name)


    
    cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


    start = time.time()
    video_file_count = 1
    video_file = os.path.join(name, str(video_file_count) + ".avi")
    print("Capture video saved location : {}".format(video_file))

    # Create a video write before entering the loop
    video_writer = cv2.VideoWriter(
    video_file, video_codec, fps, (int(camera.get(3)), int(camera.get(4))))

    while camera.isOpened():
        start_time = time.time()
        ret, frame = camera.read()
        if ret == True:
            cv2.imshow("Security Feed", frame)
            if time.time() - start > 10:
                start = time.time()
                video_file_count += 1
                video_file = os.path.join(name, str(video_file_count) + ".avi")
                video_writer = cv2.VideoWriter(
                video_file, video_codec, fps, (int(camera.get(3)), int(camera.get(4))))
            
        # No sleeping! We don't want to sleep, we want to write
        # time.sleep(10)

    # Write the frame to the current video writer
            video_writer.write(frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
              
                break
        else:
          break
    camera.release()
    cv2.destroyAllWindows()


bot = telepot.Bot('883358290:AAFbjYe3-JrhKQWo3WkrYt8kB-5Y9cevAd4')
bot.message_loop(handle)

print('Bot ready!')

sendPhoto = False
sendVideo = False

try:
  while True:
    if sendPhoto == True:
      #sendPhoto = False
      capture()
      
    elif sendVideo == True:
      #sendVideo = False
      record()

  
except KeyboardInterrupt:
  camera.release()
