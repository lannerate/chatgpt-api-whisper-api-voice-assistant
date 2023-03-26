import gradio as gr
import openai, config, subprocess
openai.api_key = config.OPENAI_API_KEY
messages = [{"role": "system", "content": 'You are an AI Assistant. Respond to all input in 50 words or less.'}]

def transcribe(input_text):
    global messages
    model_name = "gpt-3.5-turbo"
    messages.append({"role": "user", "content": input_text})
    
    try:
        response = openai.ChatCompletion.create(model=model_name, messages=messages)
        system_message = response["choices"][0]["message"]
        messages.append(system_message)
        subprocess.call(["say", system_message['content']])
    except Exception as e:
        system_message = str(e)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs="text", outputs="text", title="GPT Chatbot", description="Enter some text to start a conversation.").launch(share=True)