import re
import json

"""Written by Spacek531 for manipulation of jobjectson files for the purposes of creating RCT1 rides in OpenRCT2. Paste a string and all numbers will be incremented by the total range, for the number of repetitions specified."""

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

DefaultImageLengths = {"flat": 32, "slopes12":4, "slopes25": 32, "slopes42":8,"slopes60":32,"slopes90":32, "slopesLoop":4, "flatBanked":32, "flatBankedTransition":8,"flatToGentleSlopeBankedTransitions":32, "restraintAnimation": 4, "inlineTwist":4, "corkscrews":4, "slopesDiag":4}

def GetLength(car,rtype):
    if "framesNumRotations" in car and rtype in car["framesNumRotations"]:
        return car["framesNumRotations"][rtype]
    else:
        return DefaultImageLengths[rtype]
    
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
    print(type(["images"]))
    carImageRanges = 3
    lengthswap = 0
    carno = 0
    sstart = 0
    for car in jobject['properties']['cars']:
        print("Car", carno, "Offset",carImageRanges, images[carImageRanges])
        carno += 1
        for i in range(car["numSeatRows"]+1):
            rowstart = carImageRanges
            if i > 0:
                print("Doing SeatRow",i-1)
            if "flat" in car["frames"]:
                sstart = carImageRanges
                print("Doing Flat",images[carImageRanges])
                lengthswap = GetLength(car,"flat")
                Cut(images, carImageRanges,lengthswap, 0)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "gentleSlopes" in car["frames"]:
                sstart = carImageRanges
                print("Doing Gentle",images[carImageRanges])
                lengthswap = GetLength(car, "slopes12")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopes25")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "steepSlopes" in car["frames"]:
                sstart = carImageRanges
                print("Doing Steep",images[carImageRanges])
                lengthswap = GetLength(car, "slopes42")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopes60")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
            
            if "verticalSlopes" in car["frames"]:
                sstart = carImageRanges
                print("Doing Vertical",images[carImageRanges])
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopes90")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "slopesLoop")
                Cut(images, carImageRanges, lengthswap, 0)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "diagonalSlopes" in car["frames"]:
                sstart = carImageRanges
                print("Doing DiagSlopees",images[carImageRanges])
                lengthswap = GetLength(car, "slopesDiag")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
    
                lengthswap = GetLength(car, "slopesDiag")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
    
                lengthswap = GetLength(car, "slopesDiag")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "flatBanked" in car["frames"]:
                sstart = carImageRanges
                print("Doing FlatBanked",images[carImageRanges])
                lengthswap = GetLength(car, "flatBankedTransition")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "flatBanked")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "inlineTwists" in car["frames"]:
                sstart = carImageRanges
                print("Doing InlineTwistgs",images[carImageRanges])
                lengthswap = GetLength(car, "inlineTwist")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "inlineTwist")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "inlineTwist")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "inlineTwist")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "inlineTwist")*2
                Cut(images, carImageRanges, lengthswap, 1)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "flatToGentleSlopeBankedTransitions" in car["frames"]:
                sstart = carImageRanges
                print("Doing flatToGentleSlopeBankedTransitions",images[carImageRanges])
                lengthswap = GetLength(car, "flatToGentleSlopeBankedTransitions")*4
                Cut(images, carImageRanges, lengthswap, 2)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "diagonalGentleSlopeBankedTransitions" in car["frames"]:
                sstart = carImageRanges
                print("Doing diagonalGentleSlopeBankedTransitions",images[carImageRanges])
                lengthswap = 16
                Cut(images, carImageRanges, lengthswap, 2)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "gentleSlopeBankedTransitions" in car["frames"]:
                sstart = carImageRanges
                print("Doing gentleSlopeBankedTransitions",images[carImageRanges])
                lengthswap = 16
                Cut(images, carImageRanges, lengthswap, 2)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "gentleSlopeBankedTurns" in car["frames"]:
                print("Doing gentleSlopeBankedTurns",images[carImageRanges])
                lengthswap = GetLength(car, "slopes25Curved")*4
                Cut(images, carImageRanges, lengthswap, 2)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "flatToGentleSlopeWhileBankedTransitions" in car["frames"]:
                sstart = carImageRanges
                print("Doing flatToGentleSlopeWhileBankedTransitions",images[carImageRanges])
                lengthswap = 16
                Cut(images, carImageRanges, lengthswap, 2)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "corkscrews" in car["frames"]:
                sstart = carImageRanges
                print("Doing corkscrews",images[carImageRanges])
                lengthswap = GetLength(car, "corkscrews")*20
                Cut(images, carImageRanges, 40, 0)
                Cut(images, carImageRanges + 40, 40, 0)
                for j in range(0,80,4):
                    Cut(images, carImageRanges + j, 4, 0)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            if "restraintAnimation" in car["frames"]:
                sstart = carImageRanges
                print("Doing restraints",images[carImageRanges])
                lengthswap = GetLength(car, "restraintAnimation")
                Cut(images, carImageRanges, lengthswap, 0)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "restraintAnimation")
                Cut(images, carImageRanges, lengthswap, 0)
                carImageRanges += lengthswap
                
                lengthswap = GetLength(car, "restraintAnimation")
                Cut(images, carImageRanges, lengthswap, 0)
                carImageRanges += lengthswap
                #print(carImageRanges -  sstart)
                
            print("Images in row:",carImageRanges - rowstart)
        
    print(type(jobject["images"]))            
    jobject["images"] = images
    
    print(json.dumps(jobject, indent = 4))