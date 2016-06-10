# MODULES
import time
import os
import sys
import numpy as np
from datetime import datetime as dt
# LOCAL MODULES
sys.path.insert(0, os.environ.get('PROJDIR_RATEANA'))
import Modules.dtOperations as DTO
import Modules.querySQL as QSQL

# StartTime and endTime for queries
# In order to correctly advance hour by hour, it should be annoyingly converted to a Unix timestamp (to add 3600 seconds) and then back to a datetime object
startTime = dt(2016, 1, 1, 0, 0, 0)
endTime = dt(2016, 6, 1, 0, 0, 0)
stepSize = 24*60*60 # in seconds

# Variable names
voltPOP = "uB_TPCDrift_HV01_keithleyPickOff/getVoltage"
devTrackPOP = "uB_TPCDrift_HV01_keithleyPickOff/voltDiff5s60s"
voltCM = "uB_TPCDrift_HV01_keithleyCurrMon/getVoltage"
currCM = "uB_TPCDrift_HV01_keithleyCurrMon/calcCurrent"

# Number of steps from startTime to endTime
diffTime = time.mktime(endTime.timetuple()) - time.mktime(startTime.timetuple())
nSteps = int(diffTime/stepSize)

# Get entries number from startTime to endTime for variable (varName)
dataOut = []
varName = voltPOP # <- Change this one here
loopTimeLeft = startTime
for i in range(nSteps):
    loopTimeRight = DTO.MoveDatetimeForward(loopTimeLeft,stepSize)
    rate = QSQL.GetEntriesNumberByName(varName,loopTimeLeft,loopTimeRight)
    timestampOut = DTO.GetChicagoTimestampDT(loopTimeLeft)
    dataOut.append([timestampOut,rate])
    print loopTimeLeft.strftime('%Y %b %d %H:%M:%S'),rate
    loopTimeLeft = loopTimeRight

outPath = "Data/"+varName.replace('/','_')+"_"+startTime.strftime('%y%m%d')+"_"+endTime.strftime('%y%m%d')+"_"+str(stepSize)+"s.dat"
np.savetxt(outPath,np.array((dataOut)),delimiter=' ',header='Timestamp Rate')
