import os
import qi
import time
import sys
import json

sys.path.insert(1, '/res/img')

global session
global text_service
global posture_service
global motion_service
global tabletService
global NAO_IP
global NAO_PORT

NAO_IP = '192.168.1.104'
NAO_PORT = '9559'

def establish_connection():
    session = qi.Session()
    session.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    text_service = session.service("ALTextToSpeech")
    posture_service = session.service("ALRobotPosture")
    motion_service = session.service("ALMotion")
    tabletService = session.service("ALTabletService")
    print("Connection with robot established")

class Action:
    def process_action(self):
        print("No such action is supported")
#----------------------------------------------------------------------------------------------------------------------#
class Speech(Action):
    def __init__(self, text, volume, speech_speed, language):
        self.text = text
        self.volume = volume
        self.speech_speed = speech_speed
        self.language = language

    def process_action(self):
		# Pepper API calls go here
        print("saying: ")
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        tts = session1.service("ALTextToSpeech")
        tts.setVoice("naoenu")
        tts.setLanguage(self.language)
        tts.setVolume(self.volume)
        tts.setParameter("speed", self.speech_speed)
        tts.say(self.text)
        print("end")
        return "Success", 200

# ----------------------------------------------------------------------------------------------------------------------#
class Movement(Action):
    def __init__(self, distance):
        self.distance = distance

    def process_action(self):
        #Pepper API calls go here
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        print("Move forward process action")
        print(self.distance)
        posture_service1 = session1.service("ALRobotPosture")
        motion_service1 = session1.service("ALMotion")
        posture_service1.goToPosture("Stand", 0.5)
        rounds = float(0.5)
        turns = rounds * 0.5 * 3.14
        time = rounds * 2.0
        motion_service1.moveTo(float(self.distance), 0, 0, time)
        return "Success", 200
# ----------------------------------------------------------------------------------------------------------------------#
class Turn(Action):
    def __init__(self, angle):
        self.angle = angle

    def process_action(self):
        #Pepper API calls go here
        session1 = qi.Session()
        session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
        posture_service1 = session1.service("ALRobotPosture")
        motion_service1 = session1.service("ALMotion")
        print("moving left")
        posture_service1.goToPosture("Stand", 0.5)
        rounds = float(0.5)
        turns = rounds * 0.5 * 3.14
        time = rounds * 2.0
        motion_service1.moveTo(0.0, 0.0, float(self.angle), time)
        return "Success", 200
# ----------------------------------------------------------------------------------------------------------------------#
class Sequence(Action):
    def __init__(self, name):
        self.name = name

    def process_action(self):
		# Pepper API calls go here
		print("Process sequence")
		session1 = qi.Session()
		session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
		behaviors_service1 = session1.service("ALBehaviorManager")
		behaviors_service1.runBehavior(str(self.name), _async=True)
		return "Success", 200
# ----------------------------------------------------------------------------------------------------------------------#
class MediaDisplay(Action):
	def __init__(self, name, file_type):
		self.name = name
		self.file_type = file_type

	def process_action(self):
		# Pepper API calls go here
		print("Media Display")
		session1 = qi.Session()
		session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
		tabletService = session1.service("ALTabletService")

		if (str(self.file_type) == 'jpg'):
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, 'static', 'images.json')
			data = json.load(open(json_url))
			url = str(data[str(self.name)])
		else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, 'static', 'videos.json')
			data = json.load(open(json_url))
			url = str(data[str(self.name)])

		print(url)
		if (str(self.file_type) == 'jpg'):
			tabletService.showImage(str(url))
		else:
			tabletService.playVideo(str(url))
		return "Success", 200

# ----------------------------------------------------------------------------------------------------------------------#