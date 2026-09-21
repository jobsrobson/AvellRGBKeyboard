from lightbar import Lightbar


bar = Lightbar()

print("RGB bruto:", bar.get_raw_rgb())
print("RGB 0–255:", bar.get_rgb())
print("Animação:", bar.get_animation())