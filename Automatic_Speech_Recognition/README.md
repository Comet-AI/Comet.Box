# Automatic Speech Recognition

Here,"facebook/wav2vec2-base-960h" model from hugging face model hub is deployed in order to recognize the speech automatically from an audio and convert it to text.
The base model was pretrained and fine-tuned on 960 hours of Librispeech on 16kHz sampled speech audio. While using the model ,we need to make sure that our speech input is also sampled at 16Khz.