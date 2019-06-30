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
			print("Checking database")
			# result = check_database_new()
			if result.count() == 0:
				print("Record not found\n")
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
			time = input(text)
			next_flow = '0'

		elif d[current_flow][0] == 'q':
			# ASK A QUESTION 
			question = ''
			for j in range(len(d[current_flow])-1):
				question = question + ' ' + d[current_flow][j+1]
			ans = input(question).lower()
			# print(ans)
			counter = 1
			try:
				exit1 = 0
				while exit1 == 0:
					# print(d[current_flow + str(counter)][1], ans)
					if d[current_flow + str(counter)][1] == ans:
						# current_flow = current_flow + str(counter)
						next_flow =  str(counter)
						exit1 = 1
						break
					else:
						counter += 1

			except Exception as e:
				raise e
				print("\nRan out of options\n")
				exit = 1


		elif d[current_flow][0] == 'e':
			exit = 1

		if d[current_flow][-1] == 'p':
			to_be_printed = ""
			# print("Printing\n")
			# for j in range(len(d[current_flow])-2):
			# 	to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
			for j in range(len(d[current_flow])-2):
				# to_be_printed = to_be_printed + ' ' + d[current_flow][j+1]
				if d[current_flow][j+1] != "NEWLINE":
					print(d[current_flow][j+1], end = " ")
				else:
					print()
			# print(to_be_printed)

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
			save_record(result, time)

		current_flow = current_flow + next_flow



	print("Workflow execution completed (successfully)\n")




def check_database_new():
	payment_mode = input("Enter payment mode: ")
	amount = input("Enter paid amount: ")
	date = input("Enter date of payment: ")
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	mycol = mydb["payment_data"]
	result = mycol.find({'Amount': amount, 'Mode': payment_mode, 'LastPaymentDate': date})
	return result



def check_database():
	payment_mode = input("Enter payment mode: ")
	amount = input("Enter paid amount: ")
	date = input("Enter date of payment: ")
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

	# Checks result.
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
	    return "Recognized: {}".format(result.text), 1
	elif result.reason == speechsdk.ResultReason.NoMatch:
	    return "No speech could be recognized: {}".format(result.no_match_details), 0
	elif result.reason == speechsdk.ResultReason.Canceled:
	    cancellation_details = result.cancellation_details
	    return "Speech Recognition canceled: {}".format(cancellation_details.reason), 0
	    if cancellation_details.reason == speechsdk.CancellationReason.Error:
	        return "Error details: {}".format(cancellation_details.error_details), 0


def get_voice_input():
	exit = 0
	while exit != 1:
		detected_voice = speech_to_text_short()
		if detected_voice[1] == 1:
			print(detected_voice[0])
			x = input("Is the detected input correct? (Yes/No)")
			if x in affirmatives:
				return detected_voice[0]
		else:
			print(detected_voice[0])
			print("Press enter to retry voice input")
			x = input()


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
num = int(input("Enter workflow number: "))
execute_workflow(num)

# # CHANGE SPEECH TO TEXT RECOGNITION STUFF HERE


# warnings.filterwarnings("ignore")

# speech_key, service_region = "b3d1f03e79554727a8592485898db611", "westus"
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# # Creates a recognizer with the given settings
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)



# fpointer = open("queries_bsnl.txt", 'r')

# temp = fpointer.read()
# queries = temp.split('\n')
# print("\n\nQueries: ")
# print(queries)
# print()
# fpointer.close()

# choice = "no"
# query = ""
# max_index = 0
# affirmatives = ['YES', 'yes', 'Yes']

# # #SELECTING SINGLE CATEGORY
# # while (choice != 'YES') or (choice != 'yes') or (choice != 'Yes'):
# # 	sentence1 = input("What can I help you with? ")
# # 	output = select_category(queries, sentence1)
# # 	query = output[0]
# # 	max_index = output[1]
# # 	print("Do you require assistance with '", query "'?")
# # 	choice = input()


# # query = select_category(queries)

# #SELECTING MULTIPLE CATEOGARIES
# input_type = input("Choose input type Text/Voice (1 for Text, 2 for Voice)")

# sentence2_o = ""
# if input_type == '1':
# 	sentence2_o = input("What can I help you with?")
# else:
# 	sentence2_o = get_voice_input()

# sentence2 = spell_check(sentence2_o)
# cateogaries_indices = list()
# sentences = sentence2.replace(' and', '.').split('.')
# scores = list()
# for i in sentences:
# 	output = select_category(queries, i)
# 	if (output[1] not in cateogaries_indices) and (output[2] >= 0.125*output[3]):
# 		cateogaries_indices.append(output[1])
# 	print("Score: ", output[2])

# print("\n\nIdentified problems are: ")
# for j in cateogaries_indices:
# 	print(queries[j])

# if len(cateogaries_indices) == 0:
# 	print("No issues found, Exiting\n")
# 	exit()

# result = check_database()
# if result.count() >= 1:
# 	print("Record found\n")

# for i in cateogaries_indices:
# 	if i == 0:
# 		bill_payment_status(result)
# 	if i == 1:
# 		service_not_resumed(result)
# 	if i == 2:
# 		disturbance_in_line(result)

# # # SOLVING THE PROBLEMS IN SEQUENTIAL ORDER 

# # print("\nAnswer these questions in order (binary answers preferred): \n")
# # i_counter = 0
# # for i in cateogaries_indices:
# # 	print("Solving query/issue: ", queries[i], ": ")
# # 	fpointer_q = open(str(i+1) + '_q.txt')
# # 	questions = fpointer_q.read().split('\n')
# # 	fpointer_q.close()

# # 	fpointer_a = open(str(i+1) + '_a.txt')
# # 	answers = fpointer_a.read().split('\n')
# # 	fpointer_a.close()

# # 	binary_logic = questions[-1].split()
# # 	while_loop_counter = 0
# # 	solved = "No"
# # 	while while_loop_counter < len(questions)-1:
# # 		print(questions[while_loop_counter])
# # 		input_1 = input().split()
# # 		answered = 0
# # 		if (int(binary_logic[while_loop_counter]) == 1) and (input_1[0] in affirmatives):
# # 			print()
# # 			print(answers[while_loop_counter])
# # 			answered = 1
# # 		elif (int(binary_logic[while_loop_counter]) == 0) and (input_1[0] not in affirmatives):
# # 			print(answers[while_loop_counter])
# # 			answered = 1
# # 		if answered == 1:
# # 			solved = input("Did that solve your issue (Yes/No)").split()
# # 			if solved[0] in affirmatives:
# # 				break


# # 		while_loop_counter+=1

# # 	if solved[0] not in affirmatives:
# # 		# the bot ran out of ideas
# # 		print("Sorry, I could not help you with this. email your diagnostic logs to us and we'll get back to you")
# # 	else:
# # 		print("\nGlad to help you out with that :)")

# # 	i_counter+=1



print("\n\nExiting ...")







