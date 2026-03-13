from datasets import load_dataset
from transformers import AutoModel, AutoTokenizer

dataset = load_dataset("squad", split="train")
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
