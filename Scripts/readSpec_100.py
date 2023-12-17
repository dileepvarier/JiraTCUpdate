# import xlrd
from pandas import *

import writeLog


def readExcel(spec_file, sheetIndex_DetailedSpec):
    try:
        writeLog.writeLogInfo("Debug", "Begin to read Spec document.")
        xls = ExcelFile(spec_file)
        df = xls.parse(xls.sheet_names[sheetIndex_DetailedSpec])
        return df
        # code to read the data to dictionary
    except Exception as e:
        writeLog.writeLogInfo("Error", "Exception in this method")
        print(e)
