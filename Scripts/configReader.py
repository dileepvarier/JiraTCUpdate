import configparser
import os
from pathlib import Path

'''
Author Name: Dileep P B - I530925
Author ID: I530925
Script Usage: Script to read the config file and return the values 
'''

# General- Settimg project path
os.environ["PYTHONIOENCODING"] = "utf-8"
path_current_directory = os.path.dirname(__file__)
pjt_basePath = str(Path(path_current_directory).parents[0])

# General- Config file read
#configFilePath = os.path.join(pjt_basePath, 'config\config.ini')
configFilePath = '..\config\config.ini'
config = configparser.ConfigParser()
config.read(configFilePath)


def getLogFileName():
    return config.get('LOG', 'logFileName')

def get_automationResultFilePath():
    return config.get('ResultExcel', 'filepath')

def get_colName_JiraTCID():
    return config.get('ResultExcel', 'colName_JiraTCID')

def get_colName_Result():
    return config.get('ResultExcel', 'colName_Result')

def get_colName_isEvidenceAvailable():
    return config.get('ResultExcel', 'colName_isEvidenceAvailable')

def get_colName_isUploadComplete():
    return config.get('ResultExcel', 'colName_isUploadComplete')

def get_jiraHost():
    return config.get('Jira_ENDpoints', 'jiraHost')

def get_endPoint_GetProjectAPI():
    return config.get('Jira_ENDpoints', 'endPoint_GetProjectAPI')

def get_endPoint_GetCycleID():
    return config.get('Jira_ENDpoints','endPoint_GetCycleID')

def get_endPoint_GetTCID():
    return config.get('Jira_ENDpoints','endPoint_GetTCID')

def get_endpoint_GetExecutionInfo():
    return config.get('Jira_ENDpoints','endpoint_GetExecutionInfo')

def get_endpoint_GetTestSepsInfo():
    return config.get('Jira_ENDpoints','endpoint_GetTestSepsInfo')

def get_endpoint_POSTAddTCToExecution():
    return config.get('Jira_ENDpoints','endpoint_POSTAddTCToExecution')

def get_endpoint_PUTStepStatusUpdate():
    return config.get('Jira_ENDpoints','endpoint_PUTStepStatusUpdate')

def get_endpoint_PUTTCStatusUpdate():
    return config.get('Jira_ENDpoints','endpoint_PUTTCStatusUpdate')

def get_endpoint_POSTAttachFile():
    return config.get('Jira_ENDpoints','endpoint_POSTAttachFile')

def get_endpoint_GetFolderInfo():
    return config.get('Jira_ENDpoints','endpoint_GetFolderInfo')

def get_projectName():
    return config.get('Jira_Project', 'projectName')

def get_currentVersion():
    return config.get('Jira_Project', 'currentVersion')

def get_currentCycle():
    return config.get('Jira_Project', 'currentCycle')

def get_currentFolder():
    return config.get('Jira_Project', 'currentFolder')

def get_basicAuth():
    return config.get('Jira_Project', 'basicAuth')

def get_evidenceFileFormat():
    return config.get('EvidenceFile', 'evidenceFileFormat')

def get_evidenceFilePath():
    return config.get('EvidenceFile', 'evidenceFilePath')

def get_evidenceMIMEType():
    filetype=get_evidenceFileFormat()
    if filetype == '.zip':
        return 'application/zip'
    elif filetype == '.doc':
        return 'application/msword'
    elif filetype == '.xls':
        return 'application/msexcel'
    elif filetype == '.pdf':
        return 'application/pdf'
    elif filetype == '.jpeg' or filetype == '.jpg':
        return 'image/jpeg'
    elif filetype == '.html':
        return 'text/html'
    elif filetype == '.ppt':
        return 'application/mspowerpoint'
    elif filetype == '.txt':
        return 'text/plain'