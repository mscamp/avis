# Libraries
from flask import Flask, request
import tinytuya as tt
from tinytuya import Contrib
from time import sleep
from config import *

# Connect to bulb
bulb = tt.BulbDevice(lights_id, lights_ip, lights_key)
bulb.set_version(3.3)

# Connect to IR remote
ir = Contrib.IRRemoteControlDevice(ir_id, ir_ip, ir_key)
ir.set_version(3.3)

# Color mapping
colors = {
    "violet": (40, 0, 255),
    "pink": (255, 30, 255),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (30, 255, 30)
}

app = Flask(__name__)

@app.route("/lights", methods=["POST"])
def lights():
    command = request.form.get("command")
    time = int(request.form.get("time", 0))
    brightness = int(request.form.get("brightness", 0))

    if command in colors:
        bulb.turn_on()
        color = colors[command]
        bulb.set_colour(*color)
        return f"Set color to {command}"

    elif command == "white":
        bulb.turn_on()
        bulb.set_white_percentage(brightness, 100) 
        return f"Set color to {command}"

    elif command == "yellow":
        bulb.turn_on()
        bulb.set_white_percentage(brightness, 0) 
        return f"Set color to {command}"

    elif command == "night" and time != 0:
        bulb.turn_on()
        bulb.set_colour(0, 0, 255)
        bulb.set_brightness_percentage(brightness)
        bulb.set_timer(time * 60)
        return "Night light"

    elif command == "off":
        bulb.turn_off()
        return "Lights turned off"

    elif command == "brightness":
        bulb.set_brightness_percentage(brightness)
        return f"Brightness set to {brightness}%"

    elif command == "timer" and time != 0:
        bulb.set_timer(time * 60)
        return f"Timer set ({time} min)"

    else:
        return "Invalid command"

@app.route("/ir", methods=["POST"])
def ir_control():
    command = request.form.get("command")

    if "accendi" in command:
        ir.send_button(on_button)
        sleep(7)
        ir.send_button(display_off_button)
        return "Turned on"

    elif "spegni" in command:
        ir.send_button(off_button)
        return "Turned off"

    elif "timer1h" in command:
        ir.send_button(timer_1h_on)
        sleep(2)
        ir.send_button(display_off_button)
        return "Timer set 1h"

    elif "timer2h" in command:
        ir.send_button(timer_2h_on)
        sleep(2)
        ir.send_button(display_off_button)
        return "Timer set 2h"

    else:
        return "Invalid command"

if __name__ == "__main__":
    app.run(debug=True, host=host_ip)
