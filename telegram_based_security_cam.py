import telepot
import numpy as np
import cv2


def handle(msg):
  global sendPhoto
  global sendVideo
  global chat_id
  
  chat_id = msg['chat']['id']
  command = msg['text']
  
  print('Message received from ' + str(chat_id))
  
  if command == '/start':
      
    sendPhoto = False
    bot.sendMessage(chat_id, "Hello, I'm your secutity assistance sir")

    camera = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)
    frameCount = 0

    while(1):
        ret, frame = camera.read() # captures image


        frameCount += 1

        # Resize the frame
        resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        # Get the foreground mask
        fgmask = fgbg.apply(resizedFrame)
  
        # Count all the non zero pixels within the mask
        count = np.count_nonzero(fgmask)

        print('Frame: %d, Pixel Count: %d' % (frameCount, count))
        cv2.imshow("Mask", fgmask) # displays captured image
        cv2.imshow('Frame', resizedFrame)
        if (frameCount > 1 and count > 5000):# Determine how many pixels do you want to detect to be considered "movement"
      
                cv2.putText(resizedFrame, 'Alert...', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imwrite('photo.jpg',resizedFrame)
                bot.sendMessage(chat_id, 'Unknown movement detected.Take a necessary action')
                print('Sending photo to ' + str(chat_id))
                bot.sendPhoto(chat_id, photo = open('photo.jpg', 'rb'))
                #print('Capturing photo...')

        else:
            sendPhoto = False
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        
    camera.release()
    cv2.destroyAllWindows()
  
#def capture():

  elif command == '/photo':
      
      sendVideo =True
  
  else:
    bot.sendMessage(chat_id, 'Invalid command.')
  
  
  

bot = telepot.Bot('883358290:AAFbjYe3-JrhKQWo3WkrYt8kB-5Y9cevAd4')
bot.message_loop(handle)

print('Bot ready!')

#sendPhoto = False

#try:
  #while True:
    #if sendPhoto == True:
       #sendPhoto = False
        #capture()
  
      
        
  
#except KeyboardInterrupt:
    #camera.release()
