# dses_and_llms
This repository contains data for the paper "Can AI Understand Text? Annotating, Projecting, and Interpreting Named Entities in Digital Scholarly Editions Using Large Language Models."

In the folder [./annotation_projection](annotation_projection), you will find a Jupyter Notebook for annotation projection using Claude. This notebook includes the prompt that was used (with minimal variation) across all models. The folder also contains the [./annotation_projection/input](input) documents (French source texts) and the corresponding annotated German translations in the [./annotation_projection/output](output)directory, as well as in subfolders named after the respective models.

Additionally, HTML files are provided that display the annotated model outputs side-by-side with the original French source texts.

In the [./NER](NER) folder, you will find a script for applying Named Entity Recognition (NER) using Flair to the French texts, as well as a Jupyter Notebook for performing NER with Claude.
