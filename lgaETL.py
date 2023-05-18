# A mount point that has already been mount does not require to my mounted again, but in the chance that it is required the follow code would be run:

# dbutils.fs.mount( source = "wasbs://inputdestination@lgastatsstorage.blob.core.windows.net", mount_point = "/mnt/lgastats", extra_configs = {'SAS key'})

%pip install openpyxl
%pip install fsspec
%pip install xlrd


from pathlib import Path 
import pandas as pd

# DIRECTORIES AND PATHS TO RELEVANT FILES
# Since the ABS_data and BOCSAR_data directory consists of several files, the script will be using a path to the file's parent folder.
abs_dir = Path.cwd() / '/dbfs/mnt/lgastats/ABS_data/'
bocsar_dir = Path.cwd() / '/dbfs/mnt/lgastats/BOCSAR_data'
benefits_path = '/dbfs/mnt/lgastats/DATAGOV_data/dss-payments-2020-lga-jun-2021-to-dec-2022-historic.csv' 
emp_path = '/dbfs/mnt/lgastats/NSC_data/SALM Smoothed LGA Datafiles (ASGS 2022) - June quarter 2022.xlsx'
indexes_path = '/dbfs/mnt/lgastats/ABS_indexdata/LGA indexes.xls'

# INITIALISING PANDAS DATAFRAMES
# Since the data will be coming from several sources, DataFrames are intialised as the final destination point for the transformed data to be collated.
e_income_data = pd.DataFrame(columns=['MedianIncome'])
e_income_ids = pd.DataFrame(columns=['EIncomeId'])

pop_data = pd.DataFrame(columns=['EstimatePop', 'IndigenousPop'])
pop_ids = pd.DataFrame(columns=['PopulationId'])

emp_df = pd.DataFrame(columns=['UnemploymentId', 'AvgRate'])

indexes_data = pd.DataFrame(columns=['IndexId'])

gender_data = pd.DataFrame(columns=['Male', 'Female'])
gender_ids = pd.DataFrame(columns=['GenderId'])

age_data = pd.DataFrame(columns=['Under18', 'YoungAdult', 'Adult', 'OlderAdult'])
age_ids = pd.DataFrame(columns=['AgeId'])

ab_data = pd.DataFrame(columns=['Aboriginal', 'NonAboriginal'])
ab_ids = pd.DataFrame(columns=['AboriginalityId'])

time_data = pd.DataFrame(columns=['Morning', 'Afternoon', 'Evening', 'Night'])
time_ids = pd.DataFrame(columns=['TimeId'])

month_data = pd.DataFrame(columns=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
month_ids = pd.DataFrame(columns=['MonthId'])

income_data = pd.DataFrame(columns=['IncomeId'])

offender_data = pd.DataFrame(columns=['OffenderId'])

offence_no = pd.DataFrame(columns=['IncidentNo'])
offence_data = pd.DataFrame(columns=['OffenceId'])

lga_no = pd.DataFrame(columns=['LgaNo'])
lga_df = pd.DataFrame(columns=['LgaId'])

# UNLOAD ADLS AND EXTRACT DESIRED FILES/WORKSHEETS
# load files from ABS directory into DataFrames
for path in list(abs_dir.rglob('*.xlsx*')):
    # extract lga code
    filename = path.name
    filename = filename.replace('.xlsx', '')
    filename = filename.replace('LGA ', '')
    lga_no.loc[len(lga_no)] = filename
    e_income_ids.loc[len(e_income_ids), 'EIncomeId'] = filename + '0'
    pop_ids.loc[len(pop_ids), 'PopulationId'] = filename + '02'

    # extract median income data
    e_income_xlsx = pd.read_excel(path, 'INC')
    e_income_xlsx.set_index('INCOME (INCLUDING GOVERNMENT ALLOWANCES)', inplace=True)
    e_income_xlsx = e_income_xlsx.loc[['EQUIV_2'], ['Unnamed: 9']].transpose()
    e_income_xlsx = e_income_xlsx.rename(columns={'EQUIV_2': 'MedianIncome'})
    e_income_data = pd.concat([e_income_data, e_income_xlsx])

    # extract population data
    pop_xlsx = pd.read_excel(path, 'POP')
    pop_xlsx.set_index('POPULATION AND PEOPLE', inplace=True)
    pop_xlsx = pop_xlsx.loc[['ERP_P_20', 'CENSUS_34'], ['Unnamed: 9']].transpose()
    pop_xlsx = pop_xlsx.rename(columns={'ERP_P_20': 'EstimatePop', 'CENSUS_34': 'IndigenousPop'})
    pop_data = pd.concat([pop_data, pop_xlsx])

# extract benefits data
benefits_df = pd.read_csv(benefits_path)

# extract unemployment data
emp_xlsx = pd.read_excel(emp_path, 'Smoothed LGA unemployment rates')

# extract indexes data
indexes_df = pd.read_excel(indexes_path, 'Table 1')

# load files from BOCSAR directory into DataFrames 
for path in list(bocsar_dir.rglob('*.xlsx*')):
    # extract offence data
    offence_df = pd.read_excel(path, 'Summary of offences')
    offence_df = offence_df.iloc[6:70, [0, 10]].loc[~(offence_df['NSW Recorded Crime Statistics 2018 - 2022'] == 'Betting and gaming offences')].drop(offence_df.columns[0], axis=1).sum()
    offence_no.loc[len(offence_no)] = offence_df.iloc[0]

    # extract offender gender data
    offender_df = pd.read_excel(path, 'Offenders')
    gender_df = offender_df.iloc[[4, 11, 18], 2:].transpose()
    gender_df = gender_df.loc[~(gender_df[4] == 'Betting and gaming offences')].drop(gender_df.columns[0], axis=1).sum()
    gender_data.loc[len(gender_data)] = [gender_df.iloc[0], gender_df.iloc[1]]

    # extract offender age data
    age_df = offender_df.iloc[[4, 26, 27, 28, 29, 30], 2:].transpose()
    age_df = age_df.loc[~(age_df[4] == 'Betting and gaming offences')].drop(age_df.columns[0], axis=1).sum()
    age_data.loc[len(age_data)] = [age_df.iloc[0], age_df.iloc[[1, 2]].sum(), age_df.iloc[3], age_df.iloc[4]]

    # extract offender aboriginality data
    ab_df = pd.read_excel(path, 'Aboriginality')
    ab_df = ab_df.iloc[[4, 5, 6], 2:].transpose()
    ab_df = ab_df.loc[~(ab_df[4] == 'Betting and gaming offences')].drop(ab_df.columns[0], axis=1).astype(int).sum()
    ab_data.loc[len(ab_data)] = [ab_df.iloc[0], ab_df.iloc[1]]

    # extract time data
    time_df = pd.read_excel(path, 'Time')
    time_df = time_df.iloc[6:38].loc[~(time_df['NSW Recorded Crime Statistics 2022'] == 'Betting and gaming offences')].drop(time_df.columns[0], axis=1).sum()
    time_data.loc[len(time_data)] = [time_df.iloc[[0, 4, 8, 12, 16, 20, 24]].sum(), time_df.iloc[[1, 5, 9, 13, 17, 21, 25]].sum(), time_df.iloc[[2, 6, 10, 14, 18, 22, 26]].sum(), time_df.iloc[[3, 7, 11, 15, 19, 23, 27]].sum()]

    # extract month data
    month_df = pd.read_excel(path, 'Month')
    month_df = month_df.iloc[5:37].loc[~(month_df['NSW Recorded Crime Statistics 2022'] == 'Betting and gaming offences')].drop(month_df.columns[0], axis=1).sum()
    month_data.loc[len(month_data)] = [month_df.iloc[0], month_df.iloc[1], month_df.iloc[2], month_df.iloc[3], month_df.iloc[4], month_df.iloc[5], month_df.iloc[6], month_df.iloc[7], month_df.iloc[8], month_df.iloc[9], month_df.iloc[10], month_df.iloc[11]]

# TRANSFORM EXTRACTED DATA INTO THE CORRESPODING DESTINATION FORMAT
# transform lga codes
lga_codes = lga_no.astype(int).sort_values(by='LgaNo').reset_index(drop=True)
lga_df['LgaId'] = emp_xlsx.iloc[3:132, 1].reset_index(drop=True)
lga_df['LgaName'] = benefits.iloc[3:132, 0].reset_index(drop=True)
for row in range(len(lga_codes)):
    emp_df.loc[row, 'UnemploymentId'] = str(lga_codes.loc[row, 'LgaNo']) + '00'
    gender_ids.loc[row, 'GenderId'] = str(lga_codes.loc[row, 'LgaNo']) + '5'
    indexes_data.loc[row, 'IndexId'] = str(lga_codes.loc[row, 'LgaNo']) + '04'
    age_ids.loc[row, 'AgeId'] = str(lga_codes.loc[row, 'LgaNo']) + '4'
    ab_ids.loc[row, 'AboriginalityId'] = str(lga_codes.loc[row, 'LgaNo']) + '6'
    time_ids.loc[row, 'TimeId'] = str(lga_codes.loc[row, 'LgaNo']) + '7'
    month_ids.loc[row, 'MonthId'] = str(lga_codes.loc[row, 'LgaNo']) + '8'
    income_data.loc[row, 'IncomeId'] = str(lga_codes.loc[row, 'LgaNo']) + '01'
    offender_data.loc[row, 'OffenderId'] = str(lga_codes.loc[row, 'LgaNo']) + '456'
    offence_data.loc[row, 'OffenceId'] = str(lga_codes.loc[row, 'LgaNo']) + '03'

# transform median income data
e_income_data = e_income_data.reset_index(drop=True)
e_income_ids = e_income_ids.reset_index(drop=True)
e_income_data = pd.concat([e_income_ids, e_income_data], axis=1)
e_income_data = e_income_data.astype(int).sort_values(by='EIncomeId')
e_income_data = e_income_data.reset_index(drop=True)

# transform population data
pop_data = pop_data.reset_index(drop=True)
pop_ids = pop_ids.reset_index(drop=True)
pop_data = pd.concat([pop_ids, pop_data], axis=1)
pop_data = pop_data.astype(int).sort_values(by='PopulationId')
pop_data = pop_data.reset_index(drop=True)

# transform benefits data
benefits_df['BenefitsId'] = benefits_df['LGA_code_2020'].astype(str) + '1'
benefits_df['YouthAllowance'] = benefits_df["Youth Allowance (other)"] +benefits_df["Youth Allowance (student and apprentice)"]
benefits_df = benefits_df.iloc[0:129, [26, 14, 15, 16, 27]]
benefits_df = benefits_df.rename(columns={'Health Care Card': 'HealthCareCard', 'JobSeeker Payment': 'JobSeekerPayment', 'Low Income Card': 'LowIncomeCard'})
benefits_df = benefits_df.astype(int).sort_values(by='BenefitsId')
benefits_df = benefits_df.reset_index(drop=True)

# transform unemployment data
emp_xlsx = emp_xlsx.iloc[3:132]
emp_xlsx['AvgRate'] = (emp_xlsx['Unnamed: 47'] + emp_xlsx['Unnamed: 48'])
emp_xlsx['AvgRate'] = emp_xlsx['AvgRate'].div(2).astype(float).round(2)
emp_df['AvgRate'] = emp_xlsx['AvgRate'].reset_index(drop=True)

# transform indexes data
indexes_df = indexes_df.iloc[5:134].drop(indexes_df.columns[[0, 1, 3, 5, 7, 9, 10]], axis=1)
indexes_df = indexes_df.rename(columns={'Unnamed: 2': 'SEDis', 'Unnamed: 4': 'SEDisAdv', 'Unnamed: 6': 'EcoResources', 'Unnamed: 8': 'EduOccupation'}).reset_index(drop=True)
indexes_data = pd.concat([indexes_data, indexes_df], axis=1)

# transform offence data
# collate offender gender data
gender_data['GenderId'] = gender_ids
gender_data = gender_data[['GenderId', 'Male', 'Female']]
# collate offender age data
age_data['AgeId'] = age_ids
age_data = age_data[['AgeId', 'Under18', 'YoungAdult', 'Adult', 'OlderAdult']]
# collate aboriginality data
ab_data['AboriginalityId'] = ab_ids
ab_data = ab_data[['AboriginalityId', 'Aboriginal', 'NonAboriginal']]
# collate offence time data
time_data['TimeId'] = time_ids
time_data = time_data[['TimeId', 'Morning', 'Afternoon', 'Evening', 'Night']]
# collate offence month data
month_data['MonthId'] = month_ids
month_data = month_data[['MonthId', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]
# create offender table
offender_data['GenderId'] = gender_data['GenderId']
offender_data['AgeId'] = age_data['AgeId']
# create offence table
offence_data['IncidentNo'] = offence_no
offence_data['MonthId'] = month_data['MonthId']
offence_data['TimeId'] = time_data['TimeId']
offence_data['OffenderId'] = offender_data['OffenderId']
offence_data['AboriginalityId'] = ab_data['AboriginalityId']

# transform income data
income_data['BenefitsId'] = benefits_df['BenefitsId']
income_data['EIncomeId'] = e_income_data['EIncomeId']

#create table per lga
lga_df['OffenceId'] = offence_data['OffenceId']
lga_df['IncomeId'] = income_data['IncomeId']
lga_df['IndexId'] = indexes_data['IndexId']
lga_df['PopulationId'] = pop_data['PopulationId']
lga_df['UnemploymentId'] = emp_df['UnemploymentId']

# SAVE THE PROCESSED DATA IN ADLS
#write transformed data into csv files, overwrite remaining files
e_income_data.to_csv('/dbfs/mnt/lgastats/db_out/EIncomeT.csv', index=False, header=True)
pop_data.to_csv('/dbfs/mnt/lgastats/db_out/PopulationT.csv', index=False, header=True)
benefits_df.to_csv('/dbfs/mnt/lgastats/db_out/BenefitsT.csv', index=False, header=True)
emp_df.to_csv('/dbfs/mnt/lgastats/db_out/UnemploymentT.csv', index=False, header=True)
indexes_data.to_csv('/dbfs/mnt/lgastats/db_out/IndexesT.csv', index=False, header=True)
gender_data.to_csv('/dbfs/mnt/lgastats/db_out/GenderT.csv', index=False, header=True)
age_data.to_csv('/dbfs/mnt/lgastats/db_out/AgeRangeT.csv', index=False, header=True)
ab_data.to_csv('/dbfs/mnt/lgastats/db_out/AboriginalityT.csv', index=False, header=True)
time_data.to_csv('/dbfs/mnt/lgastats/db_out/TimeT.csv', index=False, header=True)
month_data.to_csv('/dbfs/mnt/lgastats/db_out/MonthT.csv', index=False, header=True)
offender_data.to_csv('/dbfs/mnt/lgastats/db_out/OffenderT.csv', index=False, header=True)
offence_data.to_csv('/dbfs/mnt/lgastats/db_out/OffenceT.csv', index=False, header=True)
income_data.to_csv('/dbfs/mnt/lgastats/db_out/IncomeT.csv', index=False, header=True)
lga_df.to_csv('/dbfs/mnt/lgastats/db_out/LgaT.csv', index=False, header=True)