**Listed below are the different implemetations**
- [Generative Adversarial Networks](#generative-adversarial-networks)
- [Conditional Generative Adversarial Networks](#conditional-generative-adversarial-network)


# Generative Adversarial Networks
[![digitmnist-gan.gif](https://i.postimg.cc/pdwbwzR8/digitmnist-gan.gif)](https://postimg.cc/t1NMP11C)

## Introduction

GANs belong to a set of algorithms named generative models. These algorithms belong to the field of unsupervised learning, a sub-set of ML which aims to study algorithms that learn the underlying structure of the given data, without specifying a target value. Generative models learn the intrinsic distribution function of the input data p(x) (or p(x,y) if there are multiple targets/classes in the dataset), allowing them to generate both synthetic inputs x’ and outputs/targets y’, typically given some hidden parameters.

## GAN architecture
[![GAN.jpg](https://i.postimg.cc/xjbTFB44/GAN.jpg)](https://postimg.cc/PNTjCVhW)


# Conditional Generative Adversarial Network 
[![digitmnist-cgan.gif](https://i.postimg.cc/FKD29bT6/digitmnist-cgan.gif)](https://postimg.cc/XZB2L5SK)

## Introduction

Conditional GAN is a generative adversarial network whose Generator and Discriminator are conditioned during training by using some additional information. This auxiliary information could be, in theory, anything, such as a class label, a set of tags, or even a written description.

During CGAN training, the Generator learns to produce realistic examples for each label in the training dataset, and the Discriminator learns to distinguish fake example-label pairs from real example-label pairs.

## CGAN architecture
[![CGAN.jpg](https://i.postimg.cc/3JLP2FXF/CGAN.jpg)](https://postimg.cc/kBb1m8h2)