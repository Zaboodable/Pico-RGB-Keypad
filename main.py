import time
import random
import socketpool
import wifi
import ipaddress

from rgbkeypad import RGBKeypad
import usb_hid
import storage

from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_uk import KeyboardLayout
from keycode_win_uk import Keycode
from adafruit_httpserver import Server, Request, Response, FileResponse, JSONResponse, GET, POST, PUT, DELETE

pad = RGBKeypad()
pad.brightness = 1



kbd = Keyboard(usb_hid.devices)

BUTTON_COUNT = 16
buttons = [None]*BUTTON_COUNT

brightness_max = 1
brightness_mid = 0.5
brightness_min = 0.05

class Colors():
    Red = (255,0,0)
    Green = (0,255,0)
    Blue = (0,0,255)
    Yellow = (255,255,0)
    Cyan = (0,255,255)
    Magenta = (255,0,255)
    White = (255,255,255)
    Black = (0,0,0)

    def random():
        r = random.random()
        g = random.random()
        b = random.random()
        m = max(r,g,b)
        s = 1/m
        c = (int(r * s * 255), int(g * s * 255), int(b * s * 255)) 
        return c

class ButtonGrid():
    buttons = []
    size = 0
    count = 0

    def __init__(self, size):
          self.size = size
          self.buttons = [None]*size
    def add_button(self, button):
        self.buttons[self.count] = button
        button.index = self.count
        button.grid = self
        self.count += 1
    def update(self, board_state):
        for i in range(self.count):
            self.buttons[i].update(board_state[i])

    def randomize_colors(self):     
        for i in range(self.count):
            c = Colors.random()
            self.buttons[i].set_color(c)

    def set_key(self, index, color, brightness):
         self.buttons[index].set_color(color)
         self.buttons[index].set_brightness(brightness)

class Button():
    global kbd, server

    grid = None
    key = None
    color = None

    on_press_callback = None
    on_release_callback = None
    on_hold_callback = None

    index = -1
    pressed_now = False
    pressed_prev = False
    def __init__(self, key, on_press_callback = None, on_release_callback = None, on_hold_callback = None):
        self.key = key
        self.set_color(Colors.random())
        self.set_brightness(brightness_min)
        self.on_press_callback = on_press_callback
        self.on_release_callback = on_release_callback
        self.on_hold_callback = on_hold_callback


    def set_color(self, col):
        self.color = col
        self.key.color = self.color
    def set_brightness(self, brightness):
        self.key.brightness = brightness   

    def update(self, is_pressed):        
        self.pressed_prev = self.pressed_now
        self.pressed_now = is_pressed

        # Call button events        
        if (self.pressed_now and not self.pressed_prev):
                self.on_press()
        if (self.pressed_now and self.pressed_prev):
                self.on_hold()
        if (not self.pressed_now and self.pressed_prev):
                self.on_release()
    
    # Default events
    def on_press(self):
        self.set_brightness(brightness_max)
        print(f'Pressed {self.index}')   
        if (self.on_press_callback is not None):
            self.on_press_callback()
    def on_release(self):
        self.set_brightness(brightness_min)
        self.grid.randomize_colors()
        print(f'Released {self.index}')
        if (self.on_release_callback is not None):
            self.on_release_callback()
    def on_hold(self):
        self.set_brightness(brightness_mid)
        print(f'Holding {self.index}')
        if (self.on_hold_callback is not None):     
            self.on_hold_callback()
    
    # Remote events
    def on_press_remote(self):
        if (self.on_press_callback is not None):
            self.on_press_callback()


        
grid = ButtonGrid(16)
ssid = "RGBWifi"
password = "12345678"
delay = 0.01


def set_global_variable(name, value):
    globals()[name] = value

pool = socketpool.SocketPool(wifi.radio)
set_global_variable('pool', pool)



def run_server():
    server = Server(pool, "/web", debug=True)
    set_global_variable('server', server)
    @server.route("/home")
    def home(request: Request):
        return FileResponse(request, "index.html")   
    @server.route("/api", [GET, POST], append_slash=True)
    def api(request: Request):
        # Get objects
        if request.method == GET:
            return JSONResponse(request, objects)
        # Upload or update objects
        if request.method in POST:
            uploaded_object = request.json()
            
            button_number = uploaded_object.get('button', None)
            if button_number is not None:
                grid.buttons[button_number].on_press_remote()   
                return JSONResponse(request, {"message": f'Button {button_number} clicked'}
            )
            
            usb_status = uploaded_object.get('usbStatus', None)
            if (usb_status is not None):
                return JSONResponse(request, {"message": f'Not Implemented: USB Storage {usb_status}'})

            
            return JSONResponse(request, {"message": f'Invalid request'})
        return JSONResponse(request, {"message": "Bad message"})
    server_ip = ipaddress.IPv4Address("192.168.69.1")
    server.start(str(server_ip))

def setup():
    if (wifi.radio.ap_active == False):
        print("Starting AP")
        wifi.radio.start_ap(ssid=ssid, password=password)
        ip = ipaddress.IPv4Address("192.168.69.1")
        mask = ipaddress.IPv4Address("255.255.255.0")
        gateway = ipaddress.IPv4Address("192.168.69.254")
        wifi.radio.set_ipv4_address_ap(ipv4 = ip, netmask=mask, gateway=gateway)
        wifi.radio.start_dhcp_ap()

    # Start web server
    run_server()

    for y in range(4):
        for x in range(4):
            button =  Button(pad[x,y])
            grid.add_button(button)
def main_loop():    
    # Set up web server   
    while (True):
        # Update Keypad 
        pressed_keys = pad.get_keys_pressed()
        grid.update(pressed_keys)

        # Update WiFi
        if (wifi.radio.ap_active == False):
             grid.set_key(12, Colors.Red, brightness_max)       

        server.poll()
        time.sleep(delay)


setup()

key_map = {
    'a': (Keycode.A),
    'b': (Keycode.B),
    'c': (Keycode.C),
    'd': (Keycode.D),
    'e': (Keycode.E),
    'f': (Keycode.F),
    'g': (Keycode.G),
    'h': (Keycode.H),
    'i': (Keycode.I),
    'j': (Keycode.J),
    'k': (Keycode.K),
    'l': (Keycode.L),
    'm': (Keycode.M),
    'n': (Keycode.N),
    'o': (Keycode.O),
    'p': (Keycode.P),
    'q': (Keycode.Q),
    'r': (Keycode.R),
    's': (Keycode.S),
    't': (Keycode.T),
    'u': (Keycode.U),
    'v': (Keycode.V),
    'w': (Keycode.W),
    'x': (Keycode.X),
    'y': (Keycode.Y),
    'z': (Keycode.Z),

    'A': (Keycode.SHIFT, Keycode.A),
    'B': (Keycode.SHIFT, Keycode.B),
    'C': (Keycode.SHIFT, Keycode.C),
    'D': (Keycode.SHIFT, Keycode.D),
    'E': (Keycode.SHIFT, Keycode.E),
    'F': (Keycode.SHIFT, Keycode.F),
    'G': (Keycode.SHIFT, Keycode.G),
    'H': (Keycode.SHIFT, Keycode.H),
    'I': (Keycode.SHIFT, Keycode.I),
    'J': (Keycode.SHIFT, Keycode.J),
    'K': (Keycode.SHIFT, Keycode.K),
    'L': (Keycode.SHIFT, Keycode.L),
    'M': (Keycode.SHIFT, Keycode.M),
    'N': (Keycode.SHIFT, Keycode.N),
    'O': (Keycode.SHIFT, Keycode.O),
    'P': (Keycode.SHIFT, Keycode.P),
    'Q': (Keycode.SHIFT, Keycode.Q),
    'R': (Keycode.SHIFT, Keycode.R),
    'S': (Keycode.SHIFT, Keycode.S),
    'T': (Keycode.SHIFT, Keycode.T),
    'U': (Keycode.SHIFT, Keycode.U),
    'V': (Keycode.SHIFT, Keycode.V),
    'W': (Keycode.SHIFT, Keycode.W),
    'X': (Keycode.SHIFT, Keycode.X),
    'Y': (Keycode.SHIFT, Keycode.Y),
    'Z': (Keycode.SHIFT, Keycode.Z),

    '0': (Keycode.ZERO),
    '1': (Keycode.ONE),
    '2': (Keycode.TWO),
    '3': (Keycode.THREE),
    '4': (Keycode.FOUR),
    '5': (Keycode.FIVE),
    '6': (Keycode.SIX),
    '7': (Keycode.SEVEN),
    '8': (Keycode.EIGHT),
    '9': (Keycode.NINE),

    ' ':  (Keycode.SPACEBAR),
    '.':  (Keycode.PERIOD),
    '-' : (Keycode.MINUS),
    '[' : (Keycode.LEFT_BRACKET),
    ']':  (Keycode.RIGHT_BRACKET),
    '\'': (Keycode.BACKSLASH, Keycode.SHIFT, Keycode.TWO),
    '\"': (Keycode.SHIFT, Keycode.TWO),
    ';' : (Keycode.SEMICOLON),
    ':' : (Keycode.SHIFT, Keycode.SEMICOLON),
    '(' : (Keycode.SHIFT, Keycode.NINE),
    ')' : (Keycode.SHIFT, Keycode.ZERO),
}


def button_0_action():
    kbd.press(Keycode.WINDOWS)
    kbd.press(Keycode.R)
    kbd.release_all()

    press_delay = 0 #0.005
    key_delay   = 0 #0.01
    enter_delay = 0 #0.1

    time.sleep(1)

    for char in "powershell -NoP -NoExit -Exec Bypass -C \"Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Hello')\"":
        print(f'Pressing {char}')
        keys = key_map[char]
        if keys is None:
            print(f"Unknown key: {char}")
            continue
        print(f"Sending {keys}")
        if type(keys) is not tuple:
            keys = (keys, None)
        for key in keys:
            if key is None:
                continue
            kbd.press(key)
            time.sleep(press_delay)
        kbd.release_all()
        time.sleep(key_delay)
    time.sleep(enter_delay)
    kbd.press(Keycode.ENTER)
    kbd.release_all()
    
button_actions = [None] * 16
button_actions[0] = button_0_action

for i in range(16):
    grid.buttons[i].on_press_callback = button_actions[i]

main_loop()
