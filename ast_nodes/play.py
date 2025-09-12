from dataclasses import dataclass
from .base import Node

# Play-mode commands

@dataclass
class File(Node):
    filename: str

@dataclass
class Word(Node):
    secret: str = None  

class Words(Node):
    pass  # lists all the possible secret words

@dataclass
class MaxGuesses(Node):
    n: int

@dataclass
class Guess(Node):
    word: str

class Edit(Node):
    pass

class Help(Node):
    pass

class Edit(Node):
    pass

class Quit(Node):
    pass