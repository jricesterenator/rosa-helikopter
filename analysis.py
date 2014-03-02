import thread
import time

class Filters:

    def __init__(self):
        self.filters = []

    def add(self, filter):
        self.filters.append(filter)

    def clear(self):
        del self.filters[:]

    def match(self, val):
        for f in self.filters:
            #If it didnt match the filter, skip it
            if not f(val):
                return False
        return True


class Analysis:

    def __init__(self, logGenerator):
        self.log = logGenerator
        self.counts = {}
        self.filterManager = Filters()
        self.sortfx = None
        self.sortAsc = True
        self.excludes = set()

    def excludeall(self):
        m = self.counts.copy()
        self.counts.clear()
        self.excludes = self.excludes.union(m.keys())
        print 'excludes is now', len(self.excludes),'long'


    def watch(self, counts):
        for line in self.log:
            line = line.strip()
            if line in counts:
                counts[line] += 1
            else:
                counts[line] = 1

    def displayCounts(self, delay):
        while True:

            outputList = []
            for k,v in self.counts.items():
                #skip excluded items
                if k in self.excludes:
                    continue

                if self.filterManager.match(v):
                    outputList.append((k,v))

            if self.sortfx:
                outputList = sorted(outputList, key=self.sortfx, reverse=(not self.sortAsc))

            if len(outputList):
                print "#####################################"
                for k,v in outputList:
                    print v,":::", k

            time.sleep(delay)

    def sortby(self, sortfx, asc=True):
        self.sortfx = sortfx
        self.sortAsc = asc

    def watchCounts(self):
        thread.start_new_thread(self.watch, (self.counts,))



class Details:

    def __init__(self):
        pass

"""
This function returns a generator you can iterate over for the contents.
"""
def follow(thefile):
    while True:
        line = thefile.readline()
        line = line.strip()
        if not line:
            time.sleep(0.1)
            continue

        yield line

def readfile(filename):
    f = open(filename, 'r')
    return follow(f)

global analysis

def count(fx):
    return lambda countval: fx(countval)

def lt(ltval):
    return lambda count: count < ltval

def lte(ltval):
    return lambda count: count <= ltval

def gt(val):
    return lambda count: count > val

def gte(val):
    return lambda count: count >= val

def eq(val):
    return lambda count: count == val

def excludeall():
    analysis.excludeall()

def ltcmp(o1, o2):
    ret =  o1[1] < o2[1]
    print o1, o2, ret
    return ret

sortbyval = lambda o: o[1]

def disp():
    thread.start_new_thread(analysis.displayCounts, (3,))

"""
    190 - Brake info is from 190.
    Depressed:     190 00 00 40 00 00 00 00 00
    Not depressed: 190 00 00 00 00 00 00 00 00
"""
def brakeActive(sender, hexMsg):
    if sender == 0x190:
        #Or, (hexMsg >> 8*5) & 0xF0
        #Or, (hexMsg >> 8*5+4) == 0x4
        #Or, (hexMsg >> 8*5) & 0xF0 == 0x40
        #Or, hexMsg & 0xF00000000000
        return (hexMsg >> 8*5) & 0xF0 == 0x40

    return False

"""
    39E - Steering Wheel Ops, Lights, and more
    Byte 6 - Handbrake Status 0x00 down, 0x20 up
"""
def handbrakeActive(sender, hexMsg):
    if sender == 0x39E:
        return (hexMsg >> 8*5) & 0xFF == 0x20
    return False

"""
    39E - Steering Wheel Ops, Lights, and more
    Byte 3 - Lights (if lights are actually on, not just the switch)
      0x00 - Off
      0x08 - Lights on (parking, normal, not brights)
      0x80 - Brights only
      0x88 - Brights + Lights
"""
def headlightsOn(sender, hexMsg):
    if sender == 0x39E:
        return (hexMsg >> 8*2) & 0x0F == 0x08
    return False

def brightsOn(sender, hexMsg):
    if sender == 0x39E:
        return (hexMsg >> 8*2) & 0x0F == 0x80
    return False

"""
    050 - ?? Info
    Byte 5 - Clutch in/out
    0x01 - Out
    0x02 - In
"""
def clutchIn(sender, hexMsg):
    if sender == 0x050:
        return (hexMsg >> 8*4) & 0x0F == 0x02
    return False

def clutchOut(sender, hexMsg):
    if sender == 0x050:
        return (hexMsg >> 8*4) & 0x0F == 0x01
    return False


"""
    228 - Neutral indicator
    Neutral: 228 00 00 00 00 00 00 00 00
    In Gear: 228 00 04 00 00 00 00 00 00
"""
def inNeutral(sender, hexMsg):
    if sender == 0x228:
        return (hexMsg >> 8*6) & 0x0F == 0x04
    return False

"""
    228 - Neutral indicator
    Neutral: 228 00 00 00 00 00 00 00 00
    In Gear: 228 00 04 00 00 00 00 00 00
"""
def inGear(sender, hexMsg):
    if sender == 0x228:
        return (hexMsg >> 8*6) & 0x0F == 0x00
    return False


if __name__ == '__main__':
    loggen = readfile('/tmp/log.txt')

    global analysis
    analysis = Analysis(loggen)
    analysis.watchCounts()
    analysis.sortby(sortbyval, asc=True)

    fm = analysis.filterManager
    fm.add(count(lt(5)))
    fm.add(count(gte(2)))

