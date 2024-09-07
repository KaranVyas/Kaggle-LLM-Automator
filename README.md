# Kaggle-LLM-Automator
# Kaggle Competition Automator using OpenAI

This project automates the process of downloading Kaggle competition datasets, generating a machine learning model using OpenAI, and submitting predictions to Kaggle. The project is designed to streamline the workflow of participating in Kaggle competitions by utilizing the Kaggle API and OpenAI's GPT models to automatically generate and execute machine learning code.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  
## Prerequisites

Before starting, ensure you have the following installed on your machine:

1. **Python 3.8+**
2. **Kaggle Account & API Key**
3. **OpenAI API Key**
4. **Kaggle CLI**
5. **A terminal or command-line tool**

## Installation

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/kaggle-automator.git
   cd kaggle-automator

2. **Set Up a Python Virtual Environment**
   It is recommended to create a virtual environment to manage dependencies:
   ```bash
   python -m venv kaggle-env
   source kaggle-env/bin/activate  # On Windows: kaggle-env\Scripts\activate

3. **Install Dependencies**  
   Install the necessary dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt

4. **Install `python-dotenv`**  
   Install `python-dotenv` to manage environment variables securely:
   ```bash
   pip install python-dotenv

5. **Install Kaggle CLI**  
   Install the Kaggle CLI tool to interact with the Kaggle platform:
   ```bash
   pip install kaggle

6. **Set Up Kaggle API Credentials**  
   - Download your Kaggle API credentials from [Kaggle](https://www.kaggle.com/account). Navigate to your account settings, scroll down to the API section, and click "Create New API Token." This will download a `kaggle.json` file.
   - Move this file to the appropriate location and set the permissions:
     ```bash
     mkdir ~/.kaggle
     mv ~/Downloads/kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json  # Secure the file
     ```

7. **Set Up OpenAI API Credentials**  
   - Create an `.env` file in the root directory of the project and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-openai-api-key-here
     ```

## Usage

1. **Run the Script**  
   Execute the `competition_agent.py` script to start the process:
   ```bash
   python competition_agent.py

2. **Select a Competition**  
   After running the script, a list of Kaggle competitions will be displayed. Select a competition by entering the corresponding keyword. For example:
   ```bash
   Enter the competition keyword (as shown above): titanic

3. **Download the Dataset**  
   The script will automatically download the dataset for the selected competition, extract it, and store it in the `datasets/` directory.

4. **Generate and Execute Model Code**  
   The script will generate a Python model using OpenAI's API based on the dataset's columns, handle missing values, and save predictions in `submission.csv`. This model will be stored in the `generated_model.py` file.

5. **Submit the Model to Kaggle**  
   The script will automatically submit the predictions to Kaggle:
   ```bash
   Successfully submitted submission.csv to titanic

