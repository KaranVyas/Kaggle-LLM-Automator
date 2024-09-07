import kaggle
import subprocess
import os
import webbrowser
import zipfile
import openai  # OpenAI SDK should be updated to the latest version
import pandas as pd

# Add your OpenAI API key here
openai.api_key = # API KEY

def list_competitions():
    """
    List active Kaggle competitions using Kaggle API.
    Returns a list of competition objects.
    """
    competitions = kaggle.api.competitions_list()
    return competitions

def display_competition_titles(competitions):
    """
    Display the title of all available competitions to help the user select a valid competition.
    """
    print("Available Competitions:")
    for idx, comp in enumerate(competitions):
        print(f"{idx+1}. {comp.title} (Keyword: {comp.ref})")
    print("\nPlease use the keyword from the list above to select a competition.")

def select_competition(competitions, keyword=None):
    """
    Select a competition based on user-input keyword.
    """
    selected = [comp for comp in competitions if keyword.lower() in comp.ref.lower()]
    return selected[0] if selected else None

def check_registration(competition_url):
    """
    Check if the user is registered for the competition.
    If not, open the registration page in a browser.
    """
    print(f"Opening competition page: {competition_url}")
    webbrowser.open(competition_url)
    print("Please ensure you are registered for the competition.")

def extract_competition_id(competition_url):
    """
    Extract the competition ID from the full URL.
    For example: https://www.kaggle.com/competitions/connectx -> connectx
    """
    return competition_url.split('/')[-1]

def download_dataset_cli(competition_name, download_path="datasets"):
    """
    Run Kaggle CLI command to download dataset using the entered competition name.
    """
    # Create a subdirectory for the competition
    competition_path = os.path.join(download_path, competition_name)
    if not os.path.exists(competition_path):
        os.makedirs(competition_path)

    # Build the Kaggle CLI command dynamically
    cli_command = f"kaggle competitions download -c {competition_name} -p {competition_path}"

    # Execute the CLI command using subprocess
    try:
        result = subprocess.run(cli_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        print(f"Dataset downloaded for competition: {competition_name}")

        # Extract the downloaded files into the competition folder
        extract_downloaded_files(competition_path)

    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset using CLI: {e.stderr.decode('utf-8')}")
        print(f"CLI Command: {cli_command}")

def extract_downloaded_files(extract_to_path):
    """
    Extract all zip files in the competition directory.
    """
    for item in os.listdir(extract_to_path):
        if item.endswith(".zip"):
            file_path = os.path.join(extract_to_path, item)
            print(f"Extracting {file_path}...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_path)
            print(f"Extracted {file_path}")
            os.remove(file_path)  # Remove the zip file after extraction

def generate_code_with_openai(dataset_path):
    """
    Use OpenAI's API to generate a Python script for the competition's dataset.
    """
    # Load the dataset into a pandas DataFrame
    data = pd.read_csv(dataset_path)

    # Analyze the dataset columns and create a prompt for OpenAI
    column_names = ', '.join(data.columns)
    
    # Modify the prompt to ensure OpenAI returns only code and uses the correct dataset path
    prompt = f"""
    Write only the Python code that builds a machine learning model to predict the target based on the dataset with columns: {column_names}. 
    Use the dataset located at '{dataset_path}', and ensure the model predicts the target for the test data. 
    Before training the model, preprocess the dataset by handling any categorical variables using one-hot encoding or label encoding.
    Save the predictions in a CSV file named 'submission.csv' at {dataset_path}. 
    The CSV should contain the same format that the submission file has located at {dataset_path}. 
    Do not include explanations or comments, only provide the code. Ensure that the file 'submission.csv' is saved in the correct format.
    """

    # Call OpenAI API for code generation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-3.5-turbo" or other available models
        messages=[
            {"role": "system", "content": "You are a helpful assistant that outputs Python code only."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.5
    )

    generated_code = response['choices'][0]['message']['content']

    # Clean the generated code by removing markdown syntax
    cleaned_code = generated_code.replace("```python", "").replace("```", "").strip()

    # Save the cleaned code to a Python file
    with open("generated_model.py", "w") as file:
        file.write(cleaned_code)
    
    print("Model code generated using OpenAI and saved to 'generated_model.py'")

    # Optionally, run the cleaned model code (you may want to validate the code first)
    exec(cleaned_code)



def submit_to_kaggle(competition_name, submission_file_path):
    """
    Submit the generated predictions to Kaggle competition.
    """
    # Make sure the file exists
    if os.path.exists(submission_file_path):
        try:
            kaggle.api.competition_submit(submission_file_path, "Generated Submission", competition_name)
            print(f"Successfully submitted {submission_file_path} to {competition_name}")
        except Exception as e:
            print(f"Error submitting to Kaggle: {e}")
    else:
        print(f"Submission file not found at {submission_file_path}")

if __name__ == "__main__":
    # Step 1: List all competitions
    competitions = list_competitions()
    
    # Step 2: Display competition titles to help the user choose a competition
    display_competition_titles(competitions)
    
    # Step 3: Get user input for competition keyword
    competition_keyword = input("Enter the competition keyword (as shown above): ").strip()
    
    # Step 4: Select the competition based on the input keyword
    selected_comp = select_competition(competitions, keyword=competition_keyword)
    
    if selected_comp:
        print(f"Selected Competition: {selected_comp.title}")
        
        # Step 5: Check if user is registered for the competition
        check_registration(f"{selected_comp.ref}")
        
        input("Press Enter after registering to continue...")  # Pause for registration
        
        # Step 6: Extract the competition ID from the URL
        competition_id = extract_competition_id(selected_comp.ref)
        
        # Step 7: Download the dataset using CLI command and extract the zip files into a folder named after the competition
        download_dataset_cli(competition_id)

        # Step 8: Generate a Python script using OpenAI's API and save it
        dataset_path = f"datasets/{competition_id}/train.csv"  # Example path to training data
        generate_code_with_openai(dataset_path)

        # Step 9: Submit the predictions to Kaggle
        submission_file_path = f"datasets/{competition_id}/submission.csv"  # Assuming generated submission file path
        submit_to_kaggle(competition_id, submission_file_path)
    else:
        print("No matching competition found. Please make sure the keyword is correct.")
