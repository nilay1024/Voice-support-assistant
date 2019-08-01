# Chatbot and voice assistant

## Voice assistant:

### Services/modules used (installation and resources):
  #### nltk
    https://www.nltk.org/install.html
  #### Azure cognitive speech services (Speech to text and text to speech)
    pip install azure-cognitiveservices-speech
    https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstart-python
    https://azure.microsoft.com/en-in/services/cognitive-services/speech-services/
  #### Pymongo (for mongodb database linked at the backend
    To modify mongodb database parameters, go to check_database_new() or check_database()
    https://api.mongodb.com/python/current/installation.html
    https://www.w3schools.com/python/python_mongodb_getstarted.asp
  #### Google text to speech (gTTS)
    https://www.geeksforgeeks.org/convert-text-speech-python/
    https://pypi.org/project/gTTS/
  #### Monkeylearn API for sentiment analysis
    modify parameters inside function sentiment_analysis_monkeylearn(text)
    https://monkeylearn.com/text-analysis/
  #### Other modules need to be installed
    Pyttsx3: pip install pyttsx3
    Autocorrect:
      pip install autocorrect
      https://pypi.org/project/autocorrect/

### How to run:
  #### Command
  `python3 sum_project_new.py`
  #### Required files:
    queries.txt (current implementation is using 'queries_bsnl.txt', can be modified in the main function)
      Contains the workflow queries (check the attached 'queries_bsnl.txt' file for reference)

    workflow_1.txt, workflow_2.txt .. (and so on, depending on number of workflows)
      number of queries in 'queries.txt' file should be same as number of workflow files
      every query has its on unique workflow file named workflow_x.txt (where x is the query number)
  #### Workflow file format
  - Every sentence is preceded by a number and a character.
  - It may be followed by 'p' or 'pu'
  - Every line begins with a number which specifies the current flow and is always unique.
  - __Instructions on how that unique number is coded are given in the num_coding_instructions.docx file__
  - If a line ends with p, the sentence has to be communicated to the user.
  - If a line ends with pu, the sentence has to be communicated to the user and database needs to be updated (like in the case of filing a complaint, database needs to be updated and complaint number should be communicated to the user)
  - The second word of every line is a character which defines the purpose of the sentence (Whether that is a question (input required), a statement, or if there is something needed to be checked within the database). Further instructions can be found in num_coding_instructions.docx file.

### To create database
  `python mongodb_test.py`. Make sure date is in the format dd-mm-yy (hyphens included)

### Parameters needed to be modified to implement this on large scale:
  - Azure Cognitive Services key: __speech_key__ variable inside the main function
  - Monkeylearn API key: __ml__ variable inside sentiment_analysis_monkeylearn() function
  - MongoDB parameters: __myclient, mydb, mycol__ variables inside check_database_new() function
  - Complaint file: __fopen__ variable inside save_record function

## Chatbot:

  #### All the modules needed for voice assistant are required here as well
  #### WebSockets (required for connecting javascript (chatbot frontend) with python (server end script))
    Installation:
    pip install websockets
    https://websockets.readthedocs.io/en/stable/intro.html
    SimpleWebSocketServer: pip install SimpleWebSocketServer

### How to run:
  #### Modify these parameters (Not requied if server is localhost):
  -  `var socket` inside Webpage_client/script.js file. Specify the host server websocket URL. Ignore if server is localhost.
  - `server = SimpleWebSocketServer('', 8000, SimpleChat)`: replace ' ' by server URL. Ignore if server is localhost

### Start server, client:
  - start python websocket server (server system) `python echo_server.py`. It should ideally be running continuously in the background
  - run the webpage client (Webpage_client/index.html).
  - run the python script: `python test_new.py`. A welcome message should appear in chatbot if everything goes right.
