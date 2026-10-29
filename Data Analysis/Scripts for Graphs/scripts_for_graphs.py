#-------------------------
# Import libs
#-------------------------

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#-------------------------
# Create vars
#-------------------------

# Overall vars
employment_status   : list = ["Full-time employee", "Part-time employee", "Self-employed"]
unemployment_status : str  = "Unemployed"
student             : str  = "Student"
retired             : str  = "Retired"
consent             : str  = "Yes, I agree"    # The exact answer that counts as giving consent
EMPLOYMENT_STATUS = "What is your current employment status?"
#-------------------------
# Subprograms
#-------------------------

def failsafe() -> dict[str, Path]:
    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_DIR = BASE_DIR.parent
    DATA_DIR = BASE_DIR / "Data Files"

    files = {
        # Located in Data Analysis
        "data": PROJECT_DIR / "data.csv",
        "test": PROJECT_DIR / "test_data.csv",
        
        # Located in Scripts for Graphs / Data Files
        "annual": DATA_DIR / "Unemployment_rate_annual.csv",
        "quarterly": DATA_DIR / "Unemployment_rate_quarterly.csv",
        "monthly": DATA_DIR / "Unemployment_rate_annual.csv",
        "historical": DATA_DIR / "UNRTUKA.csv",
    }

    for name, file_path in files.items():
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Missing required file '{name}': {file_path}"
            )

    return files

def to_df(path, consent):

    # keep_default_na=False stops pandas turning the text "N/A" into a missing value
    df = pd.read_csv(path, encoding="utf-8", keep_default_na=False)

    # Makes a True/False list (True if they consent)
    agreed = df["Do you agree to participate?"] == consent

    # Counts how many people did and didn't give consent
    consent_given = int(agreed.sum())
    no_consent    = int((~agreed).sum())

    # Keep rows of people who consent
    df = df[agreed]
    
    # Remove columns that are not needed
    df = df.drop(columns=["Submission ID", "Respondent ID", "Submitted at"])

    
    return df, consent_given, no_consent

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

def parse_unemployed_csv_anual(unemployment_data_file):
    # Anual data lines 1-55
    df_unemployment_anual       = pd.read_csv(unemployment_data_file, header=None, nrows=55)

    years       = df_unemployment_anual[0].tolist()
    rates_anual = df_unemployment_anual[1].tolist()

    # final 5 years
    final_5_yr      = df_unemployment_anual.iloc[-5:, 0].astype(int).to_list()
    final_5_rates   = df_unemployment_anual.iloc[-5:, 1].to_list()

    return df_unemployment_anual, years, rates_anual, final_5_yr, final_5_rates

def parse_unemployed_csv_quarterly(unemployment_data_file):
    # Quarterly data lines 56-275
    df_unemployment_quarterly   = pd.read_csv(unemployment_data_file, header=None, nrows=220)

    quarters        = df_unemployment_quarterly[0].to_list()
    rates_quarterly = df_unemployment_quarterly[1].to_list()

    return df_unemployment_quarterly, quarters, rates_quarterly

def parse_unemployed_csv_monthly(unemployment_data_file):
    # Monthly data lines 278-936
    df_unemployment_monthly = pd.read_csv(unemployment_data_file,header=None, nrows=219)
    return df_unemployment_monthly

# Three industrial revolutions
# 1 = 1760 to 1840
# 2 = 1870 to 1914
# 3 = 1950 to 1970

def parse_UNRTUKA_first(file):
    df = pd.read_csv(file)

    # Convert to datetime objects
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")

    # Filter while they are actual dates
    df_1760_to_1840 = df[(df["observation_date"] >= "1760-01-01")& (df["observation_date"] <= "1840-01-01")].copy()  # .copy() prevents SettingWithCopyWarning
    
    years_60_40 = df_1760_to_1840["observation_date"].dt.year.tolist()
    rates_60_40 = df_1760_to_1840["UNRTUKA"].tolist()
        
    # Format to dd/mm/yyyy at end
    df_1760_to_1840["observation_date"] = df_1760_to_1840["observation_date"].dt.strftime("%d/%m/%Y")

    #print(df_1760_to_1840)
    return df_1760_to_1840, years_60_40, rates_60_40

def parse_UNRTUKA_second(file):
    # Second Industrial Revolution: 1870 to 1914
    df = pd.read_csv(file)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    
    # Filter dates between 1870 and 1914
    df_1870_to_1914 = df[(df["observation_date"] >= "1870-01-01") & (df["observation_date"] <= "1914-01-01")].copy()

    # Extract years and unemployment rates
    years_70_14 = df_1870_to_1914["observation_date"].dt.year.tolist()
    rates_70_14 = df_1870_to_1914["UNRTUKA"].tolist()

    # Format dates as dd/mm/yyyy after filtering
    df_1870_to_1914["observation_date"] = (df_1870_to_1914["observation_date"].dt.strftime("%d/%m/%Y"))

    return df_1870_to_1914, years_70_14, rates_70_14

def parse_UNRTUKA_third(file):
    df = pd.read_csv(file)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    
    df_1950_to_1970 = df[(df["observation_date"] >= "1950-01-01") & (df["observation_date"] <= "1970-01-01")].copy()

    years_50_70 = df_1950_to_1970["observation_date"].dt.year.tolist()
    rates_50_70 = df_1950_to_1970["UNRTUKA"].tolist()

    df_1950_to_1970["observation_date"] = (df_1950_to_1970["observation_date"].dt.strftime("%d/%m/%Y"))

    #print(df_1950_to_1970)

    return df_1950_to_1970, years_50_70, rates_50_70

#-------------------------
# Main Program
#-------------------------

if __name__ == "__main__":
    
    # Load file paths with failsafe func to ensure files are present and in correct position
    files = failsafe() # Validate paths before processing data
    
    # Load survey data
    df, consent_given, no_consent = to_df(files["data"], consent)

    # Separate respondents by employment status
    (df_full_time_employed, df_part_time_employed, df_self_employed, df_unemployed, df_students, de_retirees, pie_val) = employed_unemployed(df)

    # Load unemployment statistics
    (df_unemployment_anual, years, rates_anual, final_5_yr, final_5_rates) = parse_unemployed_csv_anual(files["annual"])
    (df_unemployment_quarterly, quarters, rates_quarterly,) = parse_unemployed_csv_quarterly(files["quarterly"])
    df_unemployment_monthly = (parse_unemployed_csv_monthly(files["monthly"]))

    # Load historical data
    (df_1760_to_1840, years_60_40, rates_60_40,) = parse_UNRTUKA_first(files["historical"])
    (df_1870_to_1914, years_70_14, rates_70_14,) = parse_UNRTUKA_second(files["historical"])
    (df_1950_to_1970, years_50_70, rates_50_70,) = parse_UNRTUKA_third(files["historical"])
   
    # Calculates Percentages for (un)employed stats
    if consent_given == 0:
        raise ValueError(
            "Cannot calculate respondent percentages: "
        "no valid consent responses were recorded."
    )

    #-------------------------
    # Show All Figures 
    #-------------------------

    # Fig1.png
    # labels = ["Full time employed","Part time employed", "Self employed","Unemployed", "Students", "Retirees"]
    
    # # Keep categories with at least one respondent
    # filtered = [(label, value) for label, value in zip(labels, pie_val) if value > 0]

    # # Separate labels & vals
    # filtered_labels = [item[0] for item in filtered]
    # filtered_values = [item[1] for item in filtered]
    
    # plt.figure(figsize=(7, 7))
    # plt.pie(filtered_values, labels=filtered_labels, autopct="%1.1f%%")
    # plt.title("Employment status of respondents")
    # plt.savefig("Data Analysis/Graphs/Fig1.png")
    # plt.show()

    # Fig2.png
    # plt.figure()
    # plt.plot(final_5_yr, final_5_rates, marker="o")
    # plt.title("Unemployment rates from 2020-2025")
    # plt.savefig("Data Analysis/Graphs/Fig2.png", dpi=300, bbox_inches="tight")
    # plt.show()
    # plt.close()

    # Fig3.png
    # plt.figure(figsize=(12, 6))
    # plt.plot(quarters, rates_quarterly)
    # plt.title("Unemployment from 1971-2025 Quarterly")
    # plt.xlabel("Year")
    # plt.ylabel("Unemployment rate (%)")
    # plt.xticks(range(0, len(quarters), 20), quarters[::20], rotation=45) # Show label every 5 years
    # plt.tight_layout()
    # plt.savefig("Data Analysis/Graphs/Fig3.png", dpi=300, bbox_inches="tight")
    # plt.show()
    # plt.close()
    
    # Fig4a.png
    # plt.figure(figsize=(12, 6))
    # plt.plot(years_60_40, rates_60_40)
    # plt.title("UK Unemployment Rates, 1760-1840 (First Industrial Revolution)")
    # plt.xlabel("Year")
    # plt.ylabel("Unemployment rate (%)")
    # plt.xticks(years_60_40[::4], rotation=45)
    # plt.tight_layout()
    # plt.savefig("Data Analysis/Graphs/Fig4a.png", dpi=300)
    # plt.show()
    # plt.close()
    
    # Fig4a.png
    # plt.figure(figsize=(12, 6))
    # plt.plot(years_50_70, rates_50_70, marker="o")
    # plt.title("UK Unemployment Rates, 1950-1970 (Third Industrial Revolution)")
    # plt.xlabel("Year")
    # plt.ylabel("Unemployment rate (%)")
    # plt.xticks(years_50_70[::2], rotation=45)
    # plt.tight_layout()
    # plt.savefig("Data Analysis/Graphs/Fig4.png", dpi=300, bbox_inches="tight")
    # plt.show()

    # # Fig4b.png
    # plt.figure(figsize=(12, 6))
    # plt.plot(years_70_14, rates_70_14, marker="o")
    # plt.title("UK Unemployment Rates, 1870-1914 (Second Industrial Revolution)")
    # plt.xlabel("Year")
    # plt.ylabel("Unemployment rate (%)")
    # plt.xticks(years_70_14[::2], rotation=45)
    # plt.tight_layout()
    # plt.savefig("Data Analysis/Graphs/Fig4b.png", dpi=300, bbox_inches="tight")
    # plt.show()
    # plt.close()
