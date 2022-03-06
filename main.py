import uvicorn
import shutil
import moviepy.editor as mp
import subprocess
import speech_recognition as sr 
import os 
from os import path
from pydub import AudioSegment
from pydub.silence import split_on_silence
from transformers import pipeline
from fastapi import FastAPI,File,UploadFile
app=FastAPI()
r = sr.Recognizer()
summary_text="Harshit is a Gandu"
async def model(file):
    summary_text="L"
    clip =await mp.VideoFileClip(file)
    summary_text="Lo"
    await clip.audio.write_audiofile(r"AIaudio.mp3")
    summary_text="Lod"

    # convert mp3 to wav file
    '''subprocess.call(['ffmpeg', '-i', 'AIaudio.mp3',
    				'AIaudio.wav'])
    path = "AIaudio.wav"
    
    full_text=get_large_audio_transcription(path)
    print(full_text)
    summary_text="lodu"#full_text'''
    '''f1=open("Transcript.txt","w+")
    f1.write(full_text)
    

    summarizer=pipeline("summarization")

    summary = summarizer(full_text,max_length=200,do_sample=False)

    summary_text=summary[0]['summary_text']
    print(summary_text)

    f=open("Summary.txt","w+")

    f.write(summary_text)

    f.close()

    f1.close()'''
async def get_large_audio_transcription(path):
   
   
    sound = AudioSegment.from_wav(path)  
    chunks =await split_on_silence(sound,
        
        min_silence_len = 500,
        
        silence_thresh = sound.dBFS-14,
       
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
       
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
@app.get('/')
def index():
    return{"message":"Hello,Stranger"};
@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome ':f'{name}'};
@app.get('/{name}')
def get_name2(name: str):
    return {'Welcome ':f'{name}'};
@app.post("/file")
async def root(file: UploadFile = File(...)):
    summary_text="L"
    with open(f'{file.filename}','wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
    clip = mp.VideoFileClip(file.filename)
    clip.audio.write_audiofile(r"AIaudio.mp3")
    #subprocess.call(['ffmpeg', '-i', 'AIaudio.mp3','AIaudio.wav'])
    with open("AIaudio.mp3",'wb') as buffer:
         shutil.copyfileobj('AIaudio.mp3',buffer)
    # input_file = "AIaudio.mp3"
    # output_file = "result.wav"
    # sound = AudioSegment.from_mp3(input_file)
    # sound.export(output_file, format="wav")
    model(file)
    return {"file_name":summary_text}


if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)