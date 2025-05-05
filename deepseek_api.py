from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

#loads the model and tokenizer

model_name = "deepseek-ai/deepseek-coder-1.3b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
model.eval()

#fastAPI app

app = FastAPI()

#Defines request schema
class PromptRequest(BaseModel):
	prompt: str
	max_tokens: int = 256

@app.post("/generate")
def generate_text(request: PromptRequest):
	inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
	with torch.no_grad():
		output = model.generate(
			**inputs,
			max_length=inputs["input_ids"].shape[1] + request.max_tokens,
			do_sample=True,
			top_p=0.95,
			temperature=0.8,
		)
	result = tokenizer.decode(output[0], skip_special_tokens=True)
	return {"output": result}
