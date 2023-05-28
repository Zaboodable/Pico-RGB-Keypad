import storage
import time
from rgbkeypad import RGBKeypad

# Disable USB Storage by default
ENABLE_STORAGE = False

# Setup keypad
pad = RGBKeypad()
pad.brightness = 1

# Colors for keys
color_boot = (64,64,64)
color_enable = (64,255,64)
color_disable = (255,64,64)
color_highlight = (0,0,255)


# Create and setup keys
keys=[None]*16
for y in range(4):
    for x in range(4):
        key = pad[x,y]
        keys[x + y*4] = key
        key.color = color_boot


# Boot key is the top left key (from my perspective)
boot_key = 15
keys[boot_key].color = color_highlight

# Counter variables for key press check
# dont want to wait forever
counter = 0
counter_time = 2.5
counter_delay = 0.05
counter_max = int(counter_time/counter_delay)

# USB Storage check loop
while counter < counter_max:
    counter += 1

    board_state = pad.get_keys_pressed()
    if (board_state[boot_key]):
        keys[boot_key].color = color_enable
        ENABLE_STORAGE = True
        break    
    time.sleep(counter_delay)
#while

# Enable or disable USB Storage
if (ENABLE_STORAGE):
    for key in keys:
        key.color = color_enable
    storage.enable_usb_drive()
else:
    for key in keys:
        key.color = color_disable
    storage.disable_usb_drive()

# Wait a second before continuing
time.sleep(1)

