from nxtcommon import *

BOGUS_TURN_VALUE = 8
BASE_DISTANCE = 20 
SLEEP_TIME = .1
BUFFER = 5
SEARCH_CUTOFF = 25
BASE_SPEED = 50

bot = find_bot()

front_ultrasonic = UltrasonicSensor(bot,PORT_1)
left_ultrasonic = UltrasonicSensor(bot,PORT_2)

left_motor = Motor(bot,PORT_A)
right_motor = Motor(bot,PORT_C)

def check_stuck(front_distance, old_front_distance, turn):
	if front_distance == old_front_distance:
		set_turn(left_motor,right_motor,LEFT,-BASE_SPEED,STRAIGHT)
		sleep(SLEEP_TIME)
		turn = set_turn(left_motor,right_motor,(not turn),BASE_SPEED,PIVOT)
		sleep(SLEEP_TIME/2)
		set_turn(left_motor,right_motor,LEFT,BASE_SPEED,STRAIGHT)
	return turn
	

turn = BOGUS_TURN_VALUE

try:
	set_turn(left_motor,right_motor,RIGHT,BASE_SPEED,STRAIGHT)
	sleep(SLEEP_TIME*2)
		
	front_distance = front_ultrasonic.get_sample()
	left_distance = left_ultrasonic.get_sample()
	
	while True:
		old_front_distance = front_distance
		old_left_distance = left_distance
		
		front_distance = front_ultrasonic.get_sample()
		left_distance = left_ultrasonic.get_sample()
		
		turn=check_stuck(front_distance, old_front_distance, turn)
		
		print front_distance,left_distance
	
		if left_distance > BASE_DISTANCE :
			print "found opening"
			turn = set_turn(left_motor,right_motor,RIGHT,BASE_SPEED/4,PIVOT)
			sleep(SLEEP_TIME*2)
			older_front_distance = front_distance
			i = 0
			while (abs(left_ultrasonic.get_sample() - older_front_distance) > BUFFER) and i < SEARCH_CUTOFF :
				old_front_distance = front_distance
				front_distance = front_ultrasonic.get_sample()
				i = i + 1
				print i
					
			print "found edge"
			set_turn(left_motor,right_motor,LEFT,BASE_SPEED/2,PIVOT)
			sleep(SLEEP_TIME/2)
			set_turn(left_motor,right_motor,LEFT,BASE_SPEED,STRAIGHT)
			sleep(SLEEP_TIME*5)
			
		elif front_distance < BASE_DISTANCE/2:	
			print "hit front"
			turn = set_turn(left_motor,right_motor,LEFT,BASE_SPEED/3,PIVOT)	
			sleep(SLEEP_TIME*3)
			while front_distance < BASE_DISTANCE*2:
				old_front_distance = front_distance
				front_distance = front_ultrasonic.get_sample()
				turn=check_stuck(front_distance, old_front_distance, turn)
			print "found opening"
			set_turn(left_motor,right_motor,RIGHT,BASE_SPEED/2,PIVOT)
			sleep(SLEEP_TIME/2)
			set_turn(left_motor,right_motor,LEFT,BASE_SPEED,STRAIGHT)
			sleep(SLEEP_TIME*3.5)
finally:
	stop_motors(bot)	

