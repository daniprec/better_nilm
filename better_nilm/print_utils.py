import os
import sys


class HiddenPrints:
    """
    Hides print outputs
    Credit: Alexander Chzhen, on StackOverflow
    """

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
