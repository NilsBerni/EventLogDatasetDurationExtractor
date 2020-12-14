# This is a sample implementation

# 1. Rename the xes extension to xml and insert into eventLogAna
# 2. Set the name of the dataset you want to extract information from

from parser.datasetParser import DatasetParser

# Dataset name
dataset = "T_BPIC15_1.xml"

dParser = DatasetParser()
dParser.parse(dataset, "{http://www.xes-standard.org}trace")

avrDur = dParser.getAverage()
maxDur = dParser.getMax()

print("Average duration (days): " + str(avrDur))
print("Max duration (days): " + str(avrDur))
