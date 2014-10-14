import sys

prefix = sys.argv[1]
count = 0
for line in sys.stdin:
   count += 1
   f = open("{}-{}.txt".format(prefix,count),"w")
   for i in range(30):
      f.write("{} {} {}\n".format(line.rstrip("\n"),(i*2+1),(i*2+2)))
   f.close()