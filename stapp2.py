import streamlit as st
import requests 
import ast
from time import  sleep
import datetime


def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

# Function to POST on the FastAPI EndPoint
def get_reply(temperature, maxlen, sysmessage, promptmessage):   
    API_URL = "http://127.0.0.1:8000/instruct/"
    headers = {}
    payloads = {
        "temperature" : temperature,
        "maxlen" : maxlen,
        "sysmessage" : sysmessage,
        "promptmessage" : promptmessage
    }
    response = requests.post(API_URL, headers=headers, json=payloads)
    risposta = response.content.decode("utf-8")
    import ast
    res = ast.literal_eval(risposta)
    return res


# Set the webpage title
st.set_page_config(
    page_title="Your own 🕸️ NetworkGPT",
    page_icon="🐋")

# Create a header element
st.header("Your own NetworkGPT with 🦙TinyLlama OpenOrca🐋")
st.markdown("#### :green[*tinyllama-1.1b-1t-openorca.Q4_K_M.gguf - the best tiny model?*]")

if "logfilename" not in st.session_state:
## Logger file
    tstamp = datetime.datetime.now()
    tstamp = str(tstamp).replace(' ','_')
    tstamp = str(tstamp).replace(':','_')
    logfile = f'{tstamp[:-7]}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🐋: How may I help you today?\-------------------------\n')

if "sysmessage" not in st.session_state:
    st.session_state.sysmessage = ""

if "promptmessage" not in st.session_state:
    st.session_state.promptmessage = 0

if "maxlen" not in st.session_state:
    st.session_state.maxlen = 200

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

with st.sidebar:
    st.markdown("""### Parameters:""", unsafe_allow_html=True)
    st.session_state.temperature = st.slider('Temperature:', min_value=0.00, max_value=1.0, value=0.1, step=0.02)
    st.session_state.maxlen = st.slider('MaxLength:', min_value=50, max_value=500, value=200, step=5)
    st.markdown("---")
    st.markdown("### Logfile")
    st.markdown(st.session_state.logfilename)


st.session_state.sysmessage = st.text_area('System Message', value="", height=20)
st.session_state.promptmessage = st.text_area('User Message', value="", height=170)
btn = st.button('Ask TinyLlama', type='primary')
resultarea = st.empty()
resultarea.write("Reply will go here...")
st.write('---')

if btn:
    log = f'SYS: {st.session_state.sysmessage}\nUSER: {st.session_state.promptmessage}'
    writehistory(st.session_state.logfilename,log)
    response = get_reply(st.session_state.temperature,st.session_state.maxlen,
                         st.session_state.sysmessage,st.session_state.promptmessage)
    resultarea.markdown(response['result'])
    log = f"TINYLLAMA: {response['result']}\n---\n\n"
    writehistory(st.session_state.logfilename,log)

