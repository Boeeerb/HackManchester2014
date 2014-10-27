import ws2812
import time
import png
import urllib
import threading

brightness = 10 # Less is brighter
channels = 4

ws2812.init(64)

ra = [0] * 64
ga = [0] * 64
ba = [0] * 64

class updateword(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
 
  def run(self):
    while True:
      print "Run updater"
      self.get()
      time.sleep(5)

  def get(self):
    response = urllib.urlopen('http://boeeerb.co.uk/hm/word.txt')
    word = response.read()
    wordfile = open("word2.txt", "w")
    wordfile.write(word)
    wordfile.close()
    print "Updated word"

class rundisp(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def drawpx(self,p,r,g,b):
    global brightness,channels,ra,ga,ba
    x = 0
    ra[p] = r
    ga[p] = g
    ba[p] = b
    while x < 64:
      ws2812.setPixelColor(x,ra[x],ga[x],ba[x])

      x += 1
    ws2812.show()
    time.sleep(5)
    

  def run(self):
    while True:
      wordfile = open("word2.txt", "r")
      word = wordfile.readline().split("\n")
      wordfile.close()

      word1 = word
      word = word[0].split()

      try:
        if word[0] == "0":
          print "draw"
          word1 = [int(n) for n in word1[0].split()]
          pix,r,g,b = word1[1],word1[2],word1[3],word1[4]
        
          self.drawpx(pix,r,g,b)
        elif word[0] == "clear":
          self.clear()
        else:
          self.display(word[0])
      except:
        print "Something exceptional happened"
        time.sleep(2)
      else:
        a=1

  def display(self,input):
    try:
      reader = png.Reader(filename=str(input) +'.png')
    except IOError:
      print "-- File read error --"
    else:
      w, h, pixels, metadata = reader.read()
      pix = list(pixels)
  
      ws2812.clear()

      if h < 8:
        self.static(h,pix)
      else:
        self.move(h,pix)


  def move(self,h,pix):
    x = 0
    y = 0
    z = 0
    s = 0
    global brightness,channels
    totalsprites = h / 8
    while s < totalsprites:
      while x < 8:
        p = list(pix[x+(s*8)])
        while y < 8:
          ws2812.setPixelColor(z, (p[(y*channels)+0]/brightness), (p[(y*channels)+1]/brightness), (p[(y*channels)+2]/brightness))
      #    print p[((y+1)*3)/3], p[((y+2)*3)/3], p[((y+3)*3)/3]
          y += 1
          z += 1
        x += 1
        y = 0
      ws2812.show()
      time.sleep(0.25)
      s += 1
      x = 0
      z = 0

  def static(self,h,pix):
    x = 0
    y = 0
    z = 0
    print h
    global brightness,channels
    while x < 8:
      p = list(pix[x])
      print p
      while y < 8:
        ws2812.setPixelColor(z, (p[(y*channels)+0]/brightness), (p[(y*channels)+1]/brightness), (p[(y*channels)+2]/brightness))
    #    print p[((y+1)*3)/3], p[((y+2)*3)/3], p[((y+3)*3)/3]
        y += 1
        z += 1
      x += 1
      y = 0

    ws2812.show()


  def clear(self):
    global ra, ga, ba
    ws2812.clear()
    ws2812.show()
    ra = [0] * 64
    ga = [0] * 64
    ba = [0] * 64
    time.sleep(5)


  
thread1 = rundisp()
thread2 = updateword()
#thread1.daemon = True
#thread2.daemon = True
thread1.start()
thread2.start()
