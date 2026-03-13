from datasets import load_dataset
import anthropic

dataset = load_dataset("imdb", split="train")
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
