from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from prompt_tem import prompt_template_str
import pandas as pd
import time
import os

df = pd.read_csv('output_file.csv')
df= df.drop('is_english', axis=1)

load_dotenv()

model = ChatGroq(
    model='openai/gpt-oss-120b',
    temperature='.1',
)

prompt_template = PromptTemplate.from_template(
    prompt_template_str
    )

for i in range(1000, df.shape[0], 100):
    notifications = df.iloc[i:i+100, :].to_string(index=False)
 
    prompt = prompt_template.invoke({'notification_here': notifications})
    response = model.invoke(prompt)

    with open('oss.csv', 'a', encoding='utf-8') as f:
        f.write(response.content)
    
    print(f"Sucess Up to {i+100}")
    time.sleep(10)