# Libraries
from config import *
from vosk import Model, KaldiRecognizer
import pyaudio
import subprocess
import requests
import re
from bs4 import BeautifulSoup
import tinytuya as tt
from tinytuya import Contrib
from time import sleep

# Main class
class Assistant:
    def __init__(self):

        # Vosk model setup
        self.model_it = Model(model_it_path)
        self.recognizer_it = KaldiRecognizer(self.model_it, 16000)

        # Audio setup
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

        # Bulb setup
        self.bulb = tt.BulbDevice(lights_id, lights_ip, lights_key)
        self.bulb.set_version(3.3)

        # IR controller setup
        self.ir = Contrib.IRRemoteControlDevice(ir_id, ir_ip, ir_key)
        self.ir.set_version(3.3)

    def speak(self, text):
        subprocess.Popen(f'espeak-ng -v roa/it "{text}"', shell=True)

    def listen(self):
        while True:
            data = self.stream.read(4096)

            if self.recognizer_it.AcceptWaveform(data):
                text = self.recognizer_it.Result()[14:-3]
                break

        return text

    def weather(self, city):
        city = city.replace(" ", "+")
        url = f"https://www.3bmeteo.com/meteo/{city}"

        try:
            page = requests.get(url)

            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                result = soup.find("div", {"class": "section-title pad-box"}).findChildren("p")[0].get_text(strip=False).rstrip("\n")
                result = result.replace("°C", " gradi centigradi")
                result = re.sub(r"(\d{4})m", "\g<1> metri", result)
                return result
            else:
                raise Exception(f"Page loading failed ({page.status_code})")
        except Exception as e:
            print(f"Error while loading or parsing the page: {str(e)}")
            return None

    def alarm(self):
        subprocess.Popen(f"bash {alarm_script_path} {alarm_hours} {alarm_minutes} {alarm_seconds} {alarm_sound} {name} {alarm_wait} {alarm_lights_script_path}", shell=True)
        self.speak(alarm_confirmation_msg)

    def lights(self, command):
        if "bianca" in command or "bianche" in command:
            self.bulb.turn_on()
            self.bulb.set_white_percentage(70, 100)

        elif "gialla" in command or "gialle" in command:
            self.bulb.turn_on()
            self.bulb.set_white_percentage(70, 0)

        elif "viola" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(40, 0, 255)
            self.bulb.set_brightness_percentage(70)

        elif "rosa" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(255, 30, 255)
            self.bulb.set_brightness_percentage(70)

        elif "rossa" in command or "rosse" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(255, 0, 0)
            self.bulb.set_brightness_percentage(70)

        elif "blu" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(0, 0, 255)
            self.bulb.set_brightness_percentage(70)

        elif "verde" in command or "verdi" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(30, 255, 30)
            self.bulb.set_brightness_percentage(70)

        elif "notte" in command:
            self.bulb.turn_on()
            self.bulb.set_colour(0, 0, 255)
            self.bulb.set_brightness_percentage(20)
            self.bulb.set_timer(180)

        elif "spegni" in command:
            self.bulb.turn_off()

        elif "alza" in command:
            self.bulb.set_brightness_percentage(100)

        elif "abbassa" in command:
            self.bulb.set_brightness_percentage(20)

        elif "timer" in command:
            self.bulb.set_timer(300)

        else:
            self.speak(didnt_understand)

    def ir_control(self, command):
        if "accendi" in command:
            self.ir.send_button(on_button)
            sleep(7)
            self.ir.send_button(display_off_button)

        elif "spegni" in command:
            self.ir.send_button(off_button)

        elif "timer" in command and "breve" in command:
            self.ir.send_button(timer_1h_on)
            sleep(2)
            self.ir.send_button(display_off_button)

        elif "timer" in command and "lungo" in command:
            self.ir.send_button(timer_2h_on)
            sleep(2)
            self.ir.send_button(display_off_button)

        else:
            self.speak(didnt_understand)

    def tgpt(self, query):
        subprocess.Popen(f'bash {tgpt_script} "{query}"', shell=True)

    def main(self):
        self.speak(greeting)

        while True:
            cmd = self.listen()

            if weather_keyword in cmd:
                result = self.weather(city)

                if result is not None:
                    self.speak(result)

                else:
                    self.speak(page_loading_error)

                break

            elif alarm_keyword in cmd:
                self.alarm()
                break

            elif lights_keyword in cmd:
                self.lights(cmd)
                break

            elif ir_keyword in cmd:
                self.ir_control(cmd)
                break

            elif exit_word in cmd:
                self.speak(confirm_msg)
                break

            else:
                self.tgpt(cmd)
                break

    def run(self):

        while True:
            wake = self.listen()

            if wake == activation_word:
                self.main()

            elif wake == silent_activation_word:
                self.lights("notte")

            elif wake == exit_word:
                self.speak(confirm_msg)
                break

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()
