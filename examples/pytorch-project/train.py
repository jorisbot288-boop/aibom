import torch
import torch.nn as nn

model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)