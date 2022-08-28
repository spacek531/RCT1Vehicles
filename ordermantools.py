import re
import json
import pathlib
"""Written by Spacek531 for manipulation of jobjectson files for the purposes of creating RCT1 rides in OpenRCT2. Paste a string and all numbers will be incremented by the total range, for the number of repetitions specified."""

"""
exec(open("D:/documents/openrct2/custom rides/rct1 project/object/ordermantools.py").read())

"""
def aresame(a,b):
    return a == b

"""accepts individual images only, no image ranges"""
def ConsolidateImages(imageList):
    for i in range(len(imageList)):
        if type(imageList[i]) != type(""):
            continue
class ImageConsolidator:
    def __init__(self, imageList):
        self.previousPrefix = None
        self.currentIndex = 0
        self.runStartIndex = 0
        self.runStartNumber = 0
        self.currentNumber = 0
        self.onARun = False
        self.getn = re.compile(r"(?<=[[])(\d+)(?=[\]])")
        self.getp = re.compile(r".*(?=[[])")
        while not self.increment(imageList):
            pass
        
    def endRun(self, imageList):
        if not self.onARun:
            return
        imageList[self.runStartIndex] = "{0}[{1}..{2}]".format(self.previousPrefix,self.runStartNumber, self.currentNumber)
        del imageList[self.runStartIndex+1 : self.currentIndex ]
        self.previousPrefix = None
        self.currentIndex = self.runStartIndex + 1
        self.runStartIndex = 0
        self.currentNumber = 0
        self.runStartNumber = 0
        self.runStartIndex = 0
        self.onARun = False
        
    def increment(self, imageList):
        if self.currentIndex >= len(imageList):
            self.endRun(imageList)
            return 1
        if type(imageList[self.currentIndex]) != str:
            self.endRun(imageList)
            self.currentIndex += 1
            return 0
        prex = self.getp.search(imageList[self.currentIndex])
        prex = prex and prex.group(0)
        nrex = self.getn.search(imageList[self.currentIndex])
        nrex = nrex and int(nrex.group(0))
        
        if nrex and prex:
            if aresame(prex, self.previousPrefix) and aresame(nrex, self.currentNumber + 1):
                self.onARun = True
                self.currentNumber = nrex
            else:
                self.endRun(imageList)
                self.previousPrefix = prex
                self.runStartIndex = self.currentIndex
                self.runStartNumber = nrex
                self.currentNumber = nrex
            self.currentIndex += 1
            return 0
        self.endRun(imageList)
        self.currentIndex += 1
        return 0

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
    images = []
    for s in jobject:
        if type(s) == str:
            if len(s) == 0:
                images.append(s)
                continue
            prefix = s.split("[")[0]
            rng = GetRange(s.split("[")[1])
            if len(rng) > 0:
                for i in rng:
                    images.append(prefix+"["+str(i)+"]")
            else:
                images.append(s)
        else:
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
    def __init__(self, name, defaultPrecision, reversePower, reverseRepetitions, specialFunction = None):
        self.specialFunction = specialFunction
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

def corkscrewFunction(images, precision, carImageRanges):
    print("Corkscrew function called", precision, carImageRanges)
    # print(images, precision, carImageRanges)
    Cut(images, carImageRanges, precision * 10, 0)
    Cut(images, carImageRanges + precision * 10, precision * 10, 0)
    for j in range(0,precision * 20,precision):
        Cut(images, carImageRanges + j, precision, 0)

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
    SpriteGroup("flatBanked67", 4, 1, 1),
    SpriteGroup("flatBanked90", 4, 1, 1),
    SpriteGroup("inlineTwists", 4, 1, 3),
    SpriteGroup("slopes12Banked22",32, 2, 1),
    SpriteGroup("slopes8Banked22", 4, 2, 1),
    SpriteGroup("slopes25Banked22", 4, 2, 1),
    SpriteGroup("slopes25Banked45", 32, 2, 1),
    SpriteGroup("slopes12Banked45", 4, 2, 1),
    SpriteGroup("corkscrews", 4, 0, 20, corkscrewFunction),
    SpriteGroup("restraintAnimation", 4, 0, 3),
    SpriteGroup("curvedLiftHill", 32, 0, 1)
]

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
    images = ScrapeImages(jobject["images"])
    if len(images) == 0:
        return
    fimages = ["" for _ in range(len(images))]
    if jobject.get("noCsgImages"):
        fimages = ScrapeImages(jobject["noCsgImages"])
        
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
                print(spriteGroup.name, spriteGroups[spriteGroup.name], spriteGroup.specialFunction)
                if spriteGroup.specialFunction is not None:
                    spriteGroup.specialFunction(images, precision, carImageRanges)
                    spriteGroup.specialFunction(fimages, precision, carImageRanges)
                    carImageRanges += spriteGroup.sprites(precision)
                else:
                    for i in range(spriteGroup.reverseRepetitions):
                        Cut(images, carImageRanges, spriteGroup.group(precision),spriteGroup.reversePower)
                        Cut(fimages, carImageRanges, spriteGroup.group(precision),spriteGroup.reversePower)
                        carImageRanges += spriteGroup.group(precision)
    ImageConsolidator(images)
    jobject["images"] = images
    if jobject.get("noCsgImages"):
        ImageConsolidator(fimages)
        jobject["noCsgImages"] = fimages
    
    print(json.dumps(jobject, indent = 4))
    
OldSpriteGroupOrder = [
    "flat",
    "gentleSlopes",
    "steepSlopes",
    "verticalSlopes",
    "diagonalSlopes",
    "flatBanked",
    "inlineTwists",
    "flatToGentleSlopeBankedTransitions",
    "diagonalGentleSlopeBankedTransitions",
    "gentleSlopeBankedTransitions",
    "gentleSlopeBankedTurns",
    "flatToGentleSlopeWhileBankedTransitions",
    "corkscrews",
    "restraintAnimation"]

OldSpriteGroupLengths = {
    "flat": 32,
    "gentleSlopes": 72, 
    "steepSlopes": 80,
    "verticalSlopes": 116,
    "diagonalSlopes": 24,
    "flatBanked": 80,
    "inlineTwists": 40,
    "flatToGentleSlopeBankedTransitions": 128,
    "diagonalGentleSlopeBankedTransitions": 16,
    "gentleSlopeBankedTransitions": 16,
    "gentleSlopeBankedTurns": 128,
    "flatToGentleSlopeWhileBankedTransitions": 16,
    "corkscrews": 80,
    "restraintAnimation": 12
    }

def GetOffsets(spriteGroups, animationFrames, offset):
    m = {}
    highestindex = 0
    for group in spriteGroups:
        start = offset
        sindex = OldSpriteGroupOrder.index(group)
        highestindex = max(sindex, highestindex)
        for i in reversed(range(sindex)):
            if spriteGroups.get(OldSpriteGroupOrder[i], None):
                #print("Adding sprites from", OldSpriteGroupOrder[i])
                start += OldSpriteGroupLengths[OldSpriteGroupOrder[i]] * animationFrames
        #print("Sprite Group {0} start {1}".format(group, start))
        m[group] = start
    m["length"] = OldSpriteGroupLengths[OldSpriteGroupOrder[highestindex]] * animationFrames
    for i in reversed(range(highestindex)):
        if OldSpriteGroupOrder[i] in spriteGroups:
            m["length"] += OldSpriteGroupLengths[OldSpriteGroupOrder[i]] * animationFrames
    #print("Car sequence start, end",offset, offset + m["length"])
    return m

class FallbackSpriteGroup:
    def __init__(self, newgroup, oldgroup, startOffset, precision, repetitions):
        self.newGroup = newgroup
        self.oldGroup = oldgroup
        self.startOffset = startOffset
        self.precision = precision
        self.repetitions = repetitions
        
    def getIndices(self, animationFrames, newPrecision):
        payload = []
        for i in range(self.repetitions):
            for j in range(0,self.precision * animationFrames, animationFrames * self.precision // newPrecision):
                for k in range(animationFrames):
                    payload.append((self.startOffset + i * self.precision)*  animationFrames + j + k)
        return payload
    
SPMap = [
    FallbackSpriteGroup("slopeFlat", "flat", 0, 32, 1),
    FallbackSpriteGroup("slopes12", "gentleSlopes", 0, 4, 2),
    FallbackSpriteGroup("slopes25", "gentleSlopes", 8, 32, 2),
    FallbackSpriteGroup("slopes42", "steepSlopes", 0, 8, 2),
    FallbackSpriteGroup("slopes60", "steepSlopes", 16, 32,2),
    FallbackSpriteGroup("slopes75", "verticalSlopes", 0, 4, 2),
    FallbackSpriteGroup("slopes90", "verticalSlopes", 8, 32, 2),
    FallbackSpriteGroup("slopesLoop", "verticalSlopes", 72, 4, 10),
    FallbackSpriteGroup("slopeInverted", "verticalSlopes", 112, 4, 1),
    FallbackSpriteGroup("slopes8", "diagonalSlopes", 0, 4, 2),
    FallbackSpriteGroup("slopes16", "diagonalSlopes", 8, 4, 2),
    FallbackSpriteGroup("slopes50", "diagonalSlopes", 16, 4, 2),
    FallbackSpriteGroup("flatBanked22", "flatBanked", 0, 8, 2),
    FallbackSpriteGroup("flatBanked45", "flatBanked", 16, 32, 2),
    FallbackSpriteGroup("flatBanked67", "inlineTwists", 0, 4, 2),
    FallbackSpriteGroup("flatBanked90", "inlineTwists", 8, 4, 2),
    FallbackSpriteGroup("inlineTwists", "inlineTwists", 16, 4, 10),
    FallbackSpriteGroup("slopes12Banked22", "flatToGentleSlopeBankedTransitions", 0, 32, 4),
    FallbackSpriteGroup("slopes8Banked22", "diagonalGentleSlopeBankedTransitions", 0, 4, 4),
    FallbackSpriteGroup("slopes25Banked22", "gentleSlopeBankedTransitions", 0,4, 4),
    FallbackSpriteGroup("slopes25Banked45", "gentleSlopeBankedTurns", 0,32, 4),
    FallbackSpriteGroup("slopes12Banked45", "flatToGentleSlopeWhileBankedTransitions", 0,4, 4),
    FallbackSpriteGroup("corkscrews", "corkscrews", 0, 4, 20),
    FallbackSpriteGroup("restraintAnimation", "restraintAnimation", 0, 4, 3)
]

def loadJSON(inputfile):
    if not inputfile.exists():
        raise Exception("Inputfile does not exist")
    try:
        with inputfile.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print("Could not load JSON file:", e)

def writeJSON(outputfile, data):
    if not outputfile.exists():
        raise Exception("outputfile does not exist")
    try:
        with outputfile.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Could not write JSON file:", e)

def GetVerticalFrames(car):
    flags = car
    VEHICLE_ENTRY_FLAG_OVERRIDE_NUM_VERTICAL_FRAMES = flags.get("overrideNumberOfVerticalFrames")
    VEHICLE_ENTRY_FLAG_SPINNING_ADDITIONAL_FRAMES = flags.get("hasAdditionalSpinningFrames")
    VEHICLE_ENTRY_FLAG_VEHICLE_ANIMATION = flags.get("hasVehicleAnimation")
    VEHICLE_ENTRY_FLAG_DODGEM_INUSE_LIGHTS = flags.get("hasDodgemInUseLights")
    VEHICLE_ENTRY_ANIMATION_OBSERVATION_TOWER = car.get("animation") == 6
    numVerticalFrames = 1;
    if VEHICLE_ENTRY_FLAG_OVERRIDE_NUM_VERTICAL_FRAMES:
        numVerticalFrames = car.get("numVerticalFramesOverride",0)
    elif not VEHICLE_ENTRY_FLAG_SPINNING_ADDITIONAL_FRAMES:
        if VEHICLE_ENTRY_FLAG_VEHICLE_ANIMATION and not VEHICLE_ENTRY_ANIMATION_OBSERVATION_TOWER:
            if not VEHICLE_ENTRY_FLAG_DODGEM_INUSE_LIGHTS:
                numVerticalFrames = 4;
            else:
                numVerticalFrames = 2;
        else:
            numVerticalFrames = 1;
    else:
        numVerticalFrames = 32;
    return numVerticalFrames;    
    
def GetHorizontalFrames(car):
    flags = car
    VEHICLE_ENTRY_FLAG_SWINGING = flags.get("hasSwinging", None)
    VEHICLE_ENTRY_FLAG_SLIDE_SWING = flags.get("useSlideSwing", None)
    VEHICLE_ENTRY_FLAG_SUSPENDED_SWING = flags.get("useSuspendedSwing", None)
    VEHICLE_ENTRY_FLAG_WOODEN_WILD_MOUSE_SWING = flags.get("useWoodenWildMouseSwing", None)
    numHorizontalFrames = 1
    if VEHICLE_ENTRY_FLAG_SWINGING:
        if not VEHICLE_ENTRY_FLAG_SUSPENDED_SWING and not VEHICLE_ENTRY_FLAG_SLIDE_SWING:
            if VEHICLE_ENTRY_FLAG_WOODEN_WILD_MOUSE_SWING:
                numHorizontalFrames = 3
            else:
                numHorizontalFrames = 5
        elif not VEHICLE_ENTRY_FLAG_SUSPENDED_SWING or not VEHICLE_ENTRY_FLAG_SLIDE_SWING:
            numHorizontalFrames = 7
        else:
            numHorizontalFrames = 13
    else:
        numHorizontalFrames = 1

    return numHorizontalFrames;

def GetFallbackImages(inputfile, fallbackfile):
    
    inputfile = pathlib.Path(inputfile)
    fallbackfile = pathlib.Path(fallbackfile)
    newf = loadJSON(inputfile)
    falf = loadJSON(fallbackfile)
    if not newf:
        print("Newf Nonetype")
    if not falf:
        print("Falf Nonetype")
    if not newf or not falf:
        raise Exception("Newf or Falf are Nonetype")
    myCars = newf["properties"]["cars"]
    theirCars = falf["properties"]["cars"]
    if type(myCars) == type(dict()):
        myCars = [myCars]
    if type(theirCars) == type(dict()):
        theirCars = [theirCars]
    if len(myCars) > len(theirCars):
        raise Exception("More cars in input file than in fallback file")
    
    theirImages = ScrapeImages(falf["images"])
    myImages = [ newf["images"][0], newf["images"][1], newf["images"][2] ]
    fpointer = 3 # the sprite of the current car being served
    carno = 0 # the fallback car referenced
    for car in myCars:
        ocar = theirCars[carno]
        if car.get("numSeatRows",0) > ocar.get("numSeatRows",0):
            raise Exception("Car {0} has more seat rows than fallback car".format(carno))
        
        animationFrames = GetHorizontalFrames(car) * GetVerticalFrames(car)
        if not ocar.get("frames"):
            print("Skipping car {0} - frames field not present in othercar".format(carno))
            continue
        otherCarSpriteOffsets = GetOffsets(ocar["frames"], animationFrames, fpointer)
        for i in range(1 + car.get("numSeatRows",0)):
            newOffset = i * otherCarSpriteOffsets["length"]
            for group in SPMap:
                precision = car["spriteGroups"].get(group.newGroup, 0)
                if precision > 0:
                    manifest = group.getIndices(animationFrames, precision)
                    for index in manifest:
                        try:
                            myImages.append(theirImages[newOffset + otherCarSpriteOffsets[group.oldGroup] + index])
                            #print("Add othercar sprite {0}: {4} (car {1} repetition {2} sprite group {3})".format(newOffset + otherCarSpriteOffsets[group.oldGroup] + index, carno, i, group.newGroup, theirImages[newOffset + otherCarSpriteOffsets[group.oldGroup] + index]))
                        except Exception as e:
                            print("Could not add othercar sprite {0} (car {1} repetition {2} sprite group {3})".format(newOffset + otherCarSpriteOffsets[group.oldGroup] + index, carno, i, group.newGroup), e)
                        

        carno += 1
        fpointer += otherCarSpriteOffsets["length"] * (ocar.get("numSeatRows",0) + 1)
    
    ImageConsolidator(myImages)
    newf["noCsgImages"] = myImages
    
    writeJSON(inputfile, newf)
    print("Creating fallbacks complete")
