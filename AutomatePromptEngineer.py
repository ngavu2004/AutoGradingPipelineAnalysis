from langchain import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
import requests
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import re
import threading
import os
import csv
import logging
import pandas as pd

# Class that take in a file path and grading prompts and criterias to grade the file
class SubmissionGrader():
    def __init__(self,file_path,grading_prompts,grading_criterias):
        self.file_path = file_path
        self.sections = ["Description", "Overview", "Timeline","Scope","Team"]
        self.grading_prompts = grading_prompts
        self.grading_criterias = grading_criterias
        self.content_dict = {}
        self.extract_dictionary_from_text_file(self.file_path)

    def generatePrompt(self, section, criteria):
        prompt = self.grading_prompts.format(
            criteria=criteria,
            section=section,
            input=self.content_dict[section]
            )
        return prompt

    def extract_dictionary_from_text_file(self, file_path):
        section_dict = {}
        text = open(file_path, 'r').read()
        target_sections = ["Description", "Overview", "Timeline", "Scope", "Team"]
        pattern = r'(' + '|'.join(re.escape(name) for name in target_sections) + '):'

        # Find all the section headers and split the text accordingly
        sections = re.split(pattern, text)

        # The first element in sections is either empty or non-useful text before the first header
        sections = sections[1:]  # Skip the first element as it would be empty or non-section text

        # Creating a dictionary to store the section names and their corresponding content

        # Iterate over the list in pairs: section name and its corresponding text
        for i in range(0, len(sections), 2):
            section_name = sections[i].strip()  # Section name (e.g., 'Description')
            section_content = sections[i+1].strip()  # Corresponding content

            if section_name in target_sections:  # Only add the section if it's in the predefined list
                section_dict[section_name] = section_content
        self.content_dict = section_dict
        return section_dict
    
    def get_score(self,prompt):
        url = "http://localhost:11434/api/chat"
        # The JSON data that would be sent in the POST request
        data = {
            "model": "llama3",
            "messages": [
                { "role": "user", "content": prompt }
            ],
            "stream": False
        }
        # Send the POST request
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON response
            print(response.json()["message"]["content"])
            pattern = r"Grade:\s*([A-Za-z0-9\+]+)\s*(.*)"
            match = re.search(pattern, response.json()["message"]["content"])
            return [match.group(1),match.group(2)]
            
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "-1"
        
    def get_prompts_for_all_section(self):
        # Generate prompts for all sections and criteria, and return the results in a DataFrame
        print(f"\nGenerating prompts for {self.file_path}...")
        prompts_df = {
            "filename": [],
            "Section": [],
            "Criteria": [],
            "Prompt": []
        }
        prompts_df = pd.DataFrame(prompts_df)
        for section in self.sections:
            for criteria in self.grading_criterias[section]:
                prompt = self.generatePrompt(section, criteria)
                prompts_df.loc[len(prompts_df.index)] = [self.file_path, section, criteria, prompt]
        print(f"Finished generating prompts for {self.file_path}.")
        return prompts_df
        
    def get_scores_for_all_section(self):
        print(f"\nStart grading for {self.file_path}...")
        # self.extract_dictionary_from_text_file(self.file_path)
        result_df = {
            "filename": [],
            "AI_Grade": [],
            "Comment": [],
            "Section": [],
            "Criteria": []
        }
        result_df = pd.DataFrame(result_df)
        for section in self.sections:
            for criteria in self.grading_criterias[section]:
                prompt = self.generatePrompt(section,criteria)
                [score,comment] = self.get_score(prompt)
                result_df.loc[len(result_df.index)] = [self.file_path,score,comment,section,criteria]
        print(f"Finished grading {self.file_path}.")
        return result_df 

# Class that take in a folder path and grading prompts and criterias to grade all the files in the folder
class FolderProcessor():
    def __init__(self, folder_path, grading_prompts, grading_criterias, prompt_version, criteria_version):
        self.folder_path = folder_path
        self.grading_prompts = grading_prompts
        self.grading_criterias = grading_criterias
        self.prompt_version = prompt_version
        self.criteria_version = criteria_version
        self.submission_results = []
        self.error_files = []

        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def grade_files_in_folder(self):
        # Get list of files in the folder
        files_list = [os.path.join(self.folder_path, file) for file in os.listdir(self.folder_path) if file.endswith('.txt')]

        # Process each file in the files list
        for file_path in files_list:
            try:
                # Initialize the SubmissionGrader
                submission = SubmissionGrader(
                    file_path=file_path,
                    grading_prompts=self.grading_prompts,
                    grading_criterias=self.grading_criterias
                )

                # Get scores for all sections
                submission_result = submission.get_scores_for_all_section()
                self.submission_results.append(submission_result)
                

                # Log progress
                logging.info(f"Finished {len(self.submission_results)} / {len(files_list)}")
            except Exception as e:
                # Log the error and add the file to the error list
                logging.error(f"Error processing file {file_path}: {e}")
                self.error_files.append(file_path)

        # Log the list of error files
        self.log_error_files()
        submission_result_df = self.get_concatenated_results()
        self.export_to_csv(submission_result_df)
        return submission_result_df
    
    def log_error_files(self):
        logging.info("Error files: ")
        logging.info(self.error_files)

    def get_concatenated_results(self):
        if self.submission_results:
            submission_results_df = pd.concat(self.submission_results, axis=0)
            return submission_results_df
        else:
            logging.warning("No submission results to concatenate.")
            return pd.DataFrame()

    def export_to_csv(self, df):
        file_name = f"submission_results_prompt_v{self.prompt_version}_criteria_v{self.criteria_version}.csv"
        df.to_csv(file_name, index=False)
        logging.info(f"Exported results to {file_name}")

#  Class that take in a file including feedback to input and generate the real grade dataframe with format as the rubric prompts and criterias
class FeedbackProcessor():
    def __init__(self,inputfile_folder_path,real_comment_file_path,rubric_prompts,rubric_criteria):
        self.root_dir = inputfile_folder_path
        self.file_list = os.listdir(inputfile_folder_path),
        self.rubric_prompts = rubric_prompts,
        self.rubric_criteria = rubric_criteria,
        self.sections = ["Description", "Overview", "Timeline","Scope","Team"]
        self.rubric = pd.DataFrame({
            "filename": [],
            "Section": [],
            "Criteria": [],
            "Real_Grade": []
        }),
        self.real_comment_df = pd.read_csv(real_comment_file_path).fillna('None')
        self.comment_dict = dict(zip(self.real_comment_df['Filename'].tolist(),self.real_comment_df['Reson deduct points'].tolist()))

    def get_score(self,prompt):
        url = "http://localhost:11434/api/chat"
        # The JSON data that would be sent in the POST request
        data = {
            "model": "llama3",
            "messages": [
                { "role": "user", "content": prompt }
            ],
            "stream": False
        }
        # Send the POST request
        response = requests.post(url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the JSON response
            print(response.json()["message"]["content"])
            pattern = r"Grade:\s*([A-Za-z0-9\+]+)\s*(.*)"
            match = re.search(pattern, response.json()["message"]["content"])
            return [match.group(1),match.group(2)]
            
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "-1"
        
    def generatePrompt(self, section, criteria, comment):
        prompt = self.rubric_prompts.format(
            criteria=criteria,
            section=section,
            input=comment
            )
        # print(prompt)
        return prompt

    def get_y_test(self):
        for filename in self.file_list[0]:
            print(f"File name: {filename}")
            comment = self.comment_dict[filename]
            for section in self.sections:
                for criteria in self.rubric_criteria[0][section]:
                    current_prompt = self.generatePrompt(section,criteria,comment)
                    [score,comment] = self.get_score(current_prompt)
                    self.rubric[0].loc[len(self.rubric[0].index)] = [filename,section,criteria,score]
                    print(f"Finished {len(self.rubric[0].index)}/{len(self.file_list[0])}")
        print("Finished generating real grade.")
        return self.rubric[0]
    
