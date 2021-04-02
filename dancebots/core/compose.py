#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .move import Move
from .light import Light


class Compose:
    """Combine moves and lights into a single composition"""

    _steps = []

    def __init__(self, moves, lights):
        zeros = [0] * 8

        if lights != None:
            # Add lights to choreography
            for light in lights.steps:
                if light["beats"] > 1:
                    # Expand choreography list for lights lasting longer than a beat
                    for i in range(light["beats"]):
                        self._steps.append(
                            {
                                "motor_l": zeros,
                                "motor_r": zeros,
                                "leds": light["leds"],
                                "beats": 1,
                            }
                        )
                else:
                    self._steps.append(
                        {
                            "motor_l": zeros,
                            "motor_r": zeros,
                            "leds": light["leds"],
                            "beats": light["beats"],
                        }
                    )

        if moves != None:
            # Add moves to choreography
            move_i = 0
            beat_cnt = 0
            for step in self._steps:
                if beat_cnt == moves.steps[move_i]["beats"]:
                    # Go to the next move
                    move_i += 1
                    beat_cnt = 0

                # If next move exists
                if move_i < len(moves.steps):
                    step["motor_l"] = moves.steps[move_i]["motor_l"]
                    step["motor_r"] = moves.steps[move_i]["motor_r"]
                    beat_cnt += step["beats"]

            # If there are remaining moves
            if beat_cnt != 0:
                for i in range(moves.steps[move_i]["beats"] - beat_cnt):
                    self._steps.append(
                        {
                            "motor_l": moves.steps[move_i]["motor_l"],
                            "motor_r": moves.steps[move_i]["motor_r"],
                            "leds": zeros,
                            "beats": 1,
                        }
                    )
                move_i += 1

            if move_i < len(moves.steps):
                # Add moves to choreography
                for move in moves.steps[move_i::]:
                    if move["beats"] > 1:
                        # Expand choreography list for moves lasting longer than a beat
                        for i in range(move["beats"]):
                            self._steps.append(
                                {
                                    "motor_l": move["motor_l"],
                                    "motor_r": move["motor_r"],
                                    "leds": zeros,
                                    "beats": 1,
                                }
                            )
                    else:
                        self._steps.append(
                            {
                                "motor_l": move["motor_l"],
                                "motor_r": move["motor_r"],
                                "leds": zeros,
                                "beats": move["beats"],
                            }
                        )

    @property
    def steps(self):
        return self._steps

    def __str__(self):
        # https://blog.softhints.com/python-print-pretty-table-list/
        summary = "\n"

        header = ["Step", "Beats", "Left Motor", "Right Motor", "LEDs"]
        format_row = "{:<6} {:<7} {:<26} {:<26} {:<26}"
        summary += format_row.format(*header)
        summary += "\n"

        for num, step in enumerate(self._steps, start=1):
            summary += format_row.format(
                num,
                step["beats"],
                str(step["motor_l"]),
                str(step["motor_r"]),
                str(step["leds"]),
            )
            summary += "\n"

        return summary
