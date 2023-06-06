from django.shortcuts import render
from django.http import HttpResponse

from assistant.modules.NLP.nlp_processor import NLPProcessor
from assistant.modules.tts.tts_converter import TextToSpeechConverter
from assistant.modules.speech_recognition.speech_recognizer import SpeechRecognizer
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Set the Google Application Credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_key.json"

project_id = os.getenv("PROJECT_KEY")
session_id = os.getenv("SESS_ID")
# Create an instance of NLPProcessor
nlp_processor = NLPProcessor()

# Create an instance of TextToSpeechConverter
tts_converter = TextToSpeechConverter()

# Create an instance of SpeechRecognizer
stt_converter = SpeechRecognizer()

language_code = "en"

def voice_assistant(request):
    output_file = "media/output.wav"
    if request.method == "POST":
        form = request.POST
        text = form.get("user_input", "")
        
        response, fulfilment_text, confidence = nlp_processor.process_input(
            text,project_id, session_id, language_code
        )
        if response is not None and response.query_result is not None:
            fulfilment_text = response.query_result.fulfillment_text
            confidence = response.query_result.intent_detection_confidence
            # Generate audio file
            #tts_converter.speak(response)
            
            # Save audio file
            with open(output_file, "wb") as out:
                out.write(response.output_audio)
            
            # Prepare response data
            response_text = "Fulfillment text: {}\nConfidence: {}".format(
                fulfilment_text, confidence
            )
        else:
            response_text = "No valid response received from Dialogflow."
        
        # Render the template with response data
        return render(
            request, "voice_assistant.html", 
            {"form": form, "response_text": response_text, "response_audio": output_file}
        )
    else:
        form = {}
    
    # Render the template with empty form
    return render(
        request, "voice_assistant.html", 
        {"form": form}
    )
