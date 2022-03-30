import re

pattern = "[0-9]+.?[0-9]+"
data = "(0.3453453,0.3123124345)"
numbers = re.findall(pattern,data)
x = numbers[0]
y = numbers[1]
print ("{},{}".format(x,y))
