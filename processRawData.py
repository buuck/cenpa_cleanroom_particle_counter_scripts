import sys
import csv
import datetime

#['Date', 'Time', 'Sample Period', 'Sample Volume', 'Sample Units', 'Count Mode', 'Concentration Mode', '0.5um', '1.0um', '2.0um', '5.0um', '0.0um', '0.0um', 'Sample Mode', 'Location Name', 'Sample Number', 'Cal. Value', 'Laser Current', '0.5um (Cum. Counts)', '1.0um (Cum. Counts)', '2.0um (Cum. Counts)', '5.0um (Cum. Counts)', '0.0um (Cum. Counts)', '0.0um (Cum. Counts)', 'Cal Alarm', 'Flow Alarm', 'Over Conc. Alarm', 'System Alarm', 'Count Alarm', 'Battery Alarm', 'Laser Alarm']

lastsmcount = None
lastlgcount = None
lastLineWritten = None
sample_datetime = datetime.datetime(2013,1,1)
last_datetime = None

file = sys.argv[1] 

tsvfile = open(file)
tsvreader = csv.reader(tsvfile, delimiter='\t')
for i in range(7): tsvreader.next()
colnames = tsvreader.next()
datecol = colnames.index('Date')
timecol = colnames.index('Time')
smcountcol = colnames.index('0.5um')
lgcountcol = colnames.index('2.0um')
for row in tsvreader:
    sample_datetime = sample_datetime.strptime(row[datecol]+' '+row[timecol], "%Y-%m-%d %H:%M:%S")
    if last_datetime is not None and sample_datetime < last_datetime: continue
    smcount = float(row[smcountcol])
    lgcount = float(row[lgcountcol])
    if smcount != lastsmcount or lgcount != lastlgcount: 
        if last_datetime is not None and lastLineWritten != tsvreader.line_num-1: 
            print sample_datetime, lastsmcount, lastlgcount
        print sample_datetime, smcount, lgcount
        lastLineWritten = tsvreader.line_num
    lastsmcount = smcount
    lastlgcount = lgcount
    last_datetime = sample_datetime
print last_datetime, lastsmcount, lastlgcount

