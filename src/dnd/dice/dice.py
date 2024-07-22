from typing import Optional

import numpy as np


class Die:
    def __init__(self, n_sides: int, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed=seed)
        self.n_sides = n_sides
    
    def __call__(self) -> int:
        return int(self.rng.uniform(1, self.n_sides + 1))

    def roll_with_bonus(self, bonus: int) -> int:
        """
        Roll a flat roll but with the given bonus value

        Args:
            bonus (int): The bonus to add to the roll, which may be negative
        Returns:
            int: The total of the roll with bonus
        """
        return self() + bonus
    
    def roll_with_advantage(self, bonus: int = 0) -> int:
        """
        Roll with advantage (roll 2 and keep the highest) with a possible bonus (which can be negative)

        Args:
            bonus (int): The bonus to apply to the roll, which may be negative. Default 0
        Returns:
            int: The total of the advantaged roll with bonus
        """
        return max(self(), self()) + bonus
    
    def roll_with_disadvantage(self, bonus: int = 0) -> int:
        """
        Roll with advantage (roll 2 and keep the lowest) with a possible bonus (which can be negative)

        Args:
            bonus (int): The bonus to apply to the roll, which may be negative. Default 0
        Returns:
            int: The total of the disadvantaged roll with bonus
        """
        return min(self(), self()) + bonus
    
    def roll_keep_highest(self, number_to_roll: int, number_to_keep: Optional[int] = None) -> int:
        """
        Roll some number N of dice and keep the highest M of them

        Args:
            number_to_roll (int): The total number of dice to be rolled
            number_to_keep (optional int): The total number of rolls to keep. Only the `number_to_keep` highest will be kept. If None (default), keep all dice
        Returns:
            int: The sum of the `number_to_keep` highest rolls of this die
        Raises:
            ValueError: If `number_to_keep` > `number_to_roll`
        """
        if number_to_keep is None:
            number_to_keep = number_to_roll
        if number_to_keep > number_to_roll:
            raise ValueError(f"Invalid values for roll_keep_highest: number_to_keep {number_to_keep} is larger than number_to_roll {number_to_roll}")
        keep_dice = np.array([self() for _ in range(number_to_keep)])
        number_rolled = number_to_keep
        while number_rolled < number_to_roll:
            number_rolled += 1
            new_roll = self()
            if np.any(keep_dice < new_roll):
                number_rolled[np.argmin(keep_dice < new_roll)] = new_roll
        return keep_dice.sum()