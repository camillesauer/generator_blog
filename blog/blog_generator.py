# -*- coding: utf-8 -*-
"""Blog generator

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p5VSGNSvjeI67uYeSMC0qK-Jsxs7pVub
"""

# !pip install fake_useragent
# !pip install people_also_ask
# !pip install happytransformer

import requests
import json
from fake_useragent import UserAgent
import pandas as pd
from people_also_ask import get_related_questions, get_simple_answer
from happytransformer import HappyGeneration
from happytransformer import GENSettings
from happytransformer import GENTrainArgs

keyword = "artist"
keyword.replace(" ", "+")

"""# **Etape 1 - Création de la liste de mots clés**"""

url = "http://suggestqueries.google.com/complete/search?output=chrome&hl=en&gl=us&q=" + keyword

ua = UserAgent()
headers = {"user-agent": ua.chrome}
response = requests.get(url, headers=headers, verify=False)

suggestions = json.loads(response.text)
new_list = []
for i in range(5):
  new_list.append(suggestions[1][i])
print(new_list)

keywords_list = [keyword] + new_list
print(keywords_list)

wordlist = []
for word in keywords_list:
  for i in range(5):
    wordlist.append(word)
print(wordlist)

df=pd.DataFrame(columns=['keywords'])

df['keywords'] = wordlist
df.head()

df.shape

"""# **Etape 2 - Identifier les questions**"""

get_related_questions(keyword, 4)

get_related_questions('artist', 4)

print(keywords_list)

questions = []
for word in keywords_list:
  print(word)
  #print(get_related_questions(word, 4))
  questions += get_related_questions(word, 4)
print(questions)

df['questions']=questions
df.head()

"""# **Etape 3 - Récupérer les réponses aux questions**"""

get_simple_answer("Is artist a job?")

def get_an_answer(row):
  return get_simple_answer(row)

df['answers'] = df['questions'].apply(get_an_answer)

df.head()

"""# **Etape 4 - Générer du texte**

https://happytransformer.com/text-generation/usage/


https://huggingface.co/EleutherAI/gpt-neo-125M?text=coffe+luwak
"""

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-125M")

args = GENSettings(no_repeat_ngram_size=2, do_sample=True, early_stopping=False, top_k=50, max_length=500, temperature=0.7)

result = happy_gen.generate_text("what is an artist? ", args=args)

print(result.text)

df['concat'] = df['questions'] + ' ' + df['answers']

def get_content(row):
  result = happy_gen.generate_text(row, args=args)
  return result.text

df['content'] = df['concat'].apply(get_content)

df.head()

df_to_save = df.drop(columns='concat')

df_to_save.to_csv('dataframe_contenu.csv', index=False)