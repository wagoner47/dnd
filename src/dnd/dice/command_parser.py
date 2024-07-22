from typing import Tuple
import re

from dice import Die


class DiceCommandParser:
    def __init__(self, input_string: str):
        self.command_strings = input_string.split()
        for command_pos, command_string in enumerate(self.command_strings):
            if command_string in "\u00F7\u00D7+-":
                self.command_strings[command_pos + 1] = f"{command_string}{self.command_strings[command_pos + 1]}"
        self.command_strings = [cs for cs in self.command_strings if cs not in "\u00F7\u00D7+-"]
        self.output_strings = []
        self.output_value = 0

    @staticmethod
    def roll_dice(num_sides: int, num_dice: int) -> Tuple[int, str]:
        dice_object = Die(num_sides)
        values = [dice_object() for _ in range(num_dice)]
        output = f"({' + '.join(str(v) for v in values)}"
        value = sum(values)
        return value, output

    @staticmethod
    def roll_keep_highest(num_sides: int, num_dice: int, num_to_keep: int) -> Tuple[int, str]:
        dice_object = Die(num_sides)
        values = [dice_object() for _ in range(num_dice)]
        output = f"KH{num_to_keep}({', '.join(str(v) for v in values)})"
        values.sort(reverse=True)
        value = sum(values[:num_to_keep])
        return value, output

    @staticmethod
    def roll_with_advantage(num_sides: int) -> Tuple[int, str]:
        dice_object = Die(num_sides)
        values = [dice_object() for _ in range(2)]
        output = f"Adv({', '.join(str(v) for v in values)})"
        value = max(values)
        return value, output

    @staticmethod
    def roll_with_disadvantage(num_sides: int) -> Tuple[int, str]:
        dice_object = Die(num_sides)
        values = [dice_object() for _ in range(2)]
        output = f"Dis({', '.join(str(v) for v in values)})"
        value = min(values)
        return value, output

    @staticmethod
    def multiply(value_to_multiply: int, output_string: str, output_value: int) -> Tuple[int, str]:
        new_output_string = f"{output_string} \u00D7 {value_to_multiply}"
        new_output_value = output_value * value_to_multiply
        return new_output_value, new_output_string

    @staticmethod
    def divide(value_to_divide: int, output_string: str, output_value: int) -> Tuple[int, str]:
        new_output_string = f"{output_string} \u00F7 {value_to_divide}"
        new_output_value = output_value // value_to_divide
        return new_output_value, new_output_string

    @staticmethod
    def add(value_to_add: int, output_string: str, output_value: int) -> Tuple[int, str]:
        new_output_string = f"{output_string} + {value_to_add}"
        new_output_value = output_value + value_to_add
        return new_output_value, new_output_string

    @staticmethod
    def subtract(value_to_subtract: int, output_string: str, output_value: int) -> Tuple[int, str]:
        new_output_string = f"{output_string} - {value_to_subtract}"
        new_output_value = output_value - value_to_subtract
        return new_output_value, new_output_string

    def _parse_basic(self, string_to_parse: str, current_string: str, current_value: int) -> Tuple[int, str]:
        try:
            new_value = int(string_to_parse)
            if not (current_value == 0 and current_string == ""):
                raise TypeError("Got a number without an operator in the middle of the command")
            current_value = new_value
            current_string = string_to_parse
        except ValueError:
            if string_to_parse[0] in "\u00D7\u00F7+-":
                rhs_value, rhs_string = self._parse_basic(string_to_parse[1:], "", 0)
                if string_to_parse.startswith("\u00D7"):
                    current_value, current_string = self.multiply(rhs_value, current_string, current_value)
                elif string_to_parse.startswith("\u00F7"):
                    current_value, current_string = self.divide(rhs_value, current_string, current_value)
                elif string_to_parse.startswith("+"):
                    current_value, current_string = self.add(rhs_value, current_string, current_value)
                else:
                    current_value, current_string = self.subtract(rhs_value, current_string, current_value)
            elif string_to_parse.startswith("("):
                parenthetical_value = 0
                parenthetical_string = "("

            if m := re.match(r"(\d*)d(\d+)", string_to_parse) is not None:
                num_dice = m.group(1) if m.group(1) != "" else 1
                num_sides = m.group(2)
                new_value, new_string = self.roll_dice(num_sides, num_dice)
            elif m := re.match(r"(\d+)d(\d+)KH(\d+)", string_to_parse) is not None:
                num_dice = m.group(1)
                num_sides = m.group(2)
                num_to_keep = m.group(3)
                new_value, new_string = self.roll_keep_highest(num_sides, num_dice, num_to_keep)
            elif m := re.match(r"(\d*)Adv\(d(\d+)\)", string_to_parse) is not None:
                num_dice = m.group(1) if m.group(1) != "" else 1
                num_sides = m.group(2)
                new_value = 0
                new_string = ""
                for _ in range(num_dice):
                    v, s = self.roll_with_advantage(num_sides)
                    new_value += v
                    new_string += f" + {s}"
            elif m := re.match(r"(\d*)Dis\(d(\d+)\)", string_to_parse) is not None:
                num_dice = m.group(1) if m.group(1) != "" else 1
                num_sides = m.group(2)
                new_value = 0
                new_string = ""
                for _ in range(num_dice):
                    v, s = self.roll_with_disadvantage(num_sides)
                    new_value += v
                    new_string += f" + {s}"
