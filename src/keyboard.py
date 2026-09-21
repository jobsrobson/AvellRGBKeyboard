from dataclasses import dataclass


@dataclass(frozen=True)
class Key:
    name: str
    channel: int


KEYS = {
    # Row 0
    "Ctrl_L": Key("Ctrl_L", 0),
    "Fn": Key("Fn", 2),
    "Super": Key("Super", 3),
    "Alt": Key("Alt", 4),
    "Space": Key("Space", 7),
    "AltGr": Key("AltGr", 10),
    "Menu": Key("Menu", 11),
    "Ctrl_R": Key("Ctrl_R", 12),
    "Left": Key("Left", 13),
    "Down": Key("Down", 14),
    "Right": Key("Right", 15),

    # Row 1
    "Shift_L": Key("Shift_L", 21),
    "Backslash": Key("Backslash", 23),
    "Z": Key("Z", 24),
    "X": Key("X", 25),
    "C": Key("C", 26),
    "V": Key("V", 27),
    "B": Key("B", 28),
    "N": Key("N", 29),
    "M": Key("M", 30),
    "Comma": Key("Comma", 31),
    "Period": Key("Period", 32),
    "Semicolon": Key("Semicolon", 33),
    "Slash": Key("Slash", 34),
    "Shift_R": Key("Shift_R", 35),
    "Up": Key("Up", 36),
    "End": Key("End", 37),

    # Row 2
    "CapsLock": Key("CapsLock", 42),
    "A": Key("A", 44),
    "S": Key("S", 45),
    "D": Key("D", 46),
    "F": Key("F", 47),
    "G": Key("G", 48),
    "H": Key("H", 49),
    "J": Key("J", 50),
    "K": Key("K", 51),
    "L": Key("L", 52),
    "Cedilla": Key("Cedilla", 53),
    "Tilde": Key("Tilde", 54),
    "BracketRight": Key("BracketRight", 55),
    "PgDn": Key("PgDn", 57),

    # Row 3
    "Tab": Key("Tab", 63),
    "Q": Key("Q", 65),
    "W": Key("W", 66),
    "E": Key("E", 67),
    "R": Key("R", 68),
    "T": Key("T", 69),
    "Y": Key("Y", 70),
    "U": Key("U", 71),
    "I": Key("I", 72),
    "O": Key("O", 73),
    "P": Key("P", 74),
    "Grave": Key("Grave", 75),
    "BracketLeft": Key("BracketLeft", 76),
    "Enter": Key("Enter", 77),
    "PgUp": Key("PgUp", 78),

    # Row 4
    "Quote": Key("Quote", 84),
    "1": Key("1", 85),
    "2": Key("2", 86),
    "3": Key("3", 87),
    "4": Key("4", 88),
    "5": Key("5", 89),
    "6": Key("6", 90),
    "7": Key("7", 91),
    "8": Key("8", 92),
    "9": Key("9", 93),
    "0": Key("0", 94),
    "Minus": Key("Minus", 95),
    "Equal": Key("Equal", 96),
    "Pause": Key("Pause", 97),
    "Backspace": Key("Backspace", 98),
    "Home": Key("Home", 99),

    # Row 5
    "Esc": Key("Esc", 105),
    "F1": Key("F1", 106),
    "F2": Key("F2", 107),
    "F3": Key("F3", 108),
    "F4": Key("F4", 109),
    "F5": Key("F5", 110),
    "F6": Key("F6", 111),
    "F7": Key("F7", 112),
    "F8": Key("F8", 113),
    "F9": Key("F9", 114),
    "F10": Key("F10", 115),
    "F11": Key("F11", 116),
    "F12": Key("F12", 117),
    "Insert": Key("Insert", 118),
    "PrtSc": Key("PrtSc", 119),
    "Delete": Key("Delete", 120),
}