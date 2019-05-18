import re
def fun1(peoplestr):
  pattern=r','
  result=re.split(pattern,peoplestr)
  return result
peo="gap,zhi,guang,hhu,hui"
result=fun1(peo)
print(result)
