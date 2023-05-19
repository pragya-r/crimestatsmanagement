# NSW Crime Statistics Management System
CSMS is a comprehensive platform in which users will have the ability to track and analyse crimes rates alongside socio-economic measures on an interactive dashboard.

To just view our application use this link: 
https://app.powerbi.com/reportEmbed?reportId=1c2afab0-996d-403e-aa97-7c59852f90ca&autoAuth=true&ctid=e8911c26-cf9f-4a9c-878e-527807be8791

## Prerequisites
This section will describe the prerequisites of running our Azure Data Factory pipelines, application, and surrounding services.
To view and edit our dashboard on Power Bi, you would need a windows computer and downlaod Mircorsoft Power BI. 
To view this application on a Mac uses the follwoing link below and you need to given permission, this link only allows for viewing purposes not eidting purposes.   
### Azure Data Factory
In order to run the pipelines, all files within the directory, **main_pipeline**, must be downloaded. The code will be uploaded onto Azure Powershell create the pipelines.

### SQL Database
An Azure SQL database is used as the final store. Table's within the database can be found under the directory, **sql_db**.

### Azure Databricks notebook
The code used in the databricks note book can be found in **lgaETL.py**.

### Power Bi
To import our report template and configure a connection to a SQL server, Power Bi desktop is required.

## Set-up
### Step 1
On Azure Powershell log into Azure account and select subscription. Replace "subscription name" with your choosen subscription.

Login-AzureRmAccount
Select-AzureRmSubscription -SubscriptionName "subscription name"

Next, upload the json files for the ADF pipelines (found in main_pipeline). Remember to rename "df name" to the name of your data factory, "RG name" to the name of your resource group, and "pipeline" to the name of your pipeline.

Set-AzureRmDataFactoryV2Pipeline -DataFactoryName "df name" -ResourceGroupName "RG name" -Name "pipelineName" -DefinitionFile "path to json file"

Following the same format, to upload the datasets use the command below.

Set-AzureRmDataFactoryV2Dataset 

Similarly, for the linked services, use the following command.

Set-AzureRmDataFactoryV2LinkedService

### Step 2
For the systems database, run the query sql_db.sql, to create the tables. 


### Step 3
Download the Power Bi template  LGAStatsTemplate.final.pbit. In Power Bi desktop, go to File --> Import --> Power Bi Template -->  LGAStatsTemplate.final.pbit. To configure a connection with the SQL server, on the Power Bi desktop, go to Home --> Get data --> Server, and follow the steps in the interface to configure a connection.

### Step 4
Now we have set-up our ETL architecture and are able to trigger our pipeline. We either wait for a scheduled trigger or select the option to trigger now. On a successful run, our database has been populated with our processed files.

## Data sources
### NSW Bureau of Crime Statistics and Research (BOSCAR)
Crime statisitcs per LGA:
https://www.bocsar.nsw.gov.au/Pages/bocsar_crime_stats/bocsar_lgaexceltables.aspx

NSW crime trend data:
https://www.bocsar.nsw.gov.au/Pages/bocsar_crime_stats/bocsar_crime_stats.aspx

### Australian Bureau of Statistics (ABS)

LGA population data:
https://dbr.abs.gov.au/

Local Government Area, Indexes, SEIFA 2016:
https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/2033.0.55.0012016?OpenDocument

### National Skills Commission (NSW)
SALM Smoothed LGA Datafiles (ASGS 2022) - June quarter 2022:
https://www.nationalskillscommission.gov.au/topics/small-area-labour-markets

### Data.gov.au
DSS Benefit and Payment Recipient Demographics - quarterly data:
https://data.gov.au/dataset/ds-dga-cff2ae8a-55e4-47db-a66d-e177fe0ac6a0/details


