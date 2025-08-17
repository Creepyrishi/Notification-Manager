import torch
import torch.nn as nn

# Model
class ClassificationHead(nn.Module):
  def __init__(self, in_fet, out_fet, p=.2):
    super().__init__()

    self.lays = nn.Sequential(
        nn.Linear(in_fet, 500),
        nn.ReLU(),
        nn.Dropout(p),
        nn.Linear(500, 400),
        nn.ReLU(),
        nn.Linear(400, 250),
        nn.ReLU(),
        nn.Dropout(p),
        nn.Linear(250, out_fet),
    )

  def forward(self, x):
    return self.lays(x)