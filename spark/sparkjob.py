from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/app/pageView.txt", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

#group username to post ids (arnim, <1,2,3>)
viewsperuser = pairs.distinct().groupByKey()


usertotuple = viewsperuser.flatMap(lambda newpair: [(newpair[0], pair) for pair in list(itertools.combinations(newpair[1],2))])

output = usertotuple.collect()

for user, pair in output:
    print("("+user+": "+str(pair)+")")

print("----------------done---------------")



# def pairs1(a):
#     list = []
#     for i in a:
#         for j in a:
#             pair = (i,j)
#             list.append(pair)
#     return list




# pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
# count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
#                                                   # and then reduce all the values by adding them together
#
# output = count.collect()                          # bring the data back to the master node so we can print it out
# for page_id, count in output:
#     print ("page_id %s count %d" % (page_id, count))
# print ("Popular items done")

sc.stop()
