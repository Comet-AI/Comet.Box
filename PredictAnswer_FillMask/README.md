# Answer-Prediction_Fill in the Blanks

In order to implement this function, FillMask pipeline is deployed.This mask filling pipeline can be loaded from pipeline() using the following task identifier: "fill-mask".

# Sample Input :
The sun rises in the <mask> and sets in the west.

Here, blank space to be filled is between "the" and "and" ,So, mask is placed there.

# Sample Output :

{'score': 0.8162986040115356,
  'sequence': 'The sun rises in the east and sets in the west.',
  'token': 3017,
  'token_str': ' east'},

 {'score': 0.11573756486177444,
  'sequence': 'The sun rises in the north and sets in the west.',
  'token': 1926,
  'token_str': ' north'},

 {'score': 0.035447943955659866,
  'sequence': 'The sun rises in the south and sets in the west.',
  'token': 2077,
  'token_str': ' south'},

 {'score': 0.009359453804790974,
  'sequence': 'The sun rises in the southwest and sets in the west.',
  'token': 10103,
  'token_str': ' southwest'},

 {'score': 0.00917516928166151,
  'sequence': 'The sun rises in the northeast and sets in the west.',
  'token': 9489,
  'token_str': ' northeast'}

Here,We can see that the correct answer should be east and from the deployed system also,We have the output score for east as 81.6% which is a quite good prediction.