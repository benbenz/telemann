from pedalboard import load_plugin
from PIL import Image

instrument = load_plugin('/Library/Audio/Plug-Ins/Components/Diva.component')

np_arr = instrument.capture()
im = Image.fromarray(np_arr)
rgb_image = im.convert('RGB')
rgb_image.save("your_file.jpeg")

# print(*np_arr.flatten().tolist())