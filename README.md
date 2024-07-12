# Arabic Text Summarization and Complaint Classification using Aya LLM
## Project Overview
The Egyptian government receives a large number of complaints and feedback on a daily basis. Managing and addressing these complaints efficiently is a significant challenge. To assist with this, we developed a system that helps administrators classify complaints into the correct categories and provides concise summaries of the complaints. This project leverages modern natural language processing techniques, including Aya LLM, to achieve accurate classification and summarization of Arabic text.

## Problem Statement
The main problem addressed by this project is the efficient handling of numerous complaints and feedback received daily by the Egyptian government. The system aims to:

## Technologies Used
Flask: A lightweight web framework used to build the web application.
MySQL: A relational database management system used for storing complaint data.
Aya LLM: A powerful language model used for text summarization and classification.

Prompt Engineering
Prompt engineering is a crucial aspect of working with language models like Aya LLM. By crafting effective prompts, we can guide the model to produce more accurate and relevant results. Here are some strategies we used for prompt engineering in this project:


Classify complaints into the appropriate sections.
Summarize the complaints to provide a quick overview for administrators.
## Complaint Classification Approach
## Initial Attempts
### TF-IDF (Term Frequency-Inverse Document Frequency)

We initially used TF-IDF for text classification.
Challenges:
Required a large amount of data for training.
Struggled with misspelled words.
Overall, it did not perform well for our needs.
### Arabert (Arabic BERT)

We then moved to using Arabert to embed the complaints.
We used clustering techniques to group similar complaints.
New complaints were classified into one of these clusters.
This approach improved classification but was still not ideal.
## Final Solution
### Aya LLM
We implemented Aya LLM for text classification.
Results:
It provided the most accurate classification.
However, it was the slowest among the methods we tried.

# Demo 
## User Demo
The user fills out an ordinary form with his complaint and personal data.

https://github.com/user-attachments/assets/d242c511-6353-41a5-9f0c-5d12eb872747

## Admin Demo
After the user submits the form, the Complaint is classified to one of the government sections. 
Every section includes only the related complaints. the Admin can browse any complaint and summarize it using Aya LLM.

https://github.com/user-attachments/assets/4714874b-99de-43dc-a81e-c54b0ea12e5c

How to Run the Project
Prerequisites
Python 3.8+
Flask
MySQL
Required Python packages (listed in requirements.txt)
Setup Instructions

### Clone the repository:
```git clone https://github.com/yourusername/arabic-text-summarization.git```
```cd arabic-text-summarization```

### Install dependencies:

```pip install -r requirements.txt```

create ```.env``` file and set database credentials in it.
then open a terminal and write ```python```
then run these two lines:

```>> from app import db```

```>> db.create_all()```

then you are ready to run the app.py and run the server.

```python app.py```

Open your browser and navigate to http://localhost:5000.


## Future Work

Performance Optimization: Work on optimizing the performance of Aya LLM to reduce the time taken for classification(by trying to fine-tune it using LoRA on a similar complaint dataset.

Scalability: Ensure the system can handle a growing number of complaints as the volume increases.


