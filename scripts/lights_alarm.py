# Libraries
import tinytuya as tt
from config import lights_id, lights_ip, lights_key

# Connect to bulb
bulb = tt.BulbDevice(lights_id, lights_ip, lights_key)
bulb.set_version(3.3)

# Turn on light
bulb.turn_on()
bulb.set_white_percentage(100, 0) # Set color to yellow
bulb.set_timer(900) # Set 15 minutes timer 
