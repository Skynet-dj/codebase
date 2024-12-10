import os
FONT_DIR = "fonts"
fonts = [f for f in os.listdir(FONT_DIR)]
for i in fonts:
    print(i)
    os.system(f"pyfiglet -L {FONT_DIR}/{i}")