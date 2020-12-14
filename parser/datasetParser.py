import xml.etree.ElementTree as ET
from datetime import datetime


class DatasetParser:
    averageDays = None
    maxDays = None

    def getAverage(self):
        return self.averageDays

    def getMax(self):
        return self.maxDays

    def __seconds_between(self, d1, d2):
        d1 = datetime.strptime(d1[0:19], "%Y-%m-%dT%H:%M:%S")
        d2 = datetime.strptime(d2[0:19], "%Y-%m-%dT%H:%M:%S")
        return abs((d2 - d1).seconds + (d2 - d1).days * 24 * 60 * 60)

    def __average(self, lst):
        return sum(lst) / len(lst)

    # Print iterations progress
    def __printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█',
                           printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    def parse(self, dataset, traceTag):

        tree = ET.parse(dataset)
        root = tree.getroot()

        durations = []

        n = 0
        for trace in root:
            childCount = len(root)

            # Initial call to print 0% progress
            self.__printProgressBar(0, childCount, prefix='Progress:', suffix='Complete', length=50)

            if trace.tag == traceTag:

                n = n + 1
                # Update Progress Bar
                self.__printProgressBar(n, childCount, prefix='Progress:', suffix='Complete', length=50)

                lasteventdate = None

                for events in trace:
                    for event in events:
                        if event.attrib.get("key") == "time:timestamp":

                            eventdate = event.attrib.get("value")
                            if lasteventdate != None:
                                duration = self.__seconds_between(eventdate, lasteventdate)
                                durations.append(duration)

                            lasteventdate = eventdate

        averageDur = self.__average(durations)
        self.averageDays = averageDur / (60 * 60 * 24)

        maxDur = max(durations)
        self.maxDays = maxDur / (60 * 60 * 24)
