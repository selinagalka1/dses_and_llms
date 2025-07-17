# dses_and_llms
This repository contains data for the paper "Can AI Understand Text? Annotating, Projecting, and Interpreting Named Entities in Digital Scholarly Editions Using Large Language Models."

In the folder [./annotation_projection](annotation_projection), you will find a Jupyter Notebook for annotation projection using Claude. This notebook includes the prompt that was used (with minimal variation) across all models. The folder also contains the input documents (French source texts) and the corresponding annotated German translations in the output directory, as well as in subfolders named after the respective models.

Additionally, HTML files are provided that display the annotated model outputs side-by-side with the original French source texts.

In the [./NER](NER) folder, you will find a script for applying Named Entity Recognition (NER) using Flair to the French texts, as well as a Jupyter Notebook for performing NER with Claude.

In the [./person_relationships](person_relationships) folder the results of the cbat-bot Claude 4 can be found.

The data available in this GitHub repository (the texts for the digital edition) is still under development and represents the current state of our work. The French TEI/XML encoding and the German translation are components of the forthcoming digital edition, which will be published as part of the FWF-funded project “Tout Vienne me riait“ Family and court relations in the memoirs of Countess Louise Charlotte von Schwerin (1684−1732)” (Principal Investigator: Ines Peper) which is running from 2022-2026, Grant DOI: 10.55776/P34943. Please note that these encoded texts are provisional and reflect a work-in-progress.
