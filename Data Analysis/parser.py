#-------------------------
# Import libs
#-------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#-------------------------
# Create vars & open file
#-------------------------

consent             : str  = "Yes, I agree"    # The exact answer that counts as giving consent
consent_given       : int  = 0                 # Counts people who agreed
no_consent          : int  = 0                 # Counts people who did not agree
kept_rows           : list = []                # Will hold only the rows of people who agreed

# Questions
CONSENT_STATEMENT = "Do you agree to participate?"
EMPLOYMENT_STATUS = "What is your current employment status?"
#-------------------------
# Subprograms
#-------------------------

def to_df(path, consent): # Read csv into table
    
    # keep_default_na=False stops pandas turning the text "N/A" into a missing value
    df = pd.read_csv(path, encoding="utf-8", keep_default_na=False)

    # Makes a True/False list (True if they consent)
    agreed = df[CONSENT_STATEMENT] == consent

    # Counts how many people did and didn't give consent
    consent_given = int(agreed.sum())
    no_consent    = int((~agreed).sum())

    # Keep rows of people who consent
    df = df[agreed]
    
    # Remove columns that are not needed
    df = df.drop(columns=["Submission ID", "Respondent ID", "Submitted at"])

    
    return df, consent_given, no_consent

# Creates different DFs
def employed_unemployed(df):

    # Seperate emplyed & unemployed datasets
    full_time_employed          = df[EMPLOYMENT_STATUS] == "Full-time employee"
    part_time_employed          = df[EMPLOYMENT_STATUS] == "Part-time employee"
    self_employed               = df[EMPLOYMENT_STATUS] == "Self-employed,"
    unemployed                  = df[EMPLOYMENT_STATUS] == "Unemployed and currently seeking work"
    students                    = df[EMPLOYMENT_STATUS] == "Student"
    retirees                    = df[EMPLOYMENT_STATUS] == "Retired"

    # Turn datasets into proper DataFrames
    df_full_time_employed   = df[full_time_employed]
    df_part_time_employed   = df[part_time_employed]
    df_self_employed        = df[self_employed]
    df_unemployed           = df[unemployed]
    df_students             = df[students]
    de_retirees             = df[retirees]

    pie_val = [len(df_full_time_employed), len(df_part_time_employed), len(df_self_employed), len(df_unemployed), len(df_students), len(de_retirees)]

    return df_full_time_employed, df_part_time_employed, df_self_employed, df_unemployed, df_students, de_retirees, pie_val

#-------------------------
# Main Program
#-------------------------

if __name__ == "__main__":
    file = "Data Analysis/data.csv" # Declare the file with data

    df, consent_given, no_consent                                 = to_df(file, consent) # Turns file into DataFrame
    df_full_time_employed, df_part_time_employed, df_self_employed, df_unemployed, df_students, de_retirees, pie_val = employed_unemployed(df) # Turn main DataFrame into seperate ones for (un)employed
    
    
    labels = ["Full time employed","Part time employed", "Self employed","Unemployed", "Students", "Retirees"]
    # Keep only categories with at least one respondent
    filtered = [(label, value) for label, value in zip(labels, pie_val) if value > 0]

    # Separate the labels and values
    filtered_labels = [item[0] for item in filtered]
    filtered_values = [item[1] for item in filtered]
    
    plt.figure(figsize=(6.5,6.5))
    plt.pie(filtered_values, labels=filtered_labels, autopct="%1.1f%%")
    plt.title("Employment status of respondents")
    plt.savefig("Data Analysis/Graphs/Fig1.png")
    plt.show()



#Note:
#  As this EPQ is intended for a non-specialist audience, I have included detailed comments throughout the code. 
#  These explain the purpose of each section, the reasoning behind key decisions, and how the different 
#  components of the program work. This is intended to make the implementation understandable to someone without specialist
#  programming knowledge and to demonstrate my understanding of the code and the development process.
