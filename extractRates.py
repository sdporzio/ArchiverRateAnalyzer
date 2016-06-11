# MODULES
import time
import os
import sys
import numpy as np
from datetime import datetime as dt
# LOCAL MODULES
projDir = os.environ.get('PROJDIR_RATEANA')
sys.path.insert(0, projDir)
import Modules.dtOperations as DTO
import Modules.querySQL as QSQL

# StartTime and endTime for queries
# In order to correctly advance hour by hour, it should be annoyingly converted to a Unix timestamp (to add 3600 seconds) and then back to a datetime object
startTime = dt(2016, 1, 1, 0, 0, 0)
endTime = dt(2016, 1, 1, 0, 10, 0)
stepSize = 24*60*60 # in seconds
options = [startTime,endTime,stepSize]

# Variable names
varNames = np.genfromtxt(projDir+"/channelNames.dat",names=True,dtype=None)
varPaths = []
for name in varNames['VariableName']:
    # Number of steps from startTime to endTime
    diffTime = time.mktime(endTime.timetuple()) - time.mktime(startTime.timetuple())
    nSteps = int(diffTime/stepSize)

    # Get entries number from startTime to endTime for variable (varName)
    dataOut = []
    varName = name # <- Change this one here
    loopTimeLeft = startTime
    for i in range(nSteps):
        loopTimeRight = DTO.MoveDatetimeForward(loopTimeLeft,stepSize)
        rate = QSQL.GetEntriesNumberByName(varName,loopTimeLeft,loopTimeRight)
        timestampOut = DTO.GetChicagoTimestampDT(loopTimeLeft)
        dataOut.append([timestampOut,rate])
        print name,loopTimeLeft.strftime('%Y %b %d %H:%M:%S'),rate
        loopTimeLeft = loopTimeRight

    outPath = "Data/"+name.replace('/','_')+"_"+startTime.strftime('%y%m%d')+"_"+endTime.strftime('%y%m%d')+"_"+str(stepSize)+"s.dat"
    varPaths.append(projDir+outPath)
    np.savetxt(outPath,np.array((dataOut)),delimiter=' ',header='Timestamp Rate')

np.savetxt(projDir+'/Data/outList.dat',np.array(varPaths),delimiter=' ',fmt="%s",header='VariablePath')

# print np.matrix(options)
# print np.matrix(options).transpose()
np.savetxt(projDir+'/Data/options.dat',np.matrix(options),delimiter='\t',fmt='%s',header='StartTime\tEndTime\tStepSize')
