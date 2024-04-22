from transformers import pipeline

'''
pipe = pipeline("text-generation", model="epfl-llm/meditron-70b")

out=pipe("what are the symptoms of covid-19?")
print(out)'''

from transformers import pipeline

classifier = pipeline("sentiment-analysis")

out=classifier("We are very happy to show you the 🤗 Transformers library.")
print(out)