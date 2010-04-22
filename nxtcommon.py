import nxt.locator
from threading import Thread
from nxt.sensor import *
from nxt.motor import *
from time import sleep
import sys

(RIGHT,LEFT)=(True,False) 
#this way, !RIGHT == LEFT 
BASE_SPEED=50
PIVOT=-1
LEAN=.5
STRAIGHT=1

DEFAULT_TESTS=2

def find_bot():
	print 'Looking for brick 3 ...'
	sock = nxt.locator.find_one_brick(host='00:16:53:06:EA:61',name='NXT')
	print 'Found brick 3 or timed-out ...'
	if sock:
		print 'Connecting to the brick ...'
		bot = sock.connect()
		print 'Connected to the brick or timed-out ...'
		if bot:
			return bot
		else:
			print 'Could not connect to NXT brick'
			exit            
	else:
		print 'No NXT bricks found'
		exit

def stop_motors(bot):
	Motor(bot, PORT_ALL).stop(False)

def stop_bot(bot):
	stop_motors(bot)
	bot.sock.close()

def set_turn(left_wheel,right_wheel,direction,speed=BASE_SPEED,turn_ratio=LEAN):
	if direction == LEFT:
		left_wheel.run(speed,True)
		right_wheel.run(speed*turn_ratio,True)
	elif direction == RIGHT:
		left_wheel.run(speed*turn_ratio,True)
		right_wheel.run(speed,True)
	return direction

def sense(sensor, tests = DEFAULT_TESTS):
	gathered = 0
	for i in range(0,tests):
		gathered += sensor.get_sample()
	return (gathered/tests)

def breakpoint(dodie,bot):
	if dodie:
		stop_bot(bot)
		exit()

def Motor.precise_update(tachos,speed=BASE_SPEED):
	start_tachos = self.get_output_state()[7]
	self.update(speed,tachos,True)
	error = self.get_output_state()[7] - (start_tachos + tachos)
	while abs(error) > 5:
		direction = abs(error) / error
		self.run(direction*speed)
		time.sleep(.1)
		self.stop(False)
		error = self.get_output_state()[7] - (start_tachos + tachos)

		

