# API import Section
from fastapi import FastAPI, Request
import asyncio
# LLM section import
from llama_cpp import Llama
# IMPORTS FOR TEXT GENERATION PIPELINE CHAIN
import copy

app = FastAPI(
    title="Inference API for TinyLlamaOO Instruct",
    description="A simple API that use TinyLlama OpenOrca for Instruction-RAG",
    version="2.0",
)

### INITIALIZING TINYLLAMA-OpenOrca MODEL
modpath = "model/tinyllama-1.1b-1t-openorca.Q4_K_M.gguf"
llm = Llama(
        model_path=modpath, n_gpu_layers=0,
        n_ctx=2048, verbose=False,
        stop=["<|im_end|>",'</s>'],
        chat_format="chatml",
        )


@app.get('/')
async def hello():
    return {"hello" : "Artificial Intelligence  enthusiast"}


@app.get('/model')
async def model():
    text = "Who is Tony Stark?"
    template = f"""<|im_start|>system\nYou are a helpful ChatBot assistant.<|im_end|>\n<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant"""
    res = llm(template)
    result = copy.deepcopy(res)
    return {"result" : result['choices'][0]['text']}


@app.get('/tinyllama')
async def tinyllama(text : str):
    template = f"""<|im_start|>system
You are a helpful ChatBot assistant.<|im_end|>
<|im_start|>user
{text}<|im_end|>
<|im_start|>assistant"""
    res = llm(template,temperature=0.42,repeat_penalty=1.5,max_tokens=300)
    result = copy.deepcopy(res)
    return {"result" : result['choices'][0]['text']}


from pydantic import BaseModel
from typing import List


class Instruction(BaseModel):
    temperature: float| None = 0.1
    maxlen: int| None = 150
    sysmessage: str
    promptmessage : str

@app.post('/instruct/')
async def instruct(instruction : Instruction):
    chattemperature = instruction.temperature
    chatlen = instruction.maxlen
    template = f"""<|im_start|>system
{instruction.sysmessage}<|im_end|>
<|im_start|>user
{instruction.promptmessage}<|im_end|>
<|im_start|>assistant"""
    stops=["<|im_end|>",'</s>']
    chat = llm(template,temperature=chattemperature,
               stop=stops,repeat_penalty=1.7,max_tokens=chatlen)
    ongoingchat = copy.deepcopy(chat)
    response = {"result" : ongoingchat['choices'][0]['text']}
    print(ongoingchat['choices'][0]['text'])
    return response