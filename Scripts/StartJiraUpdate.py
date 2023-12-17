import requests
import writeLog
import configReader as rd
import pandas as pd


projectName = rd.get_projectName()
currentVersion = rd.get_currentVersion()
currentCycle = rd.get_currentCycle()
jiraHost = rd.get_jiraHost()
endPoint_GetInternalProjectID = rd.get_endPoint_GetProjectAPI()+projectName
endPoint_GetVersions = rd.get_endPoint_GetProjectAPI()+projectName+'/versions'
endPoint_GetCycleID = rd.get_endPoint_GetCycleID()
endPoint_GetTCID = rd.get_endPoint_GetTCID()
endpoint_GetExecutionInfo = rd.get_endpoint_GetExecutionInfo()
endpoint_GetTestSepsInfo = rd.get_endpoint_GetTestSepsInfo()
endpoint_POSTAddTCToExecution = rd.get_endpoint_POSTAddTCToExecution()
endpoint_PUTStepStatusUpdate = rd.get_endpoint_PUTStepStatusUpdate()
endpoint_PUTTCStatusUpdate = rd.get_endpoint_PUTTCStatusUpdate()
endpoint_POSTAttachFile = rd.get_endpoint_POSTAttachFile()
endpoint_GetFolderInfo = rd.get_endpoint_GetFolderInfo()
basicAuth = rd.get_basicAuth()
reportFileFormat=rd.get_evidenceFileFormat()
reportFilePath=rd.get_evidenceFilePath()
evidenceMIMEType = rd.get_evidenceMIMEType()

#postData_POSTAddTCToExecution = {"cycleId": "", "issueId": "", "projectId": "", "versionId": ""}
postData_PUTTcStatus_pass = {"status": 1}
postData_PUTTcStatus_fail = {"status": 2}

inputHEADERS = {"Authorization" : basicAuth}
inputHEADERS_POST = {"Authorization" : basicAuth,"Content-Type": "application/json"}
inputHEADERS_Attach = {"Authorization" : basicAuth}
lstTCExternalIDs = ['ROCHE-21481','ROCHE-21661']

excel_data = pd.read_excel(rd.get_automationResultFilePath())
# Read the values of the file in the dataframe
data = pd.DataFrame(excel_data, columns=[rd.get_colName_JiraTCID(),rd.get_colName_Result(),rd.get_colName_isEvidenceAvailable(),rd.get_colName_isUploadComplete()])
for ind in data.index:
    print(data[rd.get_colName_JiraTCID()][ind], data[rd.get_colName_Result()][ind], data[rd.get_colName_isEvidenceAvailable()][ind],data[rd.get_colName_isUploadComplete()][ind])

def getInternalTCid_Inside_ExecutionCycle(currentTCinternalID,currentVersionInternalID,currentCycleInternalID):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method  getInternalTCid_Inside_ExecutionCycle ----" + currentTCinternalID + ',' + currentVersionInternalID + ',' + currentCycleInternalID)
        current_endPoint_GetExecutionInfo = endpoint_GetExecutionInfo + '?issueId='+currentTCinternalID+'&versionId='+currentVersionInternalID+'&cycleId='+currentCycleInternalID
        writeLog.writeLogInfo("Debug", "        Get Execution info for the test case ----")
        r = requests.get(url=jiraHost + current_endPoint_GetExecutionInfo, headers=inputHEADERS, verify=True)
        writeLog.writeLogInfo("Debug", "Response received for GET " + current_endPoint_GetExecutionInfo + str(r.json()))
        curentTCInfo_under_ExecutionCycle = r.json()['executions'][0]
        curentTCID_under_ExecutionCycle = str(curentTCInfo_under_ExecutionCycle['id'])
        writeLog.writeLogInfo("Debug", "TC Internal ID under the Execution cycle = " + curentTCID_under_ExecutionCycle)
        print("     Current TC Internal ID under Execution cycle----" + curentTCID_under_ExecutionCycle)
        return curentTCID_under_ExecutionCycle
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in Get TC ID inside the execution cycle" + str(e))
        return None

def getStepIDs_for_ExecutionTCID(curentTCID_under_ExecutionCycle):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method  getStepIDs_for_ExecutionTCID ----" + curentTCID_under_ExecutionCycle)
        current_endpoint_GetTestSepsInfo = endpoint_GetTestSepsInfo + '?executionId='+curentTCID_under_ExecutionCycle+'&expand='
        writeLog.writeLogInfo("Debug", "        Get Test step info for the test case ----")
        r = requests.get(url=jiraHost + current_endpoint_GetTestSepsInfo, headers=inputHEADERS, verify=True)
        currentTC_TestStepsInfo = r.json()
        currentTC_stepIDs =[]
        for eachStepInfo in currentTC_TestStepsInfo:
            currentTC_stepIDs.append(eachStepInfo['id'])
        print("     StepIDs =" + str(currentTC_stepIDs))
        return currentTC_stepIDs
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in getStepIDs_for_ExecutionTCID" + str(e))
        return None

def addTC_for_Execution(currentTCinternalID,currentVersionInternalID,currentCycleInternalID,projectID,folderID):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method addTC_for_Execution ----" + currentTCinternalID +','+ currentVersionInternalID+','+currentCycleInternalID+ ','+projectID)
        if folderID != None:
            postData_POSTAddTCToExecution = {"cycleId": "", "issueId": "", "projectId": "", "versionId": "","folderId":""}
            postData_POSTAddTCToExecution["folderId"] = folderID
        else:
            postData_POSTAddTCToExecution = {"cycleId": "", "issueId": "", "projectId": "", "versionId": ""}
        postData_POSTAddTCToExecution["cycleId"] = currentCycleInternalID
        postData_POSTAddTCToExecution["issueId"] = currentTCinternalID
        postData_POSTAddTCToExecution["projectId"] = projectID
        postData_POSTAddTCToExecution["versionId"] = currentVersionInternalID
        writeLog.writeLogInfo("Debug", "    ADD TC Execution ----" + str(postData_POSTAddTCToExecution) )
        print("    ADD TC Execution ----" + str(postData_POSTAddTCToExecution))
        r = requests.post(url=jiraHost + endpoint_POSTAddTCToExecution, headers=inputHEADERS_POST, json=postData_POSTAddTCToExecution)
        if (str(r.status_code) != '200'):
            writeLog.writeLogInfo("Error", "Adding TC "+ currentTCinternalID +"to cycle Failed, Proceeding with Next TC" + str(r))
            print("Adding TC " + currentTCinternalID + "to cycle Failed, Proceeding with Next TC....." )
        else:
            print("Adding TC " + currentTCinternalID + "to cycle Success, Going to upload result.....")
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in addTC_for_Execution" + str(e))
        return

def updateTestResult_inStep(curent_StepID):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method  updateTestResult_inStep ----" + str(curent_StepID))
        current_endpoint_PUTStepStatusUpdate = endpoint_PUTStepStatusUpdate + str(curent_StepID)
        writeLog.writeLogInfo("Debug", "Get Test step info for the test case ----")
        r = requests.put(url=jiraHost + current_endpoint_PUTStepStatusUpdate, headers=inputHEADERS_POST, json=postData_PUTTcStatus_pass)
        if (str(r.status_code) != '200'):
            writeLog.writeLogInfo("Error", "Updating Test step Failed.." + str(r))
            print("Updating Test step Failed ...." + str(r))
            return False
        return True
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in updateTestResult_inStep" + str(e))
        return False

def updateTestResult_inTC(curentTCID_under_ExecutionCycle,statusPayload):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method  updateTestResult_inTC ----" + curentTCID_under_ExecutionCycle)
        current_endpoint_PUTTCStatusUpdate = endpoint_PUTTCStatusUpdate + curentTCID_under_ExecutionCycle + "/execute"
        writeLog.writeLogInfo("Debug", "Get Test step info for the test case ----")
        r = requests.put(url=jiraHost + current_endpoint_PUTTCStatusUpdate, headers=inputHEADERS_POST, json=statusPayload)
        if (str(r.status_code) != '200'):
            writeLog.writeLogInfo("Error", "Updating overall Test Status Failed.." + str(r))
            print("Updating overall Test Status Failed ...." + str(r))
            return False
        return True
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in updateTestResult_inTC" + str(e))
        return False

def attachTestEvd(curentTCID_under_ExecutionCycle,postData_FileInfo):
    try:
        writeLog.writeLogInfo("Debug", "Inside the method  attachTestEvd ----" + curentTCID_under_ExecutionCycle)
        current_endpoint_POSTAttachFile = endpoint_POSTAttachFile + '?entityId=' + curentTCID_under_ExecutionCycle + '&entityType=SCHEDULE'
        writeLog.writeLogInfo("Debug", "Get Test step info for the test case ----")
        r = requests.post(url=jiraHost + current_endpoint_POSTAttachFile, headers=inputHEADERS_Attach, files=postData_FileInfo)
        if (str(r.status_code) != '200'):
            writeLog.writeLogInfo("Error", "Upload Evidence Failed.." + str(r))
            print("Upload Evidence Failed ...." + str(r))
            return False
        print("Upload Evidence Success ...." + str(r))
        return True
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in attachTestEvd" + str(e))
        return False

def getFolderDetails(projectID,currentVersionInternalID,currentCycleInternalID,folderName):
    print("Going to Get Folder details...")
    writeLog.writeLogInfo("Debug", "Going to Get Folder details---- FolderName=" + folderName)
    r = requests.get(url=jiraHost + endpoint_GetFolderInfo+currentCycleInternalID+'/'+'/folders?projectId='+projectID+'&versionId='+currentVersionInternalID, headers=inputHEADERS, verify=True)
    writeLog.writeLogInfo("Debug", "Response received for GET /rest/zapi/latest/cycle/" + str(r.json()))
    for folders in r.json():
        if folders['folderName'] == folderName:
            internalFolderID = str(folders['folderId'])
            print('Current Folder name = ' + folders['folderName'] + ', Current Folder Internal ID = ' + internalFolderID)
            writeLog.writeLogInfo("Debug", 'Current Folder name = ' + folders['folderName'] + ', Current folder Internal ID = ' + internalFolderID)
            return folders['folderId']
    return None
try:
    #1. Get internal project ID from configuration
    print("1. Get internal project ID from configuration----")
    writeLog.writeLogInfo("Debug", "1. Get internal project ID from configuration----")
    r = requests.get(url=jiraHost+endPoint_GetInternalProjectID, headers=inputHEADERS, verify=True)
    writeLog.writeLogInfo("Debug", "Response received for GET /rest/api/latest/project/ROCHE" + str(r.json()))
    projectID=r.json()['id']
    writeLog.writeLogInfo("Debug", "Internal Project ID = " + projectID)
    writeLog.writeLogInfo("Debug", "-------------------------------------------------")
    print("Internal Project ID = " + projectID)
except Exception as e:
    writeLog.writeLogInfo("Error", "Exception in 6. Get steps from execution TC ID" + str(e))
    exit()

try:
    #2. Get all available versions in Project
    print("2. Get versions from Project----")
    writeLog.writeLogInfo("Debug", "2. Get versions from Project----"+ projectID)
    r = requests.get(url=jiraHost+endPoint_GetVersions, headers=inputHEADERS, verify=True)
    writeLog.writeLogInfo("Debug", "Response received for GET /rest/api/latest/project/ROCHE" + str(r.json()))
    lstVersionInfo=r.json()
    for versionInfo in lstVersionInfo:
        if versionInfo['name'] == currentVersion:
            currentVersionInternalID = versionInfo['id']
            print("Version name = "+ versionInfo['name'] +", Internal Version ID = "+ currentVersionInternalID)
            pass
    #writeLog.writeLogInfo("Debug", "Internal Project ID = " + projectID)
    writeLog.writeLogInfo("Debug", "-------------------------------------------------")
except Exception as e:
    writeLog.writeLogInfo("Error", "Exception in 2. Get all available versions in Project" + str(e))
    exit()

try:
    #3. Get all cycles in the version
    print("3. Get all cycles in the version----")
    endPoint_GetCycleID=endPoint_GetCycleID+'?projectId='+ projectID+'&versionId=' + currentVersionInternalID
    writeLog.writeLogInfo("Debug", "3. Get all cycles in the version ----"+ currentVersionInternalID)
    r = requests.get(url=jiraHost+endPoint_GetCycleID, headers=inputHEADERS, verify=True)
    writeLog.writeLogInfo("Debug", "Response received for GET "+endPoint_GetCycleID + str(r.json()))
    lstCycleInfo=r.json()
    for cycle in lstCycleInfo:
        if cycle.isdigit() and 'name' in lstCycleInfo[cycle]:
            if lstCycleInfo[cycle]['name'] == currentCycle:
                currentCycleInternalID = cycle
                print('Current Cycle name = ' + lstCycleInfo[cycle]['name'] + ', Current Cycle Internal ID = ' +currentCycleInternalID)
                writeLog.writeLogInfo("Debug",'Current Cycle name = ' + lstCycleInfo[cycle]['name'] + ', Current Cycle Internal ID = ' + currentCycleInternalID)
    writeLog.writeLogInfo("Debug", "-------------------------------------------------")
except Exception as e:
    writeLog.writeLogInfo("Error", "Exception in 3. Get all cycles in the version----" + str(e))
    exit()

try:
    internalFolderID = getFolderDetails(projectID, currentVersionInternalID, currentCycleInternalID, rd.get_currentFolder())
except Exception as e:
    writeLog.writeLogInfo("Error", "Exception in collecting Folder name----" + str(e))
    exit()

try:
    #4. Get internal TC ID from external key and add it execution cycle, get test steps , update result (Collect for all TC - loop1)
    print("4. Get internal TC ID from external key and add it execution cycle, get test steps , update result(Collect for all TC - loop1)----")
    #for TC in lstTCExternalIDs:
    for ind in data.index:
        TC=data[rd.get_colName_JiraTCID()][ind]
        if str(data[rd.get_colName_Result()][ind]).upper() == 'PASS' and str(data[rd.get_colName_isEvidenceAvailable()][ind]).upper() == 'YES' and str(data[rd.get_colName_isUploadComplete()][ind]).upper() != 'COMPLETED':
            current_endPoint_GetTCID=endPoint_GetTCID + TC + '?fields=id'
            writeLog.writeLogInfo("Debug", "Get internal TC ID from external ----"+ TC)
            print("Get internal TC ID from external ----"+ TC)
            r = requests.get(url=jiraHost+current_endPoint_GetTCID, headers=inputHEADERS, verify=True)
            writeLog.writeLogInfo("Debug", "Response received for GET "+current_endPoint_GetTCID + str(r.json()))
            currentTCinternalID=r.json()['id']
            print("     Current TC Internal ID ----"+ currentTCinternalID)
            writeLog.writeLogInfo("Debug", "     Current TC Internal ID ----"+ currentTCinternalID)
            addTC_for_Execution(currentTCinternalID,currentVersionInternalID,currentCycleInternalID,projectID,internalFolderID)
            curentTCID_under_ExecutionCycle = getInternalTCid_Inside_ExecutionCycle(currentTCinternalID,currentVersionInternalID,currentCycleInternalID)
            if curentTCID_under_ExecutionCycle is None:
                pass
            currentTC_stepIDs = getStepIDs_for_ExecutionTCID(curentTCID_under_ExecutionCycle)
            if currentTC_stepIDs is None or len(currentTC_stepIDs) == 0:
                pass
            writeLog.writeLogInfo("Debug", "Test step IDs for " + TC +"----" + str(currentTC_stepIDs))

            for eachStep in currentTC_stepIDs:
                updateTestResult_inStep(eachStep)
            postData_FileInfo = {'file': (TC + reportFileFormat, open(reportFilePath + TC + reportFileFormat, 'rb'), 'application/zip')}
            attachTestEvd(curentTCID_under_ExecutionCycle,postData_FileInfo)
            if updateTestResult_inTC(curentTCID_under_ExecutionCycle,postData_PUTTcStatus_pass):
                data.loc[ind, [rd.get_colName_isUploadComplete()]] = 'COMPLETED'
                writeLog.writeLogInfo("Debug", TC + "Test is passed in Jira---")
                print(TC + "Test is passed in Jira---")
        elif str(data[rd.get_colName_Result()][ind]).upper() == 'FAIL':
            current_endPoint_GetTCID = endPoint_GetTCID + TC + '?fields=id'
            writeLog.writeLogInfo("Debug", "Get internal TC ID from external ----" + TC)
            print("Get internal TC ID from external ----" + TC)
            r = requests.get(url=jiraHost + current_endPoint_GetTCID, headers=inputHEADERS, verify=True)
            writeLog.writeLogInfo("Debug", "Response received for GET " + current_endPoint_GetTCID + str(r.json()))
            currentTCinternalID = r.json()['id']
            print("     Current TC Internal ID ----" + currentTCinternalID)
            writeLog.writeLogInfo("Debug", "     Current TC Internal ID ----" + currentTCinternalID)
            addTC_for_Execution(currentTCinternalID, currentVersionInternalID, currentCycleInternalID, projectID,internalFolderID)
            curentTCID_under_ExecutionCycle = getInternalTCid_Inside_ExecutionCycle(currentTCinternalID,
                                                                                    currentVersionInternalID,
                                                                                    currentCycleInternalID)
            if curentTCID_under_ExecutionCycle is None:
                pass
            currentTC_stepIDs = getStepIDs_for_ExecutionTCID(curentTCID_under_ExecutionCycle)
            if currentTC_stepIDs is None or len(currentTC_stepIDs) == 0:
                pass
            writeLog.writeLogInfo("Debug", "Test step IDs for " + TC + "----" + str(currentTC_stepIDs))
            if updateTestResult_inTC(curentTCID_under_ExecutionCycle, postData_PUTTcStatus_fail):
                writeLog.writeLogInfo("Debug", TC + "Test is passed Failed Jira-----------------------------------------")
                print(TC + "Test is Failed in Jira---")
                data.loc[ind, [rd.get_colName_isUploadComplete()]] = 'NOT COMPLETED'
        else:
            writeLog.writeLogInfo("Debug", 'Skipping ' + TC + " Test is already executed in Jira or Evidence is not available-----")
            print('Skipping ' + TC + " Test is already executed in Jira or Evidence is not available-----")
        print("==============================END of TC===================================")
    writeLog.writeLogInfo("Debug", "-------------------------------------------------")

except Exception as e:
    writeLog.writeLogInfo("Debug", "Exception in 4. Get internal TC ID from external key----" + str(e))
    exit()