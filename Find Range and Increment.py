import re

"""Written by Spacek531 for manipulation of json files for the purposes of creating RCT1 rides in OpenRCT2.
Paste a string and all numbers will be incremented by the total range, for the number of repetitions specified."""

pattern = "\d+"
prog = re.compile(pattern)

def GetNumbers(inString):
    nums = re.findall(pattern, inString)
    nums = [int(n) for n in nums]
    return nums

def FindRangeAndIncrement(inString, repetitions):
    
    nums = GetNumbers(inString)
    
    startValue = min(nums)
    endValue = max(nums)
    rangeValue = endValue - startValue + 1

    print("----------")    
    for i in range(1, repetitions + 1):
        def matchcatch(match):
            if match.group(0).isdigit():
                return str(int(match.group(0)) + rangeValue * i)
            else:
                return match.group(0)
        print(re.sub(prog,matchcatch, inString))
    print("----------")
    
def IncrementValue(inString, oldOffset, newOffset):
    print("----------")    
    for i in range(1, repetitions + 1):
        def matchcatch(match):
            if match.group(0).isdigit():
                return str(int(match.group(0)) + newOffset - oldOffset)
            else:
                return match.group(0)
        print(re.sub(prog,matchcatch, inString))
    print("----------")