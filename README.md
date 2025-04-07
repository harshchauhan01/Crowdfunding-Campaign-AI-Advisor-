
# 🚀 Laila – AI Powered Crowdfunding Campaig Advisor

This project focuses on guiding users through the process of building successful crowdfunding campaigns with the help of an intelligent assistant named Laila. The app is built using Streamlit and integrates a large language model (Mistral-7B-Instruct) from Hugging Face to provide real-time, context-aware advice.

The key features include:

Interactive campaign builder form to collect project details like name, funding goal, unique features, target audience, and duration

AI-powered assistant “Laila” that responds like a friendly professional, offering strategic guidance at every step

Dynamic generation of tailored strategies including pitch ideas, budgeting tips, audience engagement, reward suggestions, and duration advice

Real-time Q&A chat with Laila for personalized assistance on any campaign or general query

Clean and intuitive GUI with campaign summary and developer credits

This project blends AI interaction, business strategy, and Python-based UI design into a user-friendly tool for anyone looking to launch a successful crowdfunding campaign.


## Run Locally

Clone the project

```bash
  git clone https://github.com/harshchauhan01/Crowdfunding-Campaign-AI-Advisor-
```

Go to the project directory

```bash
  cd <my-project-directory>
```

Install dependencies

```bash
  python -m venv venv
  venv\Scripts\activate
  pip install huggingface_hub
  pip install streamlit transformers torch
  
```

Start the server

```bash
  streamlit run crowdfunding_advisor.py
```

