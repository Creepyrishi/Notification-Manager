import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

device = "cuda" if torch.cuda.is_available() else "cpu"

class MyDataset(Dataset):
  def __init__(self, x, y):
    super().__init__()
    self.x = torch.tensor(x, dtype=torch.float64)
    self.y = torch.tensor(y, dtype=torch.long)

  def __len__(self):
    return len(self.x)

  def __getitem__(self, idx):
    return self.x[idx], self.y[idx]


def train(epochs, model, optimizer, loss_fn, dataset_train, dataset_test):
  for epoch in range(epochs):
    train_loss = 0.0
    test_loss = 0.0
    test_i = 0
    it = 0
    for batch in dataset_train:
      x, y = batch
      x, y = x.to(device).float(), y.to(device)
      model.train()
      y_pred = model(x)
      loss = loss_fn(y_pred, y)
      loss.backward()
      optimizer.step()
      optimizer.zero_grad()
      train_loss += loss.item()
      it += 1

    model.eval()
    with torch.no_grad():
      for batch in dataset_test:
        x, y = batch
        x, y = x.to(device).float(), y.to(device)
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        test_loss += loss.item()
        test_i += 1

    print(f"Epoch: {epoch}, Train Loss: {train_loss/it}, Test Loss: {test_loss/test_i}")