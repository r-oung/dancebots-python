class Primitives(Move):
    """Choreography base class.

    This class consists of both motion and LED choreographies.
    """

    def insert_motion_tandf(self, index, freq, period):
        """Moves the robot forwards and backwards repeatedly.

        Args:
                index (int): Time index for when to start the dance primitive [sec]
                freq (float): Frequency in which to operate the dance primitive [Hz]
                period (int): Length of time in which to operate the dance primitive [sec]

        Returns:
                None

        """
        reps = freq * period  # number of dance primitive repetitions

        # unit conversion from [sec] to [commands]
        cmd_index, cmd_period = self.time2cmd(index, freq)

        # insert dance primitive
        for i in range(reps):
            self.move_forward(cmd_index, int(0.5 * cmd_period))
            cmd_index += cmd_period

            self.move_backward(cmd_index, int(0.5 * cmd_period))
            cmd_index += cmd_period

        return

    def insert_motion_twist(self, index, freq, period):
        """Twists the robot left and right repeatedly.

        Args:
                index (int): Time index for when to start the dance primitive [sec]
                freq (float): Frequency in which to operate the dance primitive [Hz]
                period (int): Length of time in which to operate the dance primitive [sec]

        Returns:
                None

        """
        reps = freq * period  # number of dance primitive repetitions

        # unit conversion from [sec] to [commands]
        cmd_index, cmd_period = self.time2cmd(index, freq)

        # insert dance primitive
        for i in range(reps):
            self.twist_left(cmd_index, int(0.5 * cmd_period))
            cmd_index += cmd_period

            self.twist_right(cmd_index, int(0.5 * cmd_period))
            cmd_index += cmd_period

        return

    def insert_light_pattern_a(self, index, freq, period):
        """LEDs change randomly for a set number of repetitions.

        Args:
                index (int): Time index for when to start the light pattern [sec]
                freq (float): Frequency in which to operate the light pattern [Hz]
                period (int): Length of time in which to operate the dance primitive [sec]

        Returns:
                None

        """
        reps = freq * period  # number of light pattern repetitions

        # insert LED pattern
        for i in range(reps):
            val = random.getrandbits(8)
            self.blink_led(index, freq, val, val)

        return

    def insert_light_pattern_b(self, index, freq, period):
        """LEDs change turn on and off for a set number of repetitions.

        Args:
                index (int): Time index for when to start the light pattern [sec]
                freq (float): Frequency in which to operate the light pattern [Hz]
                period (int): Length of time in which to operate the dance primitive [sec]

        Returns:
                None

        """
        reps = freq * period  # number of light pattern repetitions

        # insert LED pattern
        for i in range(reps):
            self.blink_led(index, freq, 0xFF, 0x00)

        return

    def insert_light_pattern_c(self, index, freq, period):
        """Description not provided.

        Args:
                index (int): Time index for when to start the light pattern [sec]
                freq (float): Frequency in which to operate the light pattern [Hz]
                period (int): Length of time in which to operate the dance primitive [sec]

        Returns:
                None

        """
        reps = freq * period  # number of light pattern repetitions

        # insert LED pattern
        val1 = random.getrandbits(8)
        val2 = ~val1

        for i in range(reps):
            self.blink_led(index, freq, val1, val2)

        return

    def __repr__(self):
        return "Choreography({}, {})".format(self.samples, self.sampling_rate)
