# ⚖️ Law Checker
This is the github repo for prototypes for humanity project

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Main Components](#main-components)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Installing & Running](#installing--running)
- [License](#license)

## Overview
Law Checker is an *AI-Powered* **Legal Assistant** for everyone to use. It provides simple answers to any question someone could have and also provides the sources to justify it's answer. For the AI interaction, we use OpenAI API with the gpt-4o LLM and Langchain.

## Features
- **United Nations:** It is trained with the United Nations Law
- **Greece:** It is trained with the Greek Law
- **User Interface:** Modern and Minimalistic User Interface

## Main Components
- **Backend (`backend/main.py`):** Sets up the FastAPI app.
- **Frontend (`frontend/src/App.js`):**: Landing page of the app.
- **Training Data (`data`):**: All the laws and practises.
- **Processes (`processes/data_hugging.py`):** Creates the *.faiss* and *.pkl* files to use with the AI.

## Setup and Installation
### Prerequisites
- **Python**
- **React**

### Installing & Running
1. **Clone the repository:**
   ```bash
   git clone git@github.com:gregalexan/prototypesforhumanity.git
   cd prototypesforhumanity
   ```
2. **Set up enviroment variables**  
    Create a .env file with your OpenAI API Key:
    ```
    OPENAI_API_KEY=
    ```

3. **Install the Requirements**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
5. **Run the Frontend**  
    Open a different terminal and run with this command:
    ```bash
    cd frontend
    npm install
    npm start
    ```
      
The application will be running at [http://localhost:3000](http://localhost:3000).

## License
This project is licensed under the terms and conditions of *Apache-2.0 License*.