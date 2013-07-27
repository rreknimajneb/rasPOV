from time import sleep
import RPi.GPIO as GPIO
import sys
import benPovLib
from benPovLib import AlphaDic as AlphaDic

#add file reading support some day
#after figure out how to leave blank input for default values
#http://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible

RATE = 0.05
LETTERSPACER = 3
SPACES = True
TALL = 8
PINREF =  (22,18,16,15,13,12,11,7)
phrase="default phrase" 
loops = 1

def main():
	boardSetup()
	setSpace()
	getInput()
	for lps in range(loops):
		print "loop ",lps,"of ",loops
		for x in range(len(phrase)):
			letter = phrase[x]
			#print letter,len(AlphaDic[letter])/8,AlphaDic[letter],len(AlphaDic[letter])
			drawLetter(letter)
			drawSpace()  #actually space BETWeen letters
			sleep(RATE*LETTERSPACER)
	boardSetup()
	boardCleanUp()

def boardSetup():
	GPIO.setmode(GPIO.BOARD)
	for loopy in range(len(PINREF)):
		GPIO.setup(PINREF[loopy],GPIO.OUT)
		#print "loop=",loopy,"pinref=",PINREF[loopy]
		GPIO.output(PINREF[loopy], False)
	print "values of dictionary",len(AlphaDic.keys() )

	#print "GPIO pin reference =",PINREF
	if len(PINREF)<TALL:
		print "error!!!!  PINREF smaller than width!"
	else:
		print "looks good. PINREF at least width length"
		
def boardCleanUp():
	for x in range(len(PINREF)):
		GPIO.output(PINREF[x], False)
	GPIO.cleanup()
		

def drawLetter(let):
	global AlphaDic,RATE,TALL,PINREF,LETTERSPACER
	county = 0
	wide = len(AlphaDic[let])/TALL
	letBlock = AlphaDic[let]
	print "county=",county,"wide=",wide,"letBlock=",letBlock
	for y in range(wide):
		for x in range(TALL):
			#print letBlock[county],
			if letBlock[county]=='1':
				print '*', #ON
				GPIO.output(PINREF[x], True)
			elif '0':
				print ' ', #OFF#
				GPIO.output(PINREF[x], False)
			else :
				print '?',
			county += 1
		sleep(RATE)
		print "yloop=",y

#replace w/ Class initialization
def setSpace():
	global PINREF, SPACES
	space = AlphaDic[' ']
	sums = 0
	print "the space is ",space
	for x in range(len(space)):
                #print int(space[x]),
                sums = sums + int(space[x])
        print "sums=",sums," space len=",len(space),'SPACES=',SPACES,
        if sums<len(space) :
                SPACES = False
                print "set space to False   ",
        print "SPACES set to ",SPACES
	


def drawSpace():
	global TALL , PINREF
	for x in range(len(PINREF)):
		GPIO.output(PINREF[x],SPACES)

def getInput():
	global RATE, phrase, loops
	bensfile = open('text.txt','r')
	container = bensfile.readlines(1)

	if len(sys.argv) < 2:
		print "no command line arguments entered.  len of argv=",len(sys.argv)
		RATE = 0.003
		RATE = raw_input("how fast to blink? (default: %f):\n" % RATE)  or RATE
		print "rate type=",type(RATE),
		RATE = float(RATE)
		print "now the rate type is=",type(RATE)
		phrase = 'default phrase'
		phrase = raw_input("Enter a blink phrase (default: %s):\n" % phrase) or phrase


		loops = int(raw_input('how many times should this message loop?'))


	elif len(sys.argv) >= 2:
		print "command line arguments are ",sys.argv
		if sys.argv[1] == 'auto':
			print container[0],"<< thats the file contents"
			print "auto command line arguments found"
			print "textFileInput=", str(container)
			loops = 650
			phrase = str(container[0].strip('\n'))
			RATE = 0.004
	else:

		print "########### command lin argv not recognize.  defaulting#####"

		RATE =float( raw_input('enter the rate (speed)'))
		phrase = 'default phrase'
		phrase = raw_input("Enter a string (default: %s):\n" % phrase) or phrase
		loops = int(raw_input('how many times should this message loop?'))
	############################

if __name__ == '__main__':
	main()

#http://www.tutorialspoint.com/python/python_dictionary.htm
#http://www.tutorialspoint.com/python/python_variable_types.htm
