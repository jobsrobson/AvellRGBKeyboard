from hardware import AvellKeyboard
from keyboard import KEYS


kbd = AvellKeyboard()

print("ITE 8291:", kbd.buffer_path)
print("W antes:", kbd.get_rgb(KEYS["W"].channel))
print("A antes:", kbd.get_rgb(KEYS["A"].channel))
print("Space antes:", kbd.get_rgb(KEYS["Space"].channel))

print()
print("Aplicando frame de teste...")

with kbd.batch():
    kbd.set_rgb(KEYS["W"].channel, 255, 0, 255)
    kbd.set_rgb(KEYS["A"].channel, 0, 255, 255)
    kbd.set_rgb(KEYS["Space"].channel, 255, 255, 0)

print("OK.")
print("W:", kbd.get_rgb(KEYS["W"].channel))
print("A:", kbd.get_rgb(KEYS["A"].channel))
print("Space:", kbd.get_rgb(KEYS["Space"].channel))