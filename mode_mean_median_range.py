from statistics import mean,mode,median





data=[1,1,6,2,3,1,3]

try:
    print("Mode:{}".format(mode(data)))
except:
    print("Mode: Error") #this means that there is no mode or there is more than 1 mode
print("Mean is {}".format(mean(data)))
print("median is {}".format(median(data)))
print("Range is {}".format(max(data)-min(data)))
