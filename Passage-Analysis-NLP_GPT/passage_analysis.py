from bs4 import BeautifulSoup
import re
import spacy
from spacy import displacy
import pandas as pd
# import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import openai

class PassageAnalize():
    def __init__(self, filepath) -> None:
        # 

    # def parse_text(self, filepath):
        html_doc=open(filepath, "r")
        soup = BeautifulSoup(html_doc, 'html.parser')
        parsed_doc = soup.get_text()
        parsed_doc = re.sub(r'\n+', '\n', parsed_doc)
        self.parsed_doc = parsed_doc

    def wordcloud(self):
        wordcloud = WordCloud(max_font_size=40).generate(self.parsed_doc)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        
    def text_analysis(self, POS):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.parsed_doc)
        POS_counts = {}
        for token in doc:
            if token.pos_ == POS:
                # If it's a noun, convert it to lowercase and add it to the noun_counts dictionary
                token = token.lemma_.lower()
                POS_counts[token] = POS_counts.get(token, 0) + 1

        # # Sort nouns and verbs by counts in descending order
        ranked_POS = pd.DataFrame.from_dict(POS_counts, orient='index',columns=['count'])
        ranked_POS.sort_values(by=['count'], ascending=False, inplace=True)

        fig, ax = plt.subplots(figsize=(12, 4))
        ranked_POS[:11].plot.bar(rot=20, ax=ax, title=f"Frequency of {POS}")
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        return {'ranked_POS': ranked_POS}

    def openai_analysis(self,api_key=None, keyword='Hannah Adrent'):

        if isinstance(api_key, str):
            openai.api_key = api_key
        else: 
            openai.api_key = os.getenv("OPENAI_API_KEY")
        # question = "Provide facts on this passage:"
        question = f"Extract the facts of this passage, and use {keyword}’s theory to interpret this passage"
        model = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=model,  
            messages=[{"role": "system", "content":f'{question}:"""{self.parsed_doc}"""'}]
            )

        # generated_text = response.choices[0].text
        return response['choices'][0]['message']['content']


            