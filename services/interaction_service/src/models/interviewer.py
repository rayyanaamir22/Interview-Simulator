from typing import AsyncGenerator
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import asyncio
from queue import Queue
from threading import Thread

class InterviewerModel:
    def __init__(self):
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )
        
        self.prompt_template = """<s>[INST] You are an experienced technical interviewer conducting a job interview. 
        Your responses should be professional, concise, and focused on evaluating the candidate's technical knowledge.
        
        Previous conversation:
        {user_input}
        
        Interviewer: [/INST]"""
    
    def _generate_response(self, user_input: str, queue: Queue):
        """Generate response in a separate thread and put chunks in queue."""
        try:
            # Format the prompt
            prompt = self.prompt_template.format(user_input=user_input)
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    streamer=None
                )
            
            # Decode and stream response
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            response = response[len(prompt):]  # Remove the prompt from the response
            
            # Put response in queue
            queue.put(response)
            
        except Exception as e:
            queue.put(json.dumps({"error": str(e)}))
        finally:
            queue.put(None)  # Signal completion
    
    async def generate_response(self, user_input: str) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the interviewer model."""
        queue = Queue()
        
        # Start generation in a separate thread
        thread = Thread(target=self._generate_response, args=(user_input, queue))
        thread.start()
        
        # Stream the response
        while True:
            response = queue.get()
            if response is None:  # End of generation
                break
            yield response
            await asyncio.sleep(0.1)  # Small delay to prevent overwhelming the client 