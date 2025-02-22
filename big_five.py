import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaTokenizer, RobertaModel
from sklearn.model_selection import train_test_split
from torch.optim.lr_scheduler import StepLR

class BigFiveDataset(Dataset):
    def __init__(self, df, tokenizer, max_len=512):
        self.texts = df['text'].tolist()
        self.labels = df[['Extraversion', 'Agreeableness', 'Openness', 'Neuroticism', 'Conscientiousness']].values
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        labels = torch.tensor(self.labels[idx], dtype=torch.float)
        encoding = self.tokenizer(text, padding='max_length', truncation=True, max_length=self.max_len, return_tensors="pt", return_attention_mask=True)
        return {"input_ids": encoding["input_ids"].squeeze(0),
                "attention_mask": encoding["attention_mask"].squeeze(0),
                "labels": labels}

# Modelo basado en RoBERTa
class RoBERTaBigFive(nn.Module):
    def __init__(self):
        super(RoBERTaBigFive, self).__init__()
        self.roberta = RobertaModel.from_pretrained("roberta-base")
        self.fc = nn.Linear(self.roberta.config.hidden_size, 5)
        # self.dropout = nn.Dropout(0.3)
        self.activation = nn.LeakyReLU()  # Cambiado a ReLU

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        x = self.fc(outputs.pooler_output)
        return self.activation(x)

# Función de entrenamiento
def train(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    for batch in dataloader:
        input_ids, attention_mask, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch['labels'].to(device)
        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)

# Función de evaluación
def test(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    total = 0
    with torch.no_grad():
        for batch in dataloader:
            input_ids, attention_mask, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch['labels'].to(device)
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            total_loss += loss.item()

    return total_loss / len(dataloader)

if __name__ == "__main__":

    df = pd.read_csv("Big-Five_Backstage.csv")
    df = df[['text', 'Extraversion', 'Agreeableness', 'Openness', 'Neuroticism', 'Conscientiousness']].dropna()

    # Dividir en entrenamiento y prueba
    train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)

    # Tokenizador
    tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
    # Preparación de datos
    dataset_train = BigFiveDataset(train_df, tokenizer)
    dataset_test = BigFiveDataset(test_df, tokenizer)
    train_dataloader = DataLoader(dataset_train, batch_size=8, shuffle=True)
    test_dataloader = DataLoader(dataset_test, batch_size=8, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = RoBERTaBigFive().to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-4)
    scheduler = StepLR(optimizer, step_size=3, gamma=0.1)  # Scheduler para reducir la tasa de aprendizaje

    criterion = nn.MSELoss()

    # Entrenamiento
    epochs = 5
    for epoch in range(epochs):
        train_loss = train(model, train_dataloader, optimizer, criterion, device)
        print(f"Epoch {epoch+1}, Train Loss: {train_loss:.4f}")
        scheduler.step()  # Actualizar la tasa de aprendizaje

    # Evaluación
    test_loss = test(model, test_dataloader, criterion, device)
    print(f"Test Loss: {test_loss:.4f}")

    model_save_path = "roberta_big5.pth"
    torch.save(model.state_dict(), model_save_path)
    print(f"Modelo guardado en {model_save_path}")
