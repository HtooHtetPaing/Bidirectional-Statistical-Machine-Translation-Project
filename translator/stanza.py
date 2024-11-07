import stanza
stanza.download('my') # download English model
nlp = stanza.Pipeline('my') # initialize English neural pipeline
doc = nlp("ထူးထက်ပိုင်သည်ငတုံးဖြစ်သည်") # run annotation over a sentence
print(doc)
print(doc.entities)