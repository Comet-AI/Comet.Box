# Token Classification Pipeline

This token recognition pipeline is be loaded from pipeline() using the following task identifier: "ner" (for predicting the classes of tokens in a sequence: person, organisation, location or miscellaneous).

The pre-trained model used here is "dslim/bert-base-NER".

bert-base-NER is a fine-tuned BERT model that is ready to use for Named Entity Recognition and achieves state-of-the-art performance for the NER task. It has been trained to recognize four types of entities: location (LOC), organizations (ORG), person (PER) and Miscellaneous (MISC).

## Abbreviation 	Description
1. O	-            Outside of a named entity
2. B-MIS -	        Beginning of a miscellaneous entity right after another miscellaneous entity
3. I-MIS -	        Miscellaneous entity
4. B-PER -	        Beginning of a person’s name right after another person’s name
5. I-PER	-        Person’s name
6. B-ORG	-        Beginning of an organization right after another organization
7. I-ORG	-        organization
8. B-LOC	-        Beginning of a location right after another location
9. I-LOC	-        Location



## Sample Input :
My name is Sachin and I live in India and work at Qualcomm .

## Sample Output :
{'word': 'Sa', 'score': 0.999005138874054, 'entity': 'B-PER', 'index': 4, 'start': 11, 'end': 13}, 
{'word': '##chin', 'score': 0.8181593418121338, 'entity': 'B-PER', 'index': 5, 'start': 13, 'end': 17},
 {'word': 'India', 'score': 0.9997580051422119, 'entity': 'B-LOC', 'index': 10, 'start': 32, 'end': 37}, 
 {'word': 'Q', 'score': 0.9988409876823425, 'entity': 'B-ORG', 'index': 14, 'start': 50, 'end': 51},
  {'word': '##ual', 'score': 0.9065722227096558, 'entity': 'I-ORG', 'index': 15, 'start': 51, 'end': 54}, 
  {'word': '##com', 'score': 0.9969865083694458, 'entity': 'I-ORG', 'index': 16, 'start': 54, 'end': 57}, 
  {'word': '##m', 'score': 0.9973446130752563, 'entity': 'I-ORG', 'index': 17, 'start': 57, 'end': 58}

## From the output ,It can clearly be seen that the model has predicted Sachin as Person, India as Location and Qualcomm as Organization.