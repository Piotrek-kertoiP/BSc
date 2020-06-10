# coding=utf-8
from flask import Flask, make_response
from flask import request
from concurrent.futures import ThreadPoolExecutor
from requests_handler import *
from pepper_handler import *
from flask_cors import CORS, cross_origin


#----------------------------------------------------------------------------------------------------------------------#
app = Flask(__name__)

SERVER_IP = "192.168.1.102"
SERVER_PORT = "5000"

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/connect": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/logger": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/scenarios": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/scenarios/remove": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/scenario": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/sequences": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/media": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/recordings": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/record": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/clear_queue": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            r"/add_action": {"origins": "http://" + SERVER_IP + ":" + SERVER_PORT},
                            })

executor = ThreadPoolExecutor(1)
#----------------------------------------------------------------------------------------------------------------------#
@app.route('/connect', methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def connect():
    print(request.json['IP'])
    result = handle_connect_request(request.json)
    return result

@app.route('/logger', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def logger():
    result = handle_logger_request()
    return result

@app.route('/scenarios', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_scenarios_list():
    result = handle_scenarios_list_request()
    return result

@app.route('/scenarios', methods=["POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def create_new_scenario():
    result = handle_creating_new_scenario_request(request.json)
    return result

@app.route('/scenarios/remove', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def delete_scenario():
    result = handle_deleting_scenario_request(request.args.get['name'])
    return result

@app.route('/scenario', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def scenarios_get_details_and_run():
	result = handle_scenario_run_request(request.args['name'], request.args['run'],
										 request.args['start'], request.args['end'])
	print(result)
	return result

@app.route('/scenarios', methods=["PUT"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def modify_scenario():
    result = handle_modify_scenario_request(request.args.get['name'], request.json)
    return result

@app.route('/sequences', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_sequences_list():
    result = handle_sequences_list_request()
    return result

@app.route('/media', methods=["GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_media_list():
    result = handle_media_list_request()
    return result

@app.route('/record', methods=["GET"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def start_stop_recording():
    result = handle_recording_toggle_request(request)
    return result

@app.route('/recordings', methods=["GET"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_recordings_list():
    result = handle_recordings_list_request()
    return result

@app.route('/recordings', methods=["GET"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def play_recording():
    result = handle_play_recording_request(request.args.get['name'])
    return result

@app.route('/settings', methods=["GET"])
def get_settings():
    result = handle_get_settings_request()  #ta metoda ma zostać niezaimplementowana, bo uznaliśmy, że nie ma ustawień robota, które chcielibyśmy uzyskiwać, ale perspektywicznie można to zostawić
    return result

@app.route('/settings', methods=["POST"])
def set_settings():
    result = handle_set_settings_request(request.json)  #ta metoda ma zostać niezaimplementowana, bo uznaliśmy, że nie ma ustawień robota, które chcielibyśmy uzyskiwać, ale perspektywicznie można to zostawić
    return result

@app.route('/clear_queue', methods=["GET"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def clear_queue():
    result = handle_clear_queue_request()
    return result

@app.route('/add_action', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_action():
    result = handle_add_action_request(request.json)
    return result
#----------------------------------------------------------------------------------------------------------------------#
@app.before_first_request
def initialize():
    executor.submit(establish_connection)
    executor.submit(initialize_queue)
#----------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(threaded=True, processes=2, host=SERVER_IP, port=SERVER_PORT)
