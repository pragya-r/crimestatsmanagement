# NSW Crime Statistics Management System
CSMS is a comprehensive platform in which users will have the ability to track and analyse crimes rates alongside socio-economic measures on an interactive dashboard.

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

### Using the application on Power Bi 
To just view our application use this link: 
https://app.powerbi.com/reportEmbed?reportId=1c2afab0-996d-403e-aa97-7c59852f90ca&autoAuth=true&ctid=e8911c26-cf9f-4a9c-878e-527807be8791

To edit and view our application:
For this data system appplication we used Power bi. 
The following decribes the steps involded: 
1. Download Microsoft Power Bi 
2. Download the file called LGAStatsTemplate.final.pbit
3. To use this systems dashborad go to file --> import --> Power Bi Template -->LGAStatsTemplate.final.pbit
This should allow you to view and edit the dashboard all. All the data used in this dashboard is already uploaded. 

