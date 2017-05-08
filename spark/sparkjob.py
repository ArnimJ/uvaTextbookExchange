from pyspark import SparkContext
import itertools
import MySQLdb

#return a list of combinations
def combs(a):
    return list(itertools.combinations(a,2))


sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/app/pageView.txt", 2)     # each worker loads a piece of the data file


pairs = data.map(lambda line: tuple(line.split("\t")))   # tell each worker to split each line of it's partition
pairs = pairs.distinct()

#group username to post ids (arnim, <1,2,3>)
viewsperuser = pairs.groupByKey()

#sort lists of page views so that we don't have (10,12) and (12,10) be different tuples
viewsperuser = viewsperuser.map(lambda x: (x[0], sorted(x[1])))

usertotuple = viewsperuser.flatMap(lambda p: [(p[0], tups) for tups in combs(p[1])])

output = usertotuple.collect()

for user, pair in output:
    for i in pair:
        print("("+user+": "+str(pair)+")")

print("----------------done---------------")

#part 4
swap = usertotuple.map(lambda p: (p[1], p[0]))
viewtouser = swap.groupByKey()

output = viewtouser.collect()

for pair, user in output:
    print("(" + str(pair) + " : " + repr(user))

print("----------------done---------------")

#part 5

step5 = viewtouser.map(lambda p: (p[0],len(p[1])))
output = step5.collect()
for pair, num in output:
    print("(" + str(pair) + " : " + str(num))

#step 6

step6 = step5.filter(lambda x: x[1] >= 2)
output = step6.collect()
for pair, num in output:
    print("(" + str(pair) + " : " + str(num))


#--------Database stuff--------------------------------------

db = MySQLdb.connect("db","www","$3cureUS","cs4501")
cursor = db.cursor()
cursor.execute("Truncate recommendations") #delete contents of table

dict = {}
for pair, num in output:
    if dict



db.close()

sc.stop()
