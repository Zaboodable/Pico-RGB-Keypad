# Pico-RGB-Keypad
RGB Keypad using circuitpython and Raspberry Pi Pico W.
Set up with a web server for pressing the buttons wirelessly.

<h2>Requirements</h2>
Alternatives might work but some modifications might be required. The wireless variant of the pico is not required but the web server and wifi features will not work and should be removed.
<br>
This project has been built using the Pico W and the Pimoroni RGB keypad base. Using CircuitPython version 8.1.0.
<br><br>
It also makes use of the uk versions of the keypad layout and has its own key map for sending keystrokes over for now. 

<h3>Hardware</h3>
<ul>  
  <li>Raspberry Pi Pico W</li>
  <li><a href="https://shop.pimoroni.com/products/pico-rgb-keypad-base">Pico RGB Keypad Base (Pimoroni)</a></li> 
</ul>
<h3>Software</h3>
<ul>  
  <li><a href="https://circuitpython.org/board/raspberry_pi_pico_w/">CircuitPython for the Pico W</a></li>
  <li><a href="https://github.com/adafruit/Adafruit_CircuitPython_Bundle">Adafruit Libraries for CircuitPython</a></li> 
  <ul>    
    <li>adafruit_hid</li> 
    <li>adafruit_httpserver</li> 
  </ul>
  <li><a href="https://github.com/martinohanlon/pico-rgbkeypad">pico-rgbkeypad by martinohanlon</a></li>
</ul>
<br>

<h2>Instructions</h2>
<ol>  
  <li>Get the required hardware</li>
  <li>Connect headers up</li> 
  <li>Put CircuitPython onto the pico by dragging the .uf2 file over</li> 
  <li>Put libraries into the /lib folder</li> 
  <li>Put boot.py, main.py and web folder onto the root folder</li> 
</ol>

<h2>Info</h2>
By default, the pico w should set up a wifi network called "RGBWifi" with password "12345678"
<br><br>
Button 0 has a custom action which sends keystrokes through and displays a message box on screen. This will probably not work on non UK keyboard layouts.
