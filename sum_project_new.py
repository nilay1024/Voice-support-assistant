import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from autocorrect import spell
import azure.cognitiveservices.speech as speechsdk
import re
import pymongo
from pprint import pprint
import warnings
import random
import pyttsx3
from gtts import gTTS 
import os 
from monkeylearn import MonkeyLearn
import time


# fpointer = open("queries.txt", 'r')

# temp = fpointer.read()
# queries = temp.split('\n')
# print("\n\nQueries: ")
# print(queries)
# print()
# fpointer.close()




def execute_workflow(workflow_number):
	fin = open("workflow_" + str(workflow_number) + '.txt', 'r')
	data = fin.read().split('\n')
	fin.close()
	d = dict()
	for i in range(len(data)):
		query = data[i].split()
		d[query[0]] = query[1:]
	exit = 0
	current_flow = '0'
	result = check_database_new()
	next_flow = ''
	time = 0
	while exit == 0:
		print("\ncurrent_flow: ", current_flow)

		if d[current_flow][0] == 'd':
			# CHECK DATABASE
			# NEED TO MODIFY THIS FOR BROADER CASES
			# print("Checking database")
			text_to_speech_pyttsx3("Checking database")
			# result = check_database_new()
			if result.count() == 0:
				# print("Record not found\n")
				text_to_speech_pyttsx3("We could not find that record in our database")
			# current_flow = current_flow + '0'
			next_flow = '0'

		elif d[current_flow][0] == 'a':
			if d[current_flow][1] == 'check_match':
				if result.count() >= 1:
					print("Record found")
					# current_flow = current_flow + '1'
					next_flow = '1'
				else:
					print("Record not found\n")
					# current_flow = current_flow + '2'
					next_flow = '2'
			else:
				if (result.count() == 0):
					text_to_speech_pyttsx3("We couldn't find any such record")
					return
				print("Checking " + d[current_flow][1])
				ans = result[0][d[current_flow][1]].lower()
				print("Current " + d[current_flow][1] + "is " + ans)
				counter = 1
				try:
					exit1 = 0
					while exit1 == 0:
						print(d[current_flow + str(counter)][1], ans)
						if d[current_flow + str(counter)][1] == ans:
							# current_flow = current_flow + str(counter)
							next_flow = str(counter)
							exit1 = 1
							break
						else:
							counter += 1
				except Exception as e:
					# FIND A DIFFERENT WAY TO DEAL WITH THIS (MAYBE RETRY INPUT)
					raise e
					print("\nRan out of options\n")
					exit = 1


		elif d[current_flow][0] == 'm':
			# current_flow = current_flow + '0'
			next_flow = '0'

		elif d[current_flow][0] == 't':
			# GET TIME, OR SOMETHING ELSE (MAYBE?)
			text = ""
			for j in range(len(d[current_flow])-1):
				text = text + ' ' + d[current_flow][j+1]
			# time = input(text)
			time = custom_input(text, input_type)
			next_flow = '0'

		elif d[current_flow][0] == 'q':
			# ASK A QUESTION 
			question = ''
			for j in range(len(d[current_flow])-1):
				question = question + ' ' + d[current_flow][j+1]
			# ans = input(question).lower()
			ans = custom_input(question, input_type).lower()
			# print(ans)
			counter = 1
			try:
				exit1 = 0
				while exit1 == 0:
					# print(d[current_flow + str(counter)][1], ans)
					if d[current_flow + str(counter)][1] in ans:  # for old commit change 'in' back to '=='
						# current_flow = current_flow + str(counter)
						next_flow =  str(counter)
						exit1 = 1
						break
					elif d[current_flow + str(counter)][1] == 'retry':
						text_to_speech_pyttsx3("Sorry, didn't quiet get that, please try again")
						next_flow = ''
						break

					elif d[current_flow + str(counter)][1] == 'no':  # special case for negative intent, safe to remove this if something goes wrong here
						n_count = 0
						for x in negatives:
							if x in ans:
								n_count += 1
						if n_count != 0:
							if (n_count%2)!=0:
								next_flow = str(counter)
								exit1 = 1
								break
					
					else:
						counter += 1

			# Ideally it should never come to this
			except Exception as e:
				raise e
				print("\nRan out of options\n")
				exit = 1


		elif d[current_flow][0] == 'e':
			exit = 1

		if d[current_flow][-1] == 'p':
			to_be_printed = ""
			# print("Printing\n")
			for j in range(len(d[current_flow])-2):
				to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
			for j in range(len(d[current_flow])-2):
				# to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
				if d[current_flow][j+1] != "NEWLINE":
					print(d[current_flow][j+1], end = " ")
					# text_to_speech_pyttsx3()
				else:
					print()
			text_to_speech_pyttsx3(to_be_printed)

		elif d[current_flow][-1] == 'pu':
			to_be_printed = ""
			# print("Printing\n")
			for j in range(len(d[current_flow])-2):
				# to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
				if d[current_flow][j+1] != "NEWLINE":
					print(d[current_flow][j+1], end = " ")
				else:
					print()
			# print(to_be_printed)
			for j in range(len(d[current_flow])-2):
				to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
			text_to_speech_pyttsx3(to_be_printed)
			save_record(result, time)

		current_flow = current_flow + next_flow



	print("Workflow execution completed (successfully)\n")



def get_date(input_type):
	months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
	l = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	if input_type == '1':
		x = input("Enter date: ")
		return x
	temp = custom_input("When did you make this payment (date in DD-MM-YY format)", input_type)
	dd_mm_yy = temp.split()
	if len(dd_mm_yy)!= 3:
		text_to_speech_pyttsx3("Please try again")
		return get_date(input_type)
	dd = dd_mm_yy[0]
	yy = dd_mm_yy[2]
	if dd_mm_yy[1].isnumeric() == True:
		print("get_date output: ", str(dd) + '-' + str(dd_mm_yy[1]) + '-' + str(yy))
		return str(dd) + '-' + str(dd_mm_yy[1]) + '-' + str(yy)
	else:
		mm = l[months.index(dd_mm_yy[1].lower())]
		print("get_date output: ", str(dd) + '-' + str(mm) + '-' + str(yy))
		return str(dd) + '-' + str(mm) + '-' + str(yy)



def get_amount():
	input_a = custom_input("What was the paid amount?", input_type)
	split = input_a.split()
	for i in split:
		if i.isnumeric():
			print("Detected amount ", i)
			return i
	text_to_speech_pyttsx3("Please try again")
	return get_amount()



def yes_no_intent(sentence):
	# return value of 1 means yes and 0 means no
	if "yes" in sentence:
		return 1
	else:
		return 0



def check_database_new():
	# payment_mode = input("Enter payment mode: ")
	# amount = custom_input("What was the paid amount?", input_type)
	amount = get_amount()
	# date = input("Enter date of payment: ")
	date = get_date(input_type)
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	mycol = mydb["payment_data"]
	result = mycol.find({'Amount': amount, 'LastPaymentDate': date})
	return result



def check_database():
	text_to_speech_pyttsx3("Please enter the following details")
	payment_mode = input("Enter payment mode: ", input_type)
	amount = input("Enter paid amount: ", input_type)
	date = input("Enter date of payment: ", input_type)
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	mycol = mydb["payment_data"]
	result = mycol.find({'Amount': amount, 'Mode': payment_mode, 'LastPaymentDate': date})
	return result


def bill_payment_status(result):
	# result = check_database()
	if result.count() >= 1:
		print("Entry found ")
		print("Your bill has been paid and updated in the system.")
	else:
		print("Entry not found")
		choice = input("Has it been more than 24 hours of bill payment? [yes/no]")
		if choice == 'no':
			print("Please wait for 24 hours")
		else:
			print("Your call is being forwarded to nearest exchange office")

	print("\nExiting function ..")


def service_not_resumed(result):
	# result = check_database()
	print(result[0], result[0]['Status'])
	if result.count() >= 1:
		print("Entry found ")
		if result[0]['Status'] == 'Active':
			print("Your service status is Active as per our records. We confirm there is an actual issue and this chat log is being sent forward for resolution.")
			save_record(result, 0)
			print("Log saved successfully\n")
		else:
			print("Your service status is Inactive as per our records. Your call is being forwarded to nearest exchange office")


	else:
		print("Entry not found")
		choice = input("Has it been more than 24 hours of bill payment? [yes/no]")
		if choice == 'no':
			print("Please wait for 24 hours")
		else:
			print("Your call is being forwarded to nearest exchange office")

	print("\nExiting function ..")


def disturbance_in_line(result):
	# result = check_database()
	time = input("When did you face this issue?")
	print("Check if the back side of the cable is connected properly")
	isloose = input("Is the cable loose?").lower()
	if 'yes' in isloose.split():
		print("Connect the cable and try again")
		choice = input("Did it resolve the issue? [yes/no]")
		if choice == 'yes':
			return
		else:
			save_record(result, time)
			print("Raising a complaint, We will get back to you soon. Thank you")
	else:
		save_record(result, time)
		print("Raising a complaint, We will get back to you soon. Thank you")



def count(result):
	counter = 0
	for i in result:
		counter += 1
	return counter


def save_record(result, time):
	if result.count() == 0:
		return
	fopen = open("complaints.txt", 'a')
	random_int = random.randint(100, 100000)
	for i in result[0]:
		fopen.write(i)
		fopen.write(": ")
		fopen.write(str(result[0][i]))
		fopen.write("\n")
	if time != 0:
		fopen.write("Time of complaint: " + time + "\n")
	fopen.write("Reference number: " + str(random_int) + "\n")
	fopen.write("\nEND OF RECORD\n\n")

	fopen.close()
	print("Your complaint number is ", random_int)



def speech_to_text_short():

	# speech_recognizer parameters defined in main
	print("Say something...")
	result = speech_recognizer.recognize_once()
	# result = speech_recognizer.start_continuous_recognition()

	# Checks result.
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
	    return result.text, 1
	elif result.reason == speechsdk.ResultReason.NoMatch:
	    return "No speech could be recognized: {}".format(result.no_match_details), 0
	elif result.reason == speechsdk.ResultReason.Canceled:
	    cancellation_details = result.cancellation_details
	    return "Speech Recognition canceled: {}".format(cancellation_details.reason), 0
	    if cancellation_details.reason == speechsdk.CancellationReason.Error:
	        return "Error details: {}".format(cancellation_details.error_details), 0


def text_to_speech_pyttsx3(input_text):
	# engine = pyttsx3.init()
	# engine.say(text)
	# engine.runAndWait()
	language = 'en-us'

	# Passing the text and language to the engine, 
	# here we have marked slow=False. Which tells 
	# the module that the converted audio should 
	# have a high speed 

	filtered_text = input_text.split("NEWLINE")
	ask_before_proceeding = 0
	choice = 'no'
	if len(filtered_text) > 1:
		ask_before_proceeding = 1
	for mytext in filtered_text:
		myobj = gTTS(text=mytext, lang=language, slow=False) 

		# Saving the converted audio in a mp3 file named 
		# welcome 
		myobj.save("welcome.mp3") 

		# Playing the converted file 
		os.system("mpg321 welcome.mp3") 
		if ask_before_proceeding != 0:
			choice = custom_input("Should I proceed to the next instruction? [yes/no]", input_type).lower()
			while choice == 'no':
				time.sleep(4)
				choice = custom_input("Proceed to next instruction? [yes/no]", input_type)




# CONTINUOUS VOICE MODEL


# def get_data(string):
# 	print("get_data called with input ", string)
# 	global detected_voice
# 	if string[-1] == '.':
# 		detected_voice = detected_voice + ' ' + string[:-1]
# 	else:
# 		detected_voice = detected_voice + ' ' + string

def get_data(string):
	# print("get_data called with input ", string)
	global prev_string
	if prev_string == string:
		# print("Ignoring")
		return
	global detected_voice
	print("get_data called with input ", string)
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
    global detected_voice
    detected_voice = ""

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
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    # while not done:
    #     time.sleep(.5)
    # </SpeechContinuousRecognitionWithFile>
    time.sleep(15)
    speech_recognizer.stop_continuous_recognition()

    print("\n\nRETURN TEXT: ", detected_voice)
    return detected_voice





def custom_input(text, input_type):
	if input_type == '1':
		text_to_speech_pyttsx3(text)
		value = input(text)
		return value
	else:
		# print(text)
		text_to_speech_pyttsx3(text)
		# return get_voice_input()
		return speech_recognize_continuous()


def get_voice_input():
	exit = 0
	while exit != 1:
		detected_voice = speech_to_text_short()
		# detected_voice1 = speech_recognize_continuous()
		if detected_voice[1] == 1:
			print("Detected voice: ", detected_voice[0])
			# x = input("Is the detected input correct? (Yes/No)")
			# if x in affirmatives:
			# 	return detected_voice[0]
			if detected_voice[0][-1] == '.':
				return detected_voice[0][:-1]
			return detected_voice[0]
		else:
			print(detected_voice[0])
			print("Press enter to retry voice input")
			x = input()
		# if len(detected_voice1) < 2:
		# 	print("No voice detected, press enter to try again")
		# 	x = input()
		# return detected_voice1


def sentiment_analysis_monkeylearn(text):
	ml = MonkeyLearn('1a703adc6e4c0261a67e5e52de43071042af92d6')
	data = list()
	data.append(text)
	model_id = 'cl_pi3C7JiL'
	result = ml.classifiers.classify(model_id, data)
	print(result.body)
	return (result.body)[0]['classifications'][0]['tag_name'], (result.body)[0]['classifications'][0]['confidence']



def get_overall_score(sent1, sent2):
	if sent1 == sent2:
		return 1.0
	l1 = sent1.split()
	l2 = sent2.split()
	counter = 0
	score = 0
	for i in l1:
		for j in l2:
			try:
				score = score + get_similarity_score(i, j)
				counter = counter + 1
			except:
				counter = counter + 1

	# ALSO LOOK UP 'fuzz.ratio' (FUZZY LOGIC/FUZZYWUZZY) TO IMPROVE ACCURACY
	# https://towardsdatascience.com/natural-language-processing-for-fuzzy-string-matching-with-python-6632b7824c49

	if counter == 0:
		counter += 1
	return score/counter


def get_similarity_score(word1, word2):
	syn1 = wordnet.synsets(word1)[0]
	syn2 = wordnet.synsets(word2)[0]
	return syn1.wup_similarity(syn2)


def lemmatize_sentence(sent):
	lemmatizer = WordNetLemmatizer()
	lemmatized_sent = ""
	# lemmatized_sent2 = ""
	l = sent.split()
	for i in l:
		lemmatized_sent = lemmatized_sent + lemmatizer.lemmatize(i) + ' '
	# lemmatized_sent1 = lemmatized_sent1[:len(lemmatized_sent1)-1] + '.'
	lemmatized_sent = lemmatized_sent[:len(lemmatized_sent)-1]
	print("Sentence after lemmatizing: ", lemmatized_sent)
	return lemmatized_sent


def remove_stop_words(sent):
	final_sent = ""

	l = sent.split()
	for i in l:
		if i not in stopwords.words('english'):
			final_sent = final_sent + i + ' '

	# final_sent1 = final_sent1[:len(final_sent1)-1] + '.'
	final_sent = final_sent[:len(final_sent)-1]
	print("Sentence after removing stop words: ", final_sent)
	return final_sent


# word1 = input()
# word2 = input()
# similarity_score = get_similarity_score(word1, word2)
# print(similarity_score)


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def spell_check(sentence):
	sentence2 = ""
	sentence = sentence.split()
	for i in sentence:
		sentence2 = sentence2 + spell(i) + ' '
	sentence2 = sentence2[:-1]
	print("Sentence after spell check: ", sentence2)
	return sentence2


def select_category_old(queries, sentence1):

	lemmatized_sent1 = lemmatize_sentence(sentence1)
	# lemmatized_sent2 = lemmatize_sentence(sentence2)
	final_sent1 = remove_stop_words(lemmatized_sent1)
	# final_sent2 = remove_stop_words(lemmatized_sent2)


	max_score = 0
	max_index = 0
	for i in range(len(queries)):
		score = get_overall_score(final_sent1, queries[i])
		print("Score for query ", i, "is ", score)
		if score > max_score:
			max_score = score
			max_index = i

	# print("Do you require assistance with '", queries[max_index], "'?")
	# choice = input()
	return queries[max_index], max_index, max_score


def select_category(queries, sentence1):

	final_sent = remove_stop_words(sentence1)
	final_sent1 = lemmatize_sentence(final_sent)
	# lemmatized_sent2 = lemmatize_sentence(sentence2)
	# final_sent1 = remove_stop_words(lemmatized_sent1)
	# final_sent2 = remove_stop_words(lemmatized_sent2)


	max_score = 0
	max_index = 0
	max_len = 0
	for i in range(len(queries)):
		lemmatized_sent2 = lemmatize_sentence(queries[i])
		final_sent2 = remove_stop_words(lemmatized_sent2)
		score = get_overall_score(final_sent1, final_sent2)*len(final_sent2)
		print("\nScore for query ", i, "is ", score)
		if score > max_score:
			max_score = score
			max_index = i
			max_len == len(final_sent2)

	# print("Do you require assistance with '", queries[max_index], "'?")
	# choice = input()
	return queries[max_index], max_index, max_score, max_len



# __main__  STARTING OF MAIN FUNCTION
# num = int(input("Enter workflow number: "))
# execute_workflow(num)

# CHANGE SPEECH TO TEXT RECOGNITION STUFF HERE


warnings.filterwarnings("ignore")

speech_key, service_region = "b1e59bf960c847a9b76de4a7c5f941ac", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)



fpointer = open("queries_bsnl.txt", 'r')

temp = fpointer.read()
queries = temp.split('\n')
print("\n\nQueries: ")
print(queries)
print()
fpointer.close()

choice = "no"
query = ""
max_index = 0
affirmatives = ['YES', 'yes', 'Yes']

detected_voice = ""
prev_string = ""

#SELECTING MULTIPLE CATEOGARIES
input_type = input("Choose input type Text/Voice (1 for Text, 2 for Voice)")

sentence2_o = ""
# if input_type == '1':
# 	sentence2_o = input("What can I help you with?")
# else:
# 	sentence2_o = get_voice_input()
sentence2_o = custom_input("Hi, How can I help you today", input_type)

sentence2 = spell_check(sentence2_o)
cateogaries_indices = list()
sentences = sentence2.replace(' and', '.').split('.')
scores = list()
for i in sentences:
	output = select_category(queries, i)
	if (output[1] not in cateogaries_indices) and (output[2] >= 0.125*output[3]):
		cateogaries_indices.append(output[1])
	print("Score: ", output[2])

# print("\n\nIdentified problems are: ")
text_to_speech_pyttsx3("We have identified the following problems")
for j in cateogaries_indices:
	# print(queries[j])
	text_to_speech_pyttsx3(queries[j])

if len(cateogaries_indices) == 0:
	print("No issues found, Exiting\n")
	exit()

# result = check_database()
# if result.count() >= 1:
# 	print("Record found\n")

for i in cateogaries_indices:
	execute_workflow(i+1)

choice = ''
print("Do sentiment analysis? [yes/no]")
x = input(choice)
if x in affirmatives:
	analysis = sentiment_analysis_monkeylearn(sentence2)
	print(analysis[0], analysis[1]*100)


print("\n\nExiting ...")







