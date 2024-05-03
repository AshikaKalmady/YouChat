import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from pytube import YouTube
from google.cloud import storage
import os
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Google Generative AI

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
 
def initialize_vertex_ai(project_id, location):
    """Initialize the Vertex AI environment."""
    vertexai.init(project=project_id, location=location)
 
def setup_model():
    """Set up the generative model with its configuration."""
    model_name = "gemini-1.5-pro-preview-0409"
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    return GenerativeModel(model_name=model_name), generation_config, safety_settings
 
def download_youtube_audio(youtube_link, output_path):
    """Download audio from a YouTube link."""
    yt = YouTube(youtube_link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path, filename="audio.mp4")
 
def upload_audio_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
 
def load_audio(audio_file_uri):
    """Load the audio file as a part."""
    return Part.from_uri(audio_file_uri, mime_type="audio/mpeg")
 
def generate_content(model, audio_file, prompt, generation_config, safety_settings):
    """Generate content using the model with provided settings."""
    transcript = ""
    contents = [audio_file, prompt]
    try:
        responses = model.generate_content(contents,
                                           generation_config=generation_config,
                                           safety_settings=safety_settings,
                                           stream=True)
        for response in responses:
            transcript += response.text
    except Exception as e:
        print("An error occurred:", str(e))
    return transcript
 
def save_to_cloud_storage(bucket_name, file_name, text):
    """Save a string to a file in Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(text)
 
def make_prompt(query, content):
    prompt = textwrap.dedent(f"""\
        You are a helpful and informative bot that answers questions using text from the reference passage included below.
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and
        strike a friendly and conversational tone.
        QUESTION: '{query}'
        PASSAGE: '{content}'
        ANSWER:
    """)
    return prompt
 
def generateText(youtube_link):
    project_id = "devpost-421903"
    location = "us-central1"
    bucket_name = "audio-file-voiceiq"
    local_audio_path = "/tmp"
    audio_file_name = "uploaded_audio.mp3"
    transcript_file_name = "transcription.txt"
    initialize_vertex_ai(project_id, location)
    model, generation_config, safety_settings = setup_model()
    download_youtube_audio(youtube_link, local_audio_path)
    upload_audio_to_gcs(bucket_name, os.path.join(local_audio_path, "audio.mp4"), audio_file_name)
    audio_file_uri = f"gs://{bucket_name}/{audio_file_name}"
    audio_file = load_audio(audio_file_uri)
    prompt = "Please transcribe this audio verbatim"
    transcript = generate_content(model, audio_file, prompt, generation_config, safety_settings)
    save_to_cloud_storage(bucket_name, transcript_file_name, transcript)
    return transcript
    
def query_transcript(transcript, query):
    prompt = make_prompt(query, transcript)
    genai_model = genai.GenerativeModel('models/gemini-pro')
    answer = genai_model.generate_content(prompt)
    return answer.text
 
# generateText('www.youtube.com/watch?v=t9IDoenf-lo', "What is the author talking about in 1 line?")