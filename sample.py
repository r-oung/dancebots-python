def main():
	"""
	INPUT
		arg0: dance choreography (.CSV)
		arg1: light choreographyc (.CSV)

	OUTPUT
		choreography file (.WAV) in Dancebot protocol
	"""


	"""
	A dance choreography consists of a list of dance primitives with associated parameters:

	['DANCE-PRIMITIVE-NAME', INDEX, FREQUENCY, PERIOD]
	
	  DANCE-PRIMITIVE-NAME: Name of the dance primitive [to_and_fro, twist]
	 				 INDEX: Time index in which to start the dance primitive [sec]
	 			 FREQUENCY: Frequency in which to operate the dance primitive [Hz]
	  				PERIOD: Length of time in which to operate the dance primitive [sec]
	"""
	rate, data = wavfile.read("test.wav")

	motion_list = [
		('TANDF', 5, 1, 10),
		('TWIST', 10, 2, 5),
		('TANDF', 30, 1, 7),
		('TWIST', 60, 2, 4),
	]

	lights_list = [
		('A', 5, 1, 10),
		('B', 15, 5, 10),
		('C', 25, 2, 5)]

	print("No. Samples: {}".format(data.shape[0]))
	print("Sampling Rate: {} Hz".format(rate))

	c = Choreography(data.shape[0], rate)
	print(c)

	# reverse motion-list such that the first element we pop from the list if the first dance primitive
	motion_list.reverse()

	# step through the motion-list and convert from dance primitives to motor commands
	for i in range(len(motion_list)):
		primitive, index, freq, period = motion_list.pop()
		"""
		primitive: name of the dance primitive
		index: time index for when to start the dance primitive [sec]
		freq: frequency in which to operate the dance primitive [Hz]
		period: length of time in which to operate the dance primitive [sec]
		"""

		# insert dance primitives
		if primitive == "TANDF":
			print("Add To and Fro")
			c.insert_motion_tandf(index, freq, period)
		elif primitive == "TWIST":
			print("Add Twist")
		else:
			print("No such primitive exists!")

	# step through the lights-list and convert from light pattern to LED commands
	for i in range(len(lights_list)):
		pattern, index, freq, period = lights_list.pop()
		"""
		pattern: name of the light pattern
		index: time index for when to start the light pattern [sec]
		freq: frequency in which to operate the light pattern [Hz]
		period: length of time in which to operate the light pattern [sec]
		"""

		# insert light pattern
		if pattern == "A":
			c.insert_light_pattern_a(index, freq, period)
		elif pattern == "B":
			c.insert_light_pattern_b(index, freq, period)
		elif pattern == "C":
			c.insert_light_pattern_c(index, freq, period)
		else:
			print("No such pattern exists!")

	# plot stuff
	t = range(0, c.cmds_total)
	t = [x * c.msg_intvl for x in t]

	plt.figure(1)
	plt.subplot(211)
	plt.title("Motor Commands")
	plt.plot(t, c.cmds_motor_left, label="Left Motor")
	plt.plot(t, c.cmds_motor_right, label="Right Motor")
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.legend()
	plt.subplot(212)
	plt.title("LED Commands")
	plt.plot(t, c.cmds_led)
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.show()

if __name__ == "__main__":
	main()
