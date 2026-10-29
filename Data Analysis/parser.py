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
CONSENT_STATEMENT   = "Do you agree to participate?"
AGE                 = "What is your age?"
EMPLOYMENT_STATUS   = "What is your current employment status?"
JOB                 = "Q3. What is your sector?"
UNEMPLOYMENT_LENGTH = "Q3A. How long have you been unemployed?"
AI_UNEMPLOYMENT     = "Q3B. To what extent do you think AI or automation contributed to you becoming unemployed?"
HOW_AI_REPLACED_YOU = ["Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (My previous job was replaced by automation)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (Some tasks in my previous job were automated, reducing the number of workers needed)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (My previous employer adopted AI and reduced staffing)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (AI changed the skills required for my previous job)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (I believe AI reduced opportunities in my previous occupation)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (Other)",
                       "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (I don't think AI or automation contributed)"]
HIGHEST_EDUCATION   = "Q4. What is your highest level of education?"
EVER_USED_AI        = "Q5. Have you ever used generative AI for work?"
FREQUENCY_USE       = "Q6. How frequently do you use generative AI?"
WHICH_AI            = ["Q7. Which generative AI tools have you used? Select all that apply. (ChatGPT)", "Q7. Which generative AI tools have you used? Select all that apply. (Microsoft Copilot)",
                       "Q7. Which generative AI tools have you used? Select all that apply. (Google Gemini)", "Q7. Which generative AI tools have you used? Select all that apply. (Claude)",
                       "Q7. Which generative AI tools have you used? Select all that apply. (Perplexity)", "Q7. Which generative AI tools have you used? Select all that apply. (Other)"]
WHAT_USAGE          = ["Q8. What do you mainly use generative AI for? Select all that apply. (Writing/editing)", "Q8. What do you mainly use generative AI for? Select all that apply. (Research/information gathering)",
                       "Q8. What do you mainly use generative AI for? Select all that apply. (Data analysis)", "Q8. What do you mainly use generative AI for? Select all that apply. (Coding/programming)",
                       "Q8. What do you mainly use generative AI for? Select all that apply. (Administrative tasks)", "Q8. What do you mainly use generative AI for? Select all that apply. (Customer service/communication)",
                       "Q8. What do you mainly use generative AI for? Select all that apply. (Creative/design work)", "Q8. What do you mainly use generative AI for? Select all that apply. (Translation)",
                       "Q8. What do you mainly use generative AI for? Select all that apply. (Planning/organisation)", "Q8. What do you mainly use generative AI for? Select all that apply. (Learning/education)",
                       "Q8. What do you mainly use generative AI for? Select all that apply. (Other)"]
TIME_SAVING         = "Q9. Approximately how much time does generative AI save you each week?"
EMPLOYER_AI_KNOW    = "Q10. Does your current employer or organisation know that you use AI?"
AI_POLICY           = "Q11. Does your current employer or organisation have a policy regarding AI use?"
AI_CHANGED_TASKS    = "Q12. Has AI or automation changed the tasks you perform in your current work?"
PRODUCTIVITY        = "Q13. What effect has AI had on your productivity at work?"
REPLACEMENT_WORRY   = "Q14. How concerned are you that AI or automation could replace some or all of the tasks associated with your current or most recent job within the next 10 years?"
EFFECTS_OF_AI       = "Q15. What do you think the overall effect of AI and automation will be on employment over the next 10 years?"
DISPLACE_GROUPS     = ["Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Low-skilled workers)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Medium-skilled workers)",
                       "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Highly skilled workers)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Administrative/clerical workers)",
                       "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Professional workers)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Manual workers)",
                       "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Creative workers)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Customer service workers)",
                       "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Managers)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Other)", "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Don't know)"]
WAGES_HIGH_SKILL    = "Q17. What effect do you think AI and automation will have on the wages of highly skilled workers over the next 10 years?"
WAGES_LOW_SKILL     = "Q18. What effect do you think AI and automation will have on the wages of low-skilled workers over the next 10 years?"
INEQUALITY          = "Q19. What overall effect do you think AI and automation will have on economic inequality in developed economies over the next 10–20 years?"
INFULENCE_INEQUALITY= ["Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Changes in employment)", "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Changes in wages)",
                       "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Differences in education and skills)", "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Access to AI technology)",
                       "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Productivity increases)", "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Ownership of AI-related companies/capital)",
                       "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Government taxation and redistribution)", "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Education and retraining)", 
                       "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Creation of new industries and jobs)", "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Other)",
                       "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Don't know)"]
EDUCATION_NEGATIVE  = "Q21. How important do you think education and retraining will be in reducing potential negative effects of AI on workers? 1 — Not at all important; 5 — Extremely important."
MOST_EFF_POLICY     = "Q22. Which policy do you think would be most effective at reducing potential inequality associated with AI?"
FAMILIARITY         = "Q23. Before completing this questionnaire, how familiar were you with the idea that AI could affect economic inequality?"

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
def seperate_dfs(df):

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
    file = "Data Analysis/data.csv" # Declare data file

    df, consent_given, no_consent                                 = to_df(file, consent) # Turns file into DataFrame
    df_full_time_employed, df_part_time_employed, df_self_employed, df_unemployed, df_students, de_retirees, pie_val = seperate_dfs(df) # Seperate main DataFrame  



#Note:
#  As this EPQ is intended for a non-specialist audience, I have included detailed comments throughout the code. 
#  These explain the purpose of each section, the reasoning behind key decisions, and how the different 
#  components of the program work. This is intended to make the implementation understandable to someone without specialist
#  programming knowledge and to demonstrate my understanding of the code and the development process.
#
# This note is included because leaving a lot of comments can indicate that the program has been 'vibe-coded'
# meaning it has been produced by an LLM/AI