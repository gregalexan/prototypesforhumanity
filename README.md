# ⚖️ Law Checker

This is the GitHub repository for the **Prototypes for Humanity** project.

## Table of Contents
- [Overview](#overview)
- [Take a Look](#take-a-look)
  - [Homepage](#homepage)
  - [Greek Law](#greek-law)
  - [United Nations](#united-nations)
  - [Find Lawyers](#find-lawyers)
- [Features](#features)
- [Main Components](#main-components)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Installing & Running](#installing--running)
- [License](#license)

## Overview
**Law Checker** is an *AI-powered legal assistant* designed to provide accurate, user-friendly legal guidance. It answers legal questions based on official sources and includes references to justify each answer. It leverages the OpenAI API (`gpt-4o`) combined with Langchain for AI interaction.

## Take a Look

### Homepage
![homepage](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/homepage.png)

### Greek Law
![greek-1](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/greek_1.png)
![greek-2](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/greek_2.png)

### United Nations
![un-1](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/un_1.png)
![un-2](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/un_2.png)

### Find Lawyers
![find-lawyers](https://github.com/gregalexan/prototypesforhumanity/blob/main/media/find_lawyers.png)

## Features
- 🇺🇳 **UN Law** — Trained on selected United Nations legal documents  
- 🇬🇷 **Greek Law** — Trained on official Greek legal codes and the Constitution  
- 💻 **User Interface** — Minimal and modern frontend using React

## Main Components
- **Backend (`backend/main.py`)** — FastAPI server that handles LLM queries  
- **Frontend (`frontend/src/App.js`)** — React interface for user interaction  
- **Training Data (`data/`)** — Text files containing Greek & international legal sources  
- **Processes (`processes/data_hugging.py`)** — Indexing script that generates FAISS vector stores

## Setup and Installation

### Prerequisites
- Python 3.9+
- Node.js & npm

### Installing & Running

1. **Clone the repository**
   ```bash
   git clone https://github.com/gregalexan/prototypesforhumanity.git
   cd prototypesforhumanity
   ```
   
2. **Create a `.env` file**  
   Add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Install Python Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

5. **Run the frontend**  
   Open a second terminal:
   ```bash
   cd frontend
   npm install
   npm start
   ```  

The application will be available at [http://localhost:3000](http://localhost:3000)

## License
This project is licensed under the *Apache 2.0 License*.
