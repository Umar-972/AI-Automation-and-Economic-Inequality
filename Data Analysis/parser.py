#-------------------------
# Import libs
#-------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

#-------------------------
# Create vars & Qs as CONSTs
#-------------------------

consent                 = "Yes, I agree"    # The exact answer that counts as giving consent
consent_given           = 0                 # Counts people who agreed
no_consent              = 0                 # Counts people who did not agree
kept_rows               = []                # Will hold only the rows of people who agreed

CONSENT_STATEMENT       = "Do you agree to participate?"
AGE                     = "What is your age?"
EMPLOYMENT_STATUS       = "What is your current employment status?"
JOB                     = "Q3. What is your sector?"
UNEMPLOYMENT_LENGTH     = "Q3A. How long have you been unemployed?"
AI_UNEMPLOYMENT         = "Q3B. To what extent do you think AI or automation contributed to you becoming unemployed?"

AUTO_REPLACED           = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (My previous job was replaced by automation)"
SOME_AUTO_TASKS         = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (Some tasks in my previous job were automated, reducing the number of workers needed)"
AI_ADOPTIONS            = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (My previous employer adopted AI and reduced staffing)"
CHANGE_SKILLS           = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (AI changed the skills required for my previous job)"
REDUCE_OPPORTUNITY      = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (I believe AI reduced opportunities in my previous occupation)"
OTHER                   = "Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (Other)"
IDK_CONTRIBUTE          ="Q3C. If you think AI or automation contributed to your unemployment, how? Select all that apply. (I don't think AI or automation contributed)"

HIGHEST_EDUCATION       = "Q4. What is your highest level of education?"
EVER_USED_AI            = "Q5. Have you ever used generative AI for work?"
FREQUENCY_USE           = "Q6. How frequently do you use generative AI?"

CHATGPT                 = "Q7. Which generative AI tools have you used? Select all that apply. (ChatGPT)"
COPILOT                 = "Q7. Which generative AI tools have you used? Select all that apply. (Microsoft Copilot)"
GEMINI                  = "Q7. Which generative AI tools have you used? Select all that apply. (Google Gemini)"
CLAUDE                  = "Q7. Which generative AI tools have you used? Select all that apply. (Claude)"
PERPLEXITY              = "Q7. Which generative AI tools have you used? Select all that apply. (Perplexity)"
OTHER_AI                = "Q7. Which generative AI tools have you used? Select all that apply. (Other)"

WRITING                 = "Q8. What do you mainly use generative AI for? Select all that apply. (Writing/editing)"
RESEARCH                = "Q8. What do you mainly use generative AI for? Select all that apply. (Research/information gathering)"
DATA_ANALYSIS           = "Q8. What do you mainly use generative AI for? Select all that apply. (Data analysis)"
CODEING                 = "Q8. What do you mainly use generative AI for? Select all that apply. (Coding/programming)"
ADMINISTRATIVE          = "Q8. What do you mainly use generative AI for? Select all that apply. (Administrative tasks)"
COMMUNICATE             = "Q8. What do you mainly use generative AI for? Select all that apply. (Customer service/communication)"
CREATIVE                = "Q8. What do you mainly use generative AI for? Select all that apply. (Creative/design work)"
TRANSLATE               = "Q8. What do you mainly use generative AI for? Select all that apply. (Translation)"
PLANNING                = "Q8. What do you mainly use generative AI for? Select all that apply. (Planning/organisation)"
EDUCATION               = "Q8. What do you mainly use generative AI for? Select all that apply. (Learning/education)"
OTHER_USE               = "Q8. What do you mainly use generative AI for? Select all that apply. (Other)"

TIME_SAVING             = "Q9. Approximately how much time does generative AI save you each week?"
EMPLOYER_AI_KNOW        = "Q10. Does your current employer or organisation know that you use AI?"
AI_POLICY               = "Q11. Does your current employer or organisation have a policy regarding AI use?"
AI_CHANGED_TASKS        = "Q12. Has AI or automation changed the tasks you perform in your current work?"
PRODUCTIVITY            = "Q13. What effect has AI had on your productivity at work?"
REPLACEMENT_WORRY       = "Q14. How concerned are you that AI or automation could replace some or all of the tasks associated with your current or most recent job within the next 10 years?"
EFFECTS_OF_AI           = "Q15. What do you think the overall effect of AI and automation will be on employment over the next 10 years?"

LOW_SKILL               = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Low-skilled workers)"
MEDIUM_SKILL            = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Medium-skilled workers)"
HIGH_SKILL              = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Highly skilled workers)"
CLERICS                 = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Administrative/clerical workers)"
PROFESSIONAL            = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Professional workers)"
MANUAL                  = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Manual workers)"
CREATIVE_WORKERS        = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Creative workers)"
CUSTOMER_SERVICE        = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Customer service workers)"
MANAGERS                = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Managers)"
OTHER                   = "Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Other)"
IDK_DISPLACE            ="Q16. Which groups do you think are most likely to experience job displacement as a result of AI and automation? . (Don't know)"

WAGES_HIGH_SKILL        = "Q17. What effect do you think AI and automation will have on the wages of highly skilled workers over the next 10 years?"
WAGES_LOW_SKILL         = "Q18. What effect do you think AI and automation will have on the wages of low-skilled workers over the next 10 years?"
INEQUALITY              = "Q19. What overall effect do you think AI and automation will have on economic inequality in developed economies over the next 10–20 years?"

Δ_EMPLOYMENT            = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Changes in employment)"
Δ_WAGES                 = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Changes in wages)"
DIFF_EDU_SKILL          = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Differences in education and skills)"
ACCESS_TECH             = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Access to AI technology)"
PRODUCTIVITY_UP         = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Productivity increases)"
OWNERSHIP               = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Ownership of AI-related companies/capital)"
TAX_REDISTRIBUTE        = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Government taxation and redistribution)"
RETENTION_EDU           = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Education and retraining)"
NEW_JOBS                = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Creation of new industries and jobs)"
OTHER_INFULENCE         = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Other)"
IDK_INFULENCE           = "Q20. Which factors do you think will have the greatest influence on whether AI increases or decreases economic inequality? . (Don't know)"

EDUCATION_NEGATIVE      = "Q21. How important do you think education and retraining will be in reducing potential negative effects of AI on workers? 1 — Not at all important; 5 — Extremely important."
MOST_EFF_POLICY         = "Q22. Which policy do you think would be most effective at reducing potential inequality associated with AI?"
FAMILIARITY             = "Q23. Before completing this questionnaire, how familiar were you with the idea that AI could affect economic inequality?"

ALL_QUESTION_ARRAY      = [
    CONSENT_STATEMENT, AGE, EMPLOYMENT_STATUS, JOB, UNEMPLOYMENT_LENGTH, AI_UNEMPLOYMENT, AUTO_REPLACED, 
    SOME_AUTO_TASKS, AI_ADOPTIONS, CHANGE_SKILLS, REDUCE_OPPORTUNITY, OTHER, IDK_CONTRIBUTE, HIGHEST_EDUCATION, 
    EVER_USED_AI, FREQUENCY_USE, CHATGPT, COPILOT, GEMINI, CLAUDE, PERPLEXITY, OTHER_AI,
    WRITING, RESEARCH, DATA_ANALYSIS, CODEING, ADMINISTRATIVE, COMMUNICATE, CREATIVE, TRANSLATE, PLANNING, EDUCATION, OTHER_USE,
    LOW_SKILL, MEDIUM_SKILL, HIGH_SKILL, CLERICS, PROFESSIONAL, MANUAL, CREATIVE_WORKERS, CUSTOMER_SERVICE, MANAGERS, OTHER, IDK_DISPLACE,
    WAGES_HIGH_SKILL, WAGES_LOW_SKILL, INEQUALITY, Δ_EMPLOYMENT, Δ_WAGES, DIFF_EDU_SKILL, ACCESS_TECH, PRODUCTIVITY_UP, 
    OWNERSHIP, TAX_REDISTRIBUTE, RETENTION_EDU, NEW_JOBS, OTHER_INFULENCE, IDK_INFULENCE, EDUCATION_NEGATIVE, MOST_EFF_POLICY, FAMILIARITY
]

#-------------------------
# Subprograms
#-------------------------

def to_df(path, consent): # Read csv into table 
    df = pd.read_csv(path, encoding="utf-8", keep_default_na=False)

    # Make True/False list 
    agreed = df[CONSENT_STATEMENT] == consent
    consent_given = int(agreed.sum())
    no_consent    = int((~agreed).sum())

    # Keep rows of people who consent
    df = df[agreed]
    
    # Remove columns that are not needed
    df = df.drop(columns=["Submission ID", "Respondent ID", "Submitted at"])

    return df, consent_given, no_consent

def seperate_dfs(df): # Creates different DFs 
    
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

def question_index(questions, path) -> dict: # {Question : Index of Question}
    ALL_QUESTION_DICT = {}
    
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        
    for question in questions:
        # FIXED: check if question is in the CSV's 'header', not 'questions'
        if question in header:
            index_num = header.index(question)
            ALL_QUESTION_DICT[question] = index_num

    return ALL_QUESTION_DICT

#-------------------------
# Main Program
#-------------------------

if __name__ == "__main__":
    file = "Data Analysis/data.csv" # Declare data file

    df, consent_given, no_consent = to_df(file, consent) # Turns file into DataFrame
    df_full_time_employed, df_part_time_employed, df_self_employed, df_unemployed, df_students, de_retirees, pie_val = seperate_dfs(df) # Seperate main DataFrame  
    ALL_QUESTION_DICT   = question_index(ALL_QUESTION_ARRAY, file)
    
    df_tech             = df[df[JOB] == "Technology or IT"]
    df_retail_hos       = df[df[JOB] == "Retail or hospitality"]
    df_proff            = df[df[JOB] == "Professional or business services"]
    df_education        = df[df[JOB] == "Education"]
    df_manufactoring    = df[df[JOB] == "Manufacturing"]
    df_other            = df[df[JOB] == "Other"]
    df_logicstics       = df[df[JOB] == "Transport or logistics"]
    df_healthcare       = df[df[JOB] == "Healthcare or social care"]
    df_finance          = df[df[JOB] == "Finance, insurance or banking"]
    df_public_admin     = df[df[JOB] == "Public administration"]
    df_media            = df[df[JOB] == "Media or creative industries"]
    df_agriculture      = df[df[JOB] == "Agriculture, forestry or fishing"]
    df_construction     = df[df[JOB] == "Construction"]
    
    
    # # Quantity of all students that use AI
    # students_used_AI  = (df_students[EVER_USED_AI] == "Yes").sum()
    # print(f"Percentage of all students that use AI: {students_used_AI/len(df_students)*100:.1f}% out of {len(df_students)}")
    
    # # Quantity of GCSE students that use AI
    # GCSE_students     = df_students[df_students[HIGHEST_EDUCATION] == "GCSE/equivalent or below"]
    # GCSE_AI           = GCSE_students[GCSE_students[EVER_USED_AI] == "Yes"]
    # percentage_GCSE   = len(GCSE_AI) / len(GCSE_students) * 100
    # print(f"Percentage of students (with highest education at GCSE or below) that use AI: {percentage_GCSE:.1f}%, from a total of {len(GCSE_students)}")

    # # Quantity of A Level students that use AI
    # AL_students       = df_students[df_students[HIGHEST_EDUCATION] == "A-level/equivalent"]
    # AL_AI             = AL_students[AL_students[EVER_USED_AI] == "Yes"]
    # percentage_AL     = len(AL_AI) / len(AL_students) * 100
    # print(f"Percentage of students (with highest education at A Level) that use AI: {percentage_AL:.1f}%, from a total of {len(AL_students)}")

    # # Quantity of Undergraduate degree students that use AI
    # Under_students    = df_students[df_students[HIGHEST_EDUCATION] == "Undergraduate degree"]
    # Under_AI          = Under_students[Under_students[EVER_USED_AI] == "Yes"]
    # percentage_Under  = len(Under_AI) / len(Under_students) * 100
    # print(f"Percentage of students (with highest education at an Undergraduate degree) that use AI: {percentage_Under:.1f}%, from a total of {len(Under_students)}")

    # # Quantity of Postgraduate degree students that use AI
    # Post_students     = df_students[df_students[HIGHEST_EDUCATION] == "Postgraduate degree"]
    # Post_AI           = Post_students[Post_students[EVER_USED_AI] == "Yes"]
    # percentage_Post   = len(Post_AI) / len(Post_students) * 100
    # print(f"Percentage of students (with highest education at a Postgraduate degree) that use AI: {percentage_Post:.1f}%, from a total of {len(Post_students)}")

    # # Under 18 that use AI
    # U18               = df[df[AGE] == "Under 18"]
    # U18_AI            = U18[U18[EVER_USED_AI] == "Yes"]
    # percentage_U18    = len(U18_AI) / len(U18) * 100
    # U18_Daily         = U18[U18[FREQUENCY_USE] == "Daily"]
    # U18_Daily_per     = len(U18_Daily) / len(U18) * 100
    # print(f"Percentage of under 18s that have used AI: {percentage_U18:.1f}%, from a total of {len(U18)} with {U18_Daily_per:.1f}% using AI daily")
    
    # # 18-24 that use AI
    # _18_24             = df[df[AGE] == "18–24"]
    # _18_24_AI          = _18_24[_18_24[EVER_USED_AI] == "Yes"]
    # percentage_18_24   = len(_18_24_AI) / len(_18_24) * 100
    # _18_24_Daily       = _18_24[_18_24[FREQUENCY_USE] == "Daily"]
    # _18_24_Daily_per   = len(_18_24_Daily) / len(_18_24) * 100
    # print(f"Percentage of people aged 18 to 24 that have used AI: {percentage_18_24:.1f}%, from a total of {len(_18_24)} with {_18_24_Daily_per:.1f}% using AI daily")
    
    # # 25-34
    # _25_34             = df[df[AGE] == "25–34"]
    # _25_34_AI          = _25_34[_25_34[EVER_USED_AI] == "Yes"]
    # percentage_25_34   = len(_25_34_AI) / len(_25_34) * 100
    # _25_34_Daily       = _25_34[_25_34[FREQUENCY_USE] == "Daily"]
    # _25_34_Daily_per   = len(_25_34_Daily) / len(_25_34) * 100
    # print(f"Percentage of people aged 25 to 34 that have used AI: {percentage_25_34:.1f}%, from a total of {len(_25_34)} with {_25_34_Daily_per:.1f}% using AI daily")





# Note:
#  As this EPQ is intended for a non-specialist audience, I have included detailed comments throughout the code. 
#  These explain the purpose of each section, the reasoning behind key decisions, and how the different 
#  components of the program work. This is intended to make the implementation understandable to someone without specialist
#  programming knowledge and to demonstrate my understanding of the code and the development process.
#
#  This note is included because leaving a lot of comments can indicate that the program has been 'vibe-coded',
#  meaning it has been produced by an LLM/AI