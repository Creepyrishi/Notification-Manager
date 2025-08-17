import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np

model_path = "Embedding Model\model_qint8_arm64.onnx"
tokenizer_path  = ".\Embedding Model"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
session = ort.InferenceSession(model_path,  providers=["CPUExecutionProvider"])


def get_embedding(text):
    tokenized_text = tokenizer(text, return_tensors="np", padding=True, truncation=True)

    onnx_inputs = {
        "input_ids": tokenized_text["input_ids"].astype(np.int64),
        "attention_mask": tokenized_text["attention_mask"].astype(np.int64),
        "token_type_ids": tokenized_text["token_type_ids"].astype(np.int64)
    }

    outputs = session.run(None, onnx_inputs)
    last_hidden = outputs[0]

    # mean pooling 
    expaned_mask = np.expand_dims(onnx_inputs['attention_mask'], -1)

    sum_embedding = np.sum(last_hidden * expaned_mask, axis=1)
    sum_mask = np.clip(expaned_mask.sum(axis=1), a_min=1e-9, a_max=None)

    # Mean pooled sentence embedding
    sentence_embeddings = sum_embedding / sum_mask

    return (sentence_embeddings[0])