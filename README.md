# AVIS (Assistente Vocale Intelligente di Scamp)

<p align="center">
	<img title="avis_logo" alt="avis_logo" width="200px" height="200px" src="avis.jpg" style="display: block; margin: 0 auto;" >
</p>

AVIS is a voice-controlled assistant written in Python and Bash that can control my room's lights and air conditioning and answer basic questions using a GPT model. It supports only Italian by default, but with some tweaking, it can support virtually any language. I decided to build AVIS for the following reasons:
1. To avoid using proprietary apps to control my smart home appliances.
2. To avoid buying proprietary and invasive spyware devices like Alexa or Google Nest.
3. To be able to control them from any device, not just my phone.
4. To configure it exactly as I want.

## Libraries Used
AVIS makes use of the following open-source libraries and software to function:
- [espeak-ng](https://github.com/espeak-ng/espeak-ng) for text-to-speech.
- [PyAudio](https://pypi.org/project/PyAudio) for recording audio.
- [Vosk](https://github.com/alphacep/vosk-api) for voice recognition.
- [Flask](https://pypi.org/project/Flask) to accept HTTP requests on the local network (to control my smart home devices from my phone using the app [HTTP Shortcuts](https://github.com/Waboodoo/HTTP-Shortcuts) or from my laptops using [curl](https://github.com/curl/curl)).
- [tinytuya](https://pypi.org/project/tinytuya) to control my smart home devices using the Tuya API.
- [requests](https://pypi.org/project/requests) and [beautifulsoup4](https://pypi.org/project/beautifulsoup4) for web scraping.
- [tgpt](https://github.com/aandrew-me/tgpt) to answer voice queries using a GPT model.
- [mpv](https://github.com/mpv-player/mpv) to play audio.

## Privacy
Voice recognition and audio recording are done **locally**. However, be aware that tgpt sends your queries to OpenGPT providers, and tinytuya sends API calls to Tuya servers, which are closed-source and proprietary, requiring you to create an account. You can choose not to use AVIS to control smart home appliances if you prefer.

## Features
- Answer generic questions.
- Provide current day's weather for a specified location.
- Control smart home devices using voice commands or HTTP requests (for now, just lights and AC).

## Hardware
AVIS is pretty lightweight and can even run on a single-board computer; in fact, I run AVIS on a Raspberry Pi 3 with Raspberry Pi OS. I use a microphone to record my voice and Trust speakers with a 3.5 mm jack for audio output.

## Installation
1. Clone the repository.
2. Run `setup.sh` and follow the instructions at the link provided at the bottom of the file if you run into issues with PyAudio. Please carefully check the script before running it.
3. Configure AVIS by editing `scripts/config.py`
