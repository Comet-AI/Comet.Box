# Question Answering Pipeline

It is implemented by deploying question-answering pipeline. This question answering pipeline can be loaded from pipeline() using the following task identifier: "question-answering".
It will require the two things :
 1. Question that is to be answered.
 2. context of the question,from which one can search for the answer.


 # sample input :
    'question':"what is the colour of this cow.",
    'context':"There was a man in a village in Bihar.He has a white coloured cow ,who gives 5 litres of milk everyday. The man became very rich by selling the milk."

# Sample Output :
    'answer': 'white', 'end': 52, 'score': 0.9587785005569458, 'start': 47

    It can clearly be seen that It has predicted the answer to be white with an accuracy score of 95.8% ,which is really awesome.

