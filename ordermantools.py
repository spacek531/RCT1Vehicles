import re
import json

"""Written by Spacek531 for manipulation of jobjectson files for the purposes of creating RCT1 rides in OpenRCT2. Paste a string and all numbers will be incremented by the total range, for the number of repetitions specified."""

"""
exec(open("D:/documents/openrct2/custom rides/rct1 project/object/ordermantools.py").read())

"""

numPattern = re.compile("\d+")

def GetNumbers(inString):
    nums = [int(n) for n in re.findall(numPattern, inString)]
    return nums

def GetRange(inString):
    nums = [int(n) for n in re.findall(numPattern, inString)]
    nums = [i for i in range(min(nums),max(nums) + 1)]
    return nums
    
def FindRangeAndIncrement(inString, repetitions):
    nums = GetNumbers(inString)
    
    startValue = min(nums)
    endValue = max(nums)
    rangeValue = endValue - startValue + 1
    print("Min: "+str(startValue)+" Max: "+str(endValue)+" Range: "+str(rangeValue))
    outstring = ""
    print("----------")
    for i in range(1, repetitions + 1):
        def matchcatch(match):
            if match.group(0).isdigit():
                return str(int(match.group(0)) + rangeValue * i)
            else:
                return match.group(0)
        outstring += re.sub(numPattern,matchcatch, inString)
    print(outstring)
    print("----------")
    
def IncrementValue(inString, oldOffset, newOffset):
    print("----------")    
    def matchcatch(match):
        if match.group(0).isdigit():
            return str(int(match.group(0)) + newOffset - oldOffset)
        else:
            return match.group(0)
    outstring = re.sub(numPattern,matchcatch, inString)
    print(outstring)
    print("----------")
    
def ScrapeImages(jobject):
    if "images" not in jobject:
        print("Error: images not in jobjectson")
        return []
    images = []
    for s in jobject["images"]:
        if type(s) == str:
            if len(s) == 0:
                images.append(s)
                continue
            prefix = s.split("[")[0]
            rng = GetRange(s)
            if len(rng) > 0:
                try:
                    for i in range(rng[0], rng[-1] + 1):
                        images.append(prefix+"["+str(i)+"]")
                except Exception as e:
                    print("Error with string \""+s+"\"",rng, e)
        elif type(s) == dict:
            images.append(s)
    return images

def CutOne(l, start, end):
    fullrange = end + 1 - start
    halfrange = fullrange // 2
    if fullrange%2 != 0:
        print("Odd number of images in CutOne", start, end)
        return
    cut1 = [l[i] for i in range(start, start + halfrange)]
    cut2 = [l[i] for i in range (start + halfrange, end + 1)]
    for i in range(halfrange):
        l[start + i] = cut2[i]
    for i in range (halfrange):
        l[start + halfrange + i] = cut1[i]

def CutTwo(l, start, end):
    fullrange = end + 1 - start
    halfrange = fullrange // 2
    if fullrange%4 != 0:
        print("Odd number of images in CutTwo", start, end)
        return
    CutOne(l, start, start + halfrange - 1)
    CutOne(l, start + halfrange, end)
    cut1 = [l[i] for i in range(start, start + halfrange)]
    cut2 = [l[i] for i in range (start + halfrange, end + 1)]
    for i in range(halfrange):
        l[start + i] = cut2[i]
    for i in range (halfrange):
        l[start + halfrange + i] = cut1[i]

def CutThree(l, start, end):
    fullrange = end + 1 - start
    halfrange = fullrange // 2
    if fullrange%8 != 0:
        print("Odd number of images in CutThree", start, end)
        return
    CutTwo(l, start, start + halfrange - 1)
    CutTwo(l, start + halfrange, end)
    cut1 = [l[i] for i in range(start, start + halfrange)]
    cut2 = [l[i] for i in range (start + halfrange, end + 1)]
    for i in range(halfrange):
        l[start + i] = cut2[i]
    for i in range (halfrange):
        l[start + halfrange + i] = cut1[i]

def Cut(l, start, length, depth):
    [CutOne, CutTwo, CutThree][depth](l, start, start + length - 1)
    
class SpriteGroup:
    def __init__(self, name, defaultPrecision, reversePower, reverseRepetitions):
        self.specialFunction = None
        self.defaultPrecision = defaultPrecision
        self.name = name
        self.reversePower = reversePower
        self.reverseRepetitions = reverseRepetitions
    
    def sprites(self, precision):
        return (precision * self.reverseRepetitions) << self.reversePower
    
    def group(self, precision):
        return precision << self.reversePower
        
    def setSpecialFunction(self, function):
        self.specialFunction = function

SpriteNameIndex = ["slopeFlat", "slopes12","slopes25","slopes42","slopes60","slopes75","slopes90","slopesLoop","slopeInverted","slopes8","slopes16","slopes50","flatBanked22","flatBanked45","inlineTwists","slopes12Banked22","slopes8Banked22","slopes25Banked22","slopes25Banked45","slopes12Banked45","corkscrews","restraintAnimation","curvedLiftHill"]
DefaultImageLengths = {"slopeFlat": 32, "slopes12":4, "slopes25": 32, "slopes42":8,"slopes60":32,"slopes75":4,"slopes90":32, "slopesLoop":4, "slopeInverted":4, "slopes8":4,"slopes16":4,"slopes50":4,"flatBanked22":8, "flatBanked45":32, "inlineTwists":4, "slopes12Banked22":32,"slopes8Banked22":4, "corkscrews":4,"restraintAnimation":4}

PowerOfGroup =       [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 255, 0, 0]
RepetitionsOfGroup = [1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 255, 3, 1]

SpriteGroups = [
    SpriteGroup("slopeFlat", 32, 0, 1),
    SpriteGroup("slopes12", 4, 1, 1),
    SpriteGroup("slopes25", 32, 1, 1),
    SpriteGroup("slopes42", 8, 1, 1),
    SpriteGroup("slopes60", 32, 1, 1),
    SpriteGroup("slopes75", 4, 1, 1),
    SpriteGroup("slopes90", 32, 1, 1),
    SpriteGroup("slopesLoop", 4, 1, 5),
    SpriteGroup("slopeInverted", 4, 0, 1),
    SpriteGroup("slopes8", 4, 1, 1),
    SpriteGroup("slopes16", 4, 1, 1),
    SpriteGroup("slopes50", 4, 1, 1),
    SpriteGroup("flatBanked22", 4, 1, 1),
    SpriteGroup("flatBanked45", 32, 1, 1),
    SpriteGroup("inlineTwists", 4, 1, 5),
    SpriteGroup("slopes12Banked22",32, 2, 1),
    SpriteGroup("slopes8Banked22", 4, 2, 1),
    SpriteGroup("slopes25Banked22", 4, 2, 1),
    SpriteGroup("slopes25Banked45", 32, 2, 1),
    SpriteGroup("slopes12Banked45", 4, 2, 1),
    SpriteGroup("corkscrews", 4, 0, 20),
    SpriteGroup("restraintAnimation", 4, 0, 3),
    SpriteGroup("curvedLiftHill", 32, 0, 1)
]

def corkscrewFunction(images, precision, carImageRanges):
    # print(images, precision, carImageRanges)
    Cut(images, carImageRanges, precision * 10, 0)
    Cut(images, carImageRanges + precision * 10, precision * 10, 0)
    for j in range(0,precision * 20,precision):
        Cut(images, carImageRanges + j, precision, 0)

SpriteGroups[20].setSpecialFunction(corkscrewFunction)

def ReverseImageOrder(inString):
    nums = []
    jobject = None
    try:
        jobject = json.loads(inString)
    except Exception as e:
        print("Error: could not load jobjectson",e)
        return
    if type(jobject) != dict:
        print("Error: jobjectson is not a dictionary")
        return
    if "properties" not in jobject:
        print("Error: properties not in jobjectson")
        return
    if "cars" not in jobject["properties"]:
        print("Error: cars not in properties dict")
        return
    images = ScrapeImages(jobject)
    if len(images) == 0:
        return
    print("Number of images",len(images))
    carImageRanges = 3
    lengthswap = 0
    carno = 0
    sstart = 0
    for car in jobject['properties']['cars']:
        spriteGroups = car['spriteGroups']
        print("Car", carno, "Offset",carImageRanges, images[carImageRanges])
        carno += 1
        for i in range(car["numSeatRows"]+1):
            print("Current offset", carImageRanges)
            for spriteGroup in SpriteGroups:
                rowstart = carImageRanges
                if spriteGroup.name not in spriteGroups:
                    continue
                precision = spriteGroups[spriteGroup.name]
                print(spriteGroup.name, spriteGroups[spriteGroup.name])
                if spriteGroup.specialFunction is not None:
                    spriteGroup.specialFunction(images, precision, carImageRanges)
                    carImageRanges += spriteGroup.sprites(precision)
                else:
                    for i in range(spriteGroup.reverseRepetitions):
                        Cut(images, carImageRanges, spriteGroup.group(precision),spriteGroup.reversePower)
                        carImageRanges += spriteGroup.group(precision)
                print("numImages",carImageRanges - rowstart)
    
    jobject["images"] = images
    
    print(json.dumps(jobject, indent = 4))
    