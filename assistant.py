import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are an therapist. Respond to all input in 50 words or less.'}]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # transcript= openai.Audio.translate("whisper-1", audio_file) # translate to english at this time

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch(share=True)
ui.launch()