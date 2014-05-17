def readFile(filename):
    f = open(filename, 'r')
    text = f.read().replace('\r\n', '\n').replace('\r','\n')
    f.close()
    return text.split('\n')



if __name__ == '__main__':
    lines = readFile('logs/SteeringLogs')

    import re

    x = re.compile(r'^082 \w{2} \w{2} (\w{2}) (\w{2}) (\w{2}) (\w{2}) \w{2} \w{2}.*')
    for l in lines:
        res = x.search(l)
        if not res:
            print l
            continue

        else:

            def getValues(groups):
                d11 = groups[0]
                d12 = groups[1]

                d21 = groups[2]
                d22 = groups[3]

#                print l
#                print d11
#                print d12
#                print d21
#                print d22

                d1_little = d12 + d11
                d1_big = d11 + d12

                d2_little = d22 + d21
                d2_big = d21 + d22


#                print d1_little
#                print d1_big
#                print d2_little
#                print d2_big


                s = "--- LE/BE %5s %5s  |  %5s %5s"
                s = s % (
                         int(d1_little, 16),
                         int(d1_big, 16),
                         int(d2_little, 16),
                         int(d2_big, 16)
                    )
                return s



            values = getValues(res.groups())

            print "%-40s %s" % (l, values)
