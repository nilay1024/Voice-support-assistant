import azure.cognitiveservices.speech as speechsdk
import time
import os
import sys


def get_data(string):
	print("get_data called with input ", string)
	global prev_string
	if prev_string == string:
		# print("Ignoring")
		return
	global detected_voice
	if string[-1] == '.':
		detected_voice = detected_voice + ' ' + string[:-1]
	else:
		detected_voice = detected_voice + ' ' + string
	prev_string = string


def speech_recognize_continuous():

    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    # speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING'))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: get_data(evt.result.text))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt.result)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    # while not done:
    #     time.sleep(.5)
    # </SpeechContinuousRecognitionWithFile>
    time.sleep(10)
    speech_recognizer.stop_continuous_recognition()



prev_string = ""
detected_voice = ""
speech_key, service_region = "b1e59bf960c847a9b76de4a7c5f941ac", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

speech_recognize_continuous()
print("\n\nDetected voice: ", detected_voice)
time.sleep(5)
print("attempt 2")
detected_voice = ""
speech_recognize_continuous()

print("\n\nDetected voice: ", detected_voice)
