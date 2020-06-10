from queue import __Queue
from pepper_handler import *
import qi
import json
import datetime
#----------------------------------------------------------------------------------------------------------------------#
global Q
global NAO_IP
NAO_IP = '192.168.1.104'
global NAO_PORT
NAO_PORT = '9559'

PASSWORD = "admin"


Q = __Queue()
#---------------------------------------------------PRIVATE METHODS----------------------------------------------------#
def enqueue_speech(text, volume, speech_speed, language):
    speech_object = Speech(text, volume, speech_speed, language)
    Q.add_to_queue(speech_object)

def enqueue_moving(distance):
    print("moving  enqueued")
    movement_object = Movement(distance)
    Q.add_to_queue(movement_object)

def enqueue_turning(angle):
    turn_object = Turn(angle)
    Q.add_to_queue(turn_object)

def enqueue_sequence_execution(name):
    sequence_object = Sequence(name)
    Q.add_to_queue(sequence_object)

def enqueue_media_display(photo_or_movie_name, file_type):
    media_display_object = MediaDisplay(photo_or_movie_name, file_type)
    Q.add_to_queue(media_display_object)

#Classes Speech, Movement, Turn, Sequence, MediaDisplay all inherit from virtual Action class and all have method process_action()
#where Pepper API is called

#---------------------------------------------------PUBLIC METHODS-----------------------------------------------------#
def initialize_queue():
    Q.queue_listener()
#----------------------------------------------------------------------------------------------------------------------#
def handle_connect_request(json_request):
    print("handling connect request")       ####DEPRECIATED
    if(json_request['password']==PASSWORD):
        return "Successfully connected to the robot", 200
    else:
        return ("Invalid password dziwko"), 400

#----------------------------------------------------------------------------------------------------------------------#
def handle_logger_request():
    print("handle_logger_request")
    session1 = qi.Session()
    session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    battery_service1 = session1.service("ALBattery")
    camera_service1 = session1.service("ALVideoRecorder")

    try:
        json_logger = {'is_queue_empty': str(Q.is_empty()), 'battery': str(battery_service1.getBatteryCharge()) + "%",
                    'is_recording': str(camera_service1.isRecording())}
        response = json.dumps(json_logger)
    except:
        return ("Couldnt get logs"), 400

    return response, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_scenarios_list_request():
    print("handle_scenarios_list_request")
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'scenarios.json')
    data = json.load(open(json_url))
    print(data)
    return data, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_creating_new_scenario_request(json_request):
    print("handle_creating_new_scenario_request")
    name = json_request['name']
    description = json_request['description']
    actions = json_request['actions']

    print name
    print description
    print actions

    config = json.loads(open('static/scenarios.json').read())
    print(config)
    config['scenarios'].append(json_request)
    with open('static/scenarios.json', 'w') as f:
        f.write(json.dumps(config))
    return "Success", 200

#----------------------------------------------------------------------------------------------------------------------#
def handle_deleting_scenario_request(scenario_name):
    print("handle_deleting_scenario_request")
    #todo
    return "Success", 200
#----------------------------------------------------------------------------------------------------------------------#

def handle_scenario_run_request(name, run, start, end):
    print("handle_scenario_run_request")
    scenarios = json.loads(open('static/scenarios.json').read())

    for scenario in scenarios['scenarios']:
        if( scenario['name'] == name ):
            counter = 0
            print(scenario['actions'])
            for action in scenario['actions']:
                print(action)
                counter += 1
                print(counter)
                print(start)
                print(end)
                print(run)
                if(counter >= int(start) and counter <= int(end) and run == 'true'): handle_add_action_request(action)
            return scenario

    return scenario, 200

#----------------------------------------------------------------------------------------------------------------------#
def handle_modify_scenario_request(scenario_name):
    print("handle_modify_scenario_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_sequences_list_request():
    print("handle_sequences_list_request")
    session1 = qi.Session()
    session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    behaviors_service1 = session1.service("ALBehaviorManager")
    names = behaviors_service1.getInstalledBehaviors()
    print "Behaviors on the robot:"
    #print(names)

    names_converted = []
    for name in names:
        print name
        names_converted.append({'name': name})

    print names_converted

    response = { "sequences": names_converted } # { "sequences:" names_converted }

    return response, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_media_list_request():
    print("handle_media_list_request")
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'images.json')
    json_url2 = os.path.join(SITE_ROOT, 'static', 'videos.json')
    photos = json.load(open(json_url))
    videos = json.load(open(json_url2))

    photos_converted = []
    videos_converted = []

    for photo in photos:
        print photo
        photos_converted.append({'name': photo})

    for video in videos:
        print video
        videos_converted.append({'name': video})

    merged = {
        "photos": photos_converted, "videos": videos_converted
    }
    return merged, 200

#----------------------------------------------------------------------------------------------------------------------#
def handle_recording_toggle_request(request):
    print("handle_recording_toggle_request")
    if "status" not in request.args:
        return '"status" not provided in request', 400

    print(request.args.get("status"))
    record = request.args.get("status")

    session1 = qi.Session()
    session1.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    camera_service1 = session1.service("ALVideoRecorder")
    camera_service1.stopRecording()

    if(record=="False"):                
        camera_service1.stopRecording()
    else:
        timestamp = datetime.datetime.now().isoformat()
        camera_service1.startRecording("/home/nao/video", timestamp)
        camera_service1.stopRecording()

    return "Success", 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_recordings_list_request():
    print("handle_recordings_list_request")
    #todo
    json_logger = {"recordings": [{"name": "VID001", "file_type": "MP4", "duration": "13"},
                   {"name": "VID002", "file_type": "MP4", "duration": "213"}]}

    return json_logger, 200
#----------------------------------------------------------------------------------------------------------------------#
def handle_play_recording_request(name):
    print("handle_play_recording_request")
    #todo
#----------------------------------------------------------------------------------------------------------------------#
def handle_get_settings_request():
    print("handle_get_settings_request")
    #leave unimplemented
#----------------------------------------------------------------------------------------------------------------------#
def handle_set_settings_request(json_request):
    print("handle_set_settings_request")
    #leave unimplemented
#----------------------------------------------------------------------------------------------------------------------#
def handle_clear_queue_request():
    print("handle_clear_queue_request")
    try:
        Q.clear_queue()
    except:
        return 'Failed', 400
    return 'Success',  200
#----------------------------------------------------------------------------------------------------------------------#
def handle_add_action_request(json_request):
    print("handle_add_action_request")
    print(json_request)
    if "type" in json_request:
        if json_request["type"] == "speech":
            text = json_request["text"]
            volume = json_request["volume"]
            speech_speed = json_request["speech_speed"]
            language = json_request["language"]
            enqueue_speech(text, volume, speech_speed, language)

        elif json_request["type"] == "movement":
            command = json_request["command"]
            if command == "move_forward":
                distance = json_request["distance"]
                enqueue_moving(distance)
            elif command == "move_backward":
                print(float(json_request["distance"]))
                distance = float(json_request["distance"]) * (-1.0)
                enqueue_moving(distance)
            elif command == "turn_right":
                angle = float(json_request["angle"]) * (-1.0)
                enqueue_turning(angle)
            elif command == "turn_left":
                angle = json_request["angle"]
                enqueue_turning(angle)

        elif json_request["type"] == "sequence":
            name = json_request["name"]
            enqueue_sequence_execution(name)

        elif json_request["type"] == "media":
            photo_or_movie_name = json_request["name"]
            file_type = json_request["file_type"]
            enqueue_media_display(photo_or_movie_name, file_type)
        else:
            return "Wrong JSON format provided", 400

    return "Success", 200
#----------------------------------------------------------------------------------------------------------------------#

