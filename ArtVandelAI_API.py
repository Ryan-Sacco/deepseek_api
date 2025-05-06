from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer
model_name = "deepseek-ai/deepseek-coder-1.3b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
model.eval()

# ArtVandelAI FastAPI App
app = FastAPI(
    title="ArtVandelAI",
    description="A FastAPI-powered API for generating text and code using the DeepSeek Coder model.",
    version="1.0.0"
)

# Prompt input schema with examples
class PromptRequest(BaseModel):
    prompt: str = Field(..., example="Write a Python function to reverse a string.")
    max_tokens: int = Field(256, example=100, ge=1, le=1024)

# Root route
@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to ArtVandelAI! Use the /generate endpoint or visit /docs to get started."
    }

# Main generate endpoint
@app.post("/generate", tags=["Text Generation"], summary="Generate text or code from a prompt")
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
