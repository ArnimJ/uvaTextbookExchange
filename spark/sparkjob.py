from pyspark import SparkContext
import itertools
import MySQLdb
import time

#return a list of combinations
def combs(a):
    return list(itertools.combinations(a,2))


sc = SparkContext("spark://spark-master:7077", "PopularItems")

#while True:
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

print("------------------")

#--------Database stuff--------------------------------------

db = MySQLdb.connect("db","www","$3cureUS","cs4501")
cursor = db.cursor()
cursor.execute("Truncate marketplace_recommendation") #delete contents of table

for pair, num in output:
    id = int(pair[0])
    rec = str(pair[1]) + ","
    sql = "INSERT INTO marketplace_recommendation (listing, recs) VALUES ('%d', '%s') ON DUPLICATE KEY UPDATE recs=CONCAT(recs,'%s')" % (id , rec, rec)
    print (sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    id1 = int(pair[1])
    rec1 = str(pair[0]) + ","

    sql2 = "INSERT INTO marketplace_recommendation (listing, recs) VALUES ('%d', '%s') ON DUPLICATE KEY UPDATE recs=CONCAT(recs,'%s')" % (id1, rec1, rec1)
    # print(sql)
    try:
        cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()

db.close()
        #time.sleep(180)

sc.stop()
