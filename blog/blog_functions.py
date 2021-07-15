import requests
import json
from fake_useragent import UserAgent
import people_also_ask


def keyword():
  """
  fonction pour récupérer des keywords
  :return: keywords
  """
  keyword = "artist"
  keyword.replace(" ", "+")

  url = "http://suggestqueries.google.com/complete/search?output=firefox&hl=en&gl=us&q=" + keyword

  ua = UserAgent()
  headers = {"user-agent": ua.chrome}
  response = requests.get(url, headers=headers, verify=False)

  suggestions = json.loads(response.text)
  new_list = []
  for i in range(5):
    new_list.append(suggestions[1][i])
  print(new_list)


def questions():
  """
  fonctions pour générer des questions
  :return:
  """
  quest = people_also_ask.get_related_questions("art", 5)
  print(quest)

def quest_and_answer():
  """
  fonctions pour générer des questions et des réponses
  :return:
  """
  check_quest = people_also_ask.generate_answer("coffee")
  print(check_quest)
