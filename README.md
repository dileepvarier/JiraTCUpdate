# JiraTCUpdate
This script is to update the automation result in Jira Test cycle along with the evidence
## Set Up   
### Configuraitons in Jira
#### Below configurations need to completed in Jira side
 1. Request a technical user 
 2. Create a Version in Jira <**Version1**>
 3. Create a test cycle in Jira <**Cycle1**>
 4. Create a folder under test cycle <**Folder1**>
 #### Configuration for script execution
 1. Clone the project to Windows are Linix server (where Python is installed)
 2. Configure the INI file **config/config.ini** with the below details     
    projectName = **<JIRA PROJECT KEY>**
    currentVersion = <**Version1**>
    currentCycle = <**Cycle1**>
    currentFolder = <**Folder1**>
    basicAuth = Basic AAbbCCaaBBCC **<Create a Basic Auth toke using Jira technical user and password >**
 3. Make sure that Automation result is copied in config/AutomationResult.xlsx **< Use the same foramt as available in Repo>**
 4. Run the python script **StartJiraUpdate.py**
#### Debug
  If any issues refer the log file log/tcGeneration.log for further analysis or connect Central Automation Team
