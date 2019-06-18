import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import azure.cognitiveservices.speech as speechsdk


# fpointer = open("queries.txt", 'r')

# temp = fpointer.read()
# queries = temp.split('\n')
# print("\n\nQueries: ")
# print(queries)
# print()
# fpointer.close()

def speech_to_text_short():

	# speech_recognizer parameters defined in main
	result = speech_recognizer.recognize_once()

	# Checks result.
	if result.reason == speechsdk.ResultReason.RecognizedSpeech:
	    print("Recognized: {}".format(result.text))
	elif result.reason == speechsdk.ResultReason.NoMatch:
	    print("No speech could be recognized: {}".format(result.no_match_details))
	elif result.reason == speechsdk.ResultReason.Canceled:
	    cancellation_details = result.cancellation_details
	    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
	    if cancellation_details.reason == speechsdk.CancellationReason.Error:
	        print("Error details: {}".format(cancellation_details.error_details))


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
	# print("Sentence after lemmatizing: ", lemmatized_sent)
	return lemmatized_sent


def remove_stop_words(sent):
	final_sent = ""

	l = sent.split()
	for i in l:
		if i not in stopwords.words('english'):
			final_sent = final_sent + i + ' '

	# final_sent1 = final_sent1[:len(final_sent1)-1] + '.'
	final_sent = final_sent[:len(final_sent)-1]
	# print("Sentence after removing stop words: ", final_sent)
	return final_sent


# word1 = input()
# word2 = input()
# similarity_score = get_similarity_score(word1, word2)
# print(similarity_score)


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

	lemmatized_sent1 = lemmatize_sentence(sentence1)
	# lemmatized_sent2 = lemmatize_sentence(sentence2)
	final_sent1 = remove_stop_words(lemmatized_sent1)
	# final_sent2 = remove_stop_words(lemmatized_sent2)


	max_score = 0
	max_index = 0
	for i in range(len(queries)):
		lemmatized_sent2 = lemmatize_sentence(queries[i])
		final_sent2 = remove_stop_words(lemmatized_sent2)
		score = get_overall_score(final_sent1, final_sent2)
		print("Score for query ", i, "is ", score)
		if score > max_score:
			max_score = score
			max_index = i

	# print("Do you require assistance with '", queries[max_index], "'?")
	# choice = input()
	return queries[max_index], max_index, max_score



# __main__  STARTING OF MAIN FUNCTION

# CHANGE SPEECH TO TEXT RECOGNITION STUFF HERE

speech_key, service_region = "b3d1f03e79554727a8592485898db611", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)



fpointer = open("queries.txt", 'r')

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

# #SELECTING SINGLE CATEGORY
# while (choice != 'YES') or (choice != 'yes') or (choice != 'Yes'):
# 	sentence1 = input("What can I help you with? ")
# 	output = select_category(queries, sentence1)
# 	query = output[0]
# 	max_index = output[1]
# 	print("Do you require assistance with '", query "'?")
# 	choice = input()


# query = select_category(queries)

#SELECTING MULTIPLE CATEOGARIES
# input_type = input("Choose input type Text/Voice (1 for Text, 2 for Voice)")

sentence2 = input("What can I help you with?")
cateogaries_indices = list()
sentences = sentence2.replace(' and', '.').split('.')
scores = list()
for i in sentences:
	output = select_category(queries, i)
	if (output[1] not in cateogaries_indices) and (output[2] >= 0.125):
		cateogaries_indices.append(output[1])
	print("Score: ", output[2])

print("\n\nIdentified problems are: ")
for j in cateogaries_indices:
	print(queries[j])


# SOLVING THE PROBLEMS IN SEQUENTIAL ORDER 

print("\nAnswer these questions in order (binary answers preferred): \n")
i_counter = 0
for i in cateogaries_indices:
	print("Solving query/issue: ", queries[i], ": ")
	fpointer_q = open(str(i+1) + '_q.txt')
	questions = fpointer_q.read().split('\n')
	fpointer_q.close()

	fpointer_a = open(str(i+1) + '_a.txt')
	answers = fpointer_a.read().split('\n')
	fpointer_a.close()

	binary_logic = questions[-1].split()
	while_loop_counter = 0
	solved = "No"
	while while_loop_counter < len(questions)-1:
		print(questions[while_loop_counter])
		input_1 = input().split()
		answered = 0
		if (int(binary_logic[while_loop_counter]) == 1) and (input_1[0] in affirmatives):
			print()
			print(answers[while_loop_counter])
			answered = 1
		elif (int(binary_logic[while_loop_counter]) == 0) and (input_1[0] not in affirmatives):
			print(answers[while_loop_counter])
			answered = 1
		if answered == 1:
			solved = input("Did that solve your issue (Yes/No)").split()
			if solved[0] in affirmatives:
				break


		while_loop_counter+=1

	if solved[0] not in affirmatives:
		# the bot ran out of ideas
		print("Sorry, I could not help you with this. email your diagnostic logs to us and we'll get back to you")
	else:
		print("\nGlad to help you out with that :)")

	i_counter+=1



print("\n\nExiting ...")







