from pyspark import SparkContext
import itertools

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
    print("("+user+": "+str(pair)+")")

print("----------------done---------------")

#part 4
swap = usertotuple.map(lambda p: (p[1], p[0]))
viewtouser = swap.groupByKey()

output = viewtouser.collect()

for pair, user in output:
    print("(" + str(pair) + " : " + str(user))

print("----------------done---------------")

#part 5

step5 = viewtouser.map(lambda p: (p[0],len(p[1])))
output = step5.collect()
for pair, num in output:
    print("(" + str(pair) + " : " + str(num))

step6 = step5.filter(lambda x: x[1] >= 2)
output = step6.collect()
for pair, num in output:
    print("(" + str(pair) + " : " + str(num))

# pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
# count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
#                                                   # and then reduce all the values by adding them together
#
# output = count.collect()                          # bring the data back to the master node so we can print it out
# for page_id, count in output:
#     print ("page_id %s count %d" % (page_id, count))
# print ("Popular items done")

sc.stop()
