import time
import datetime
import commands
import psycopg2
import os
import numpy as np


projDir = os.environ.get('PROJDIR_RATEANA')
npPassword = np.genfromtxt(projDir+"/Modules/password.txt",dtype=None)

def GetVarArrayInterval( variable , time_start , time_end ):
    conn = psycopg2.connect(host="ifdb06.fnal.gov", user='smcreader', password=npPassword,port='5438', database="slowmoncon_archive")
    cur = conn.cursor()

    cur.execute("SELECT smpl_time,float_val FROM sample INNER JOIN channel USING (channel_id)"
        "WHERE name = %s and smpl_time > %s and smpl_time < %s;",
         (variable, time_start, time_end) )

    result = []

    for row in cur:
  #      print '| ', ' | '.join( str(v) for v in row ), ' |'
        result.append([row[0],row[1]])

    conn.close()
    return result


def GetVarArrayLast( variable , time_start  ):
    conn = psycopg2.connect(host="ifdb06.fnal.gov", user='smcreader', password=npPassword,port='5438', database="slowmoncon_archive")
    cur = conn.cursor()

    cur.execute("SELECT smpl_time,float_val FROM sample INNER JOIN channel USING (channel_id)"
        "WHERE name = %s and smpl_time < %s ORDER BY smpl_time DESC LIMIT 1;",
        (variable, time_start) )

    result = []

    for row in cur:
 #       print '| ', ' | '.join( str(v) for v in row ), ' |'
        result.append([row[0],row[1]])

    conn.close()
    return result


def GetEntriesNumberByName(channelName,startTime,endTime):
    conn = psycopg2.connect(host="ifdb06.fnal.gov", user='smcreader', password=npPassword,port='5438', database="slowmoncon_archive")
    cur = conn.cursor()

    cur.execute("SELECT smpl_time,float_val FROM sample INNER JOIN channel USING (channel_id) WHERE name = %s and smpl_time > %s and smpl_time < %s;",(channelName,startTime,endTime))

    result = []

    for row in cur:
        result.append([row[0],row[1]])

    rate = len(result)
    conn.close()

    return rate


def GetEntriesNumberById(channelId,startTime,endTime):
    # Great for loops! Not very efficient (row[2] looping is unnecessary)
    # but for now will do.
    conn = psycopg2.connect(host="ifdb06.fnal.gov", user='smcreader', password=npPassword,port='5438', database="slowmoncon_archive")
    cur = conn.cursor()

    cur.execute("SELECT smpl_time,float_val,name FROM sample INNER JOIN channel USING (channel_id) WHERE channel_id = %s and smpl_time > %s and smpl_time < %s;",(channelId,startTime,endTime))

    result = []

    for row in cur:
        result.append([row[0],row[1],row[2]])

    name = result[0][2]
    rate = len(result)
    conn.close()

    return name, rate
