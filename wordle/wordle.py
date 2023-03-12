'''
Scrapes past Wordle results from rockpapershotgun.com and compares
them to a given guess to check if the word has been used before.
'''

import requests
import argparse
from bs4 import BeautifulSoup

from cachetools import cached, TTLCache

URL = 'https://www.rockpapershotgun.com/wordle-past-answers'
page = requests.get(URL)

# Caches results for 10 minutes
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_wordle_answers():
    soup = BeautifulSoup(page.content, "html.parser")
    words = soup.find_all(
        'li', string=lambda wordle_answer : wordle_answer and len(wordle_answer) == 5 
        )
    wordle_answers = []
    for word in words:
        wordle_answers.append(word.text.lower())
    return wordle_answers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Checks a Wordle answer against all previous answers')
    parser.add_argument('answer', help="A possible answer to check against previous worlde answers", type=str)
    args = parser.parse_args()

    wordle_answers = get_wordle_answers()

    if args.answer.lower() in wordle_answers:
        print('That word has been used before.')
    else:
        print('That word has never been used before.')





