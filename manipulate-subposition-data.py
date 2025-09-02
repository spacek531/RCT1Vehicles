import json
import string
from enum import Enum

subpositiondataPath = "D:/Documents/GitHub/OpenRCT2/src/openrct2/ride/VehicleSubpositionData.cpp"
new2 = "D:/Documents/GitHub/OpenRCT2/src/openrct2/ride/New 2.txt"
outputPath = "D:/Documents/GitHub/OpenRCT2/src/openrct2/ride/VehicleSubpositionData2.txt"

maxLineLength = 175
    
class VehiclePitch(Enum):
    flat = 0
    up12 = 1
    up25 = 2
    up42 = 3
    up60 = 4
    down12 = 5
    down25 = 6
    down42 = 7
    down60 = 8
    up75 = 9
    up90 = 10
    up105 = 11
    up120 = 12
    up135 = 13
    up150 = 14
    up165 = 15
    inverted = 16
    down75 = 17
    down90 = 18
    down105 = 19
    down120 = 20
    down135 = 21
    down150 = 22
    down165 = 23
    corkscrewUpRight0 = 24
    corkscrewUpRight1 = 25
    corkscrewUpRight2 = 26
    corkscrewUpRight3 = 27
    corkscrewUpRight4 = 28
    corkscrewDownLeft0 = 29
    corkscrewDownLeft1 = 30
    corkscrewDownLeft2 = 31
    corkscrewDownLeft3 = 32
    corkscrewDownLeft4 = 33
    corkscrewUpLeft0 = 34
    corkscrewUpLeft1 = 35
    corkscrewUpLeft2 = 36
    corkscrewUpLeft3 = 37
    corkscrewUpLeft4 = 38
    corkscrewDownRight0 = 39
    corkscrewDownRight1 = 40
    corkscrewDownRight2 = 41
    corkscrewDownRight3 = 42
    corkscrewDownRight4 = 43
    upHalfHelixLarge = 44
    upHalfHelixSmall = 45
    downHalfHelixLarge = 46
    downHalfHelixSmall = 47
    upQuarterHelix = 48
    downQuarterHelix = 49
    up8 = 50
    up16 = 51
    up50 = 52
    down8 = 53
    down16 = 54
    down50 = 55
    invertingDown25 = 56
    invertingDown42 = 57
    invertingDown60 = 58
    curvedLiftHillUp = 59
    curvedLiftHillDown = 60
    
class VehicleRoll(Enum):
    unbanked = 0
    left22 = 1
    left45 = 2
    right22 = 3
    right45 = 4
    left67 = 5
    left90 = 6
    left112 = 7
    left135 = 8
    left157 = 9
    right67 = 10
    right90 = 11
    right112 = 12
    right135 = 13
    right157 = 14
    invertingUnbanked = 15
    invertingLeft22 = 16
    invertingLeft45 = 17
    invertingRight22 = 18
    invertingRight45 = 19
    invertingLeft67 = 20
    invertingLeft90 = 21
    invertingLeft112 = 22
    invertingLeft135 = 23
    invertingLeft157 = 24
    invertingRight67 = 25
    invertingRight90 = 26
    invertingRight112 = 27
    invertingRight135 = 28
    invertingRight157 = 29

class SubpositionDatum:
    def __init__(self, inputString):
        self.string = ""
        if "MINI_GOLF_STATE" in inputString or "MINI_GOLF_ANIMATION" in inputString:
            self.string = inputString.strip()
            self.x = ""
            self.y = ""
            self.z = ""
            self.orientation = ""
            self.pitch = ""
            self.roll = ""
            return
        
        elems = [ a.strip() for a in inputString.split(",")]
        self.x = int(elems[0])
        self.y = int(elems[1])
        self.z = int(elems[2])
        self.orientation = int(elems[3])
        
        if elems[5].isdigit():
            self.pitch = VehiclePitch(int(elems[4]))
            self.roll = VehicleRoll(int(elems[5]))
        else:
            self.pitch = VehiclePitch[elems[4]]
            self.roll = VehicleRoll[elems[5]]
    
    def getWidths(self, widths):
        lenx = len(str(self.x))
        leny = len(str(self.y))
        lenz = len(str(self.z))
        leno = len(str(self.orientation))
        lenp = 0
        lenr = 0
        lens = len(self.string)
        if self.string == "":
            lenp = len(VehiclePitch(self.pitch).name)
            lenr = len(VehicleRoll(self.roll).name)
            lens = lenx + leny + lenz + leno + lenp + lenr + 8 # 8 is how many actual characters the format string has
        
        widths[0] = max(widths[0], lenx)
        widths[1] = max(widths[1], leny)
        widths[2] = max(widths[2], lenz)
        widths[3] = max(widths[3], leno)
        widths[4] = max(widths[4], lenp)
        widths[5] = max(widths[5], lenr)
        widths[6] = max(widths[6], lens)
            
    def serialize(self, widths):
        if self.string != "":
            return f"{self.string:>{widths[6]}}"
        asdf = f"{{{self.x:>{widths[0]}},{self.y:>{widths[1]}},{self.z:>{widths[2]}},{self.orientation:>{widths[3]}},{VehiclePitch(self.pitch).name:>{widths[4]}},{VehicleRoll(self.roll).name:>{widths[5]}} }}"
        return f"{asdf:>{widths[6]}}"

class SubpositionData:
    def __init__(self, name):
        self.name = name
        self.data = []
        
    def append(self, inputString):
        try:
            self.data.append(SubpositionDatum(inputString))
        except Exception as e:
            print("PARSER FAILURE!")
            print("name:", self.name)
            print("data:", self.data)
            print("inputString:",inputString)
            raise Exception("Parse error!")
        
    def serialize(self, tabSpaces = 0):
        widths = [0 for _ in range(7)]
        for datum in self.data:
            datum.getWidths(widths)
        widths = [a+1 for a in widths]
        outPut = "    "+" "*tabSpaces
        numColumns = (maxLineLength-4-tabSpaces)//widths[6]
        for i in range(len(self.data)):
            outPut += self.data[i].serialize(widths)
            if i == len(self.data) - 1:
                break
            if ((i+1)%numColumns) == 0:
                outPut += ",\n    "+" "*tabSpaces
            else:
                outPut += ", "
        return self.name + ", {\n"+outPut+",\n"+" "*tabSpaces+"}"

def performActions(subpositionData):
    pass

class SubpositionDataReader:
    def __init__(self, inputFileName, outputFileName):
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        self.outputFP = None
        
        self.subpositionData = None
        self.datumBuffer = ""
        self.datumBufferHasData = False
        self.depth = 0
        self.tabSpaces = 0
        
    def quitWithError(self, error):
        if self.outputFP:
            self.outputFP.close()
        raise Exception(error)
    
    def writeOut(self, text):
        if self.outputFP:
            self.outputFP.write(text)
        else:
            raise IOException("File is missing!")
    
    def parseDatum(self):
        if not self.datumBufferHasData:
            return
        #print("parsing datum","\""+self.datumBuffer+"\"")
        if self.datumBuffer == "":
            return
        try:
            self.subpositionData.append(self.datumBuffer)
        except Exception as e:
            self.quitWithError(e)
    
    def performActions(self):
        performActions(self.subpositionData)
        self.writeOut(self.subpositionData.serialize(self.tabSpaces))
        
    def parseLine(self, line):
        if "CREATE_VEHICLE_INFO(" in line and line[0] != "#":
            if self.depth != 0:
                self.quitWithError("Encountered new VEHICLE_CREATE_INFO but depth was nonzero!")
            
            self.tabSpaces = line.index("CREATE_VEHICLE_INFO(")
            endOfString = self.tabSpaces + 20
            
            inputBuffer = line[endOfString:]
            
            self.subpositionData = SubpositionData(inputBuffer[:inputBuffer.index(",")].strip())
            
            self.writeOut(line[:endOfString])
            self.depth = 1
            for char in inputBuffer:
                self.parseCharacter(char)
        else:
            if self.depth > 0:
                for char in line:
                    self.parseCharacter(char)
            else:
                self.writeOut(line)
    
    def resetBuffer(self):
        self.datumBuffer = ""
        self.datumBufferHasData = False
    
    def appendBuffer(self,text):
        self.datumBuffer += text
        if text != " " and text != "\n":
            self.datumBufferHasData = True
    
    def parseCharacter(self, char):
        if char == "," and self.depth == 2:
            self.parseDatum()
            self.resetBuffer()
            
        elif char in "({":
            self.depth += 1
            if char == "{":
                self.resetBuffer()
            elif char == "(" and self.depth == 3:
                self.appendBuffer(char)
                    
        elif char in ")}":
            self.depth -= 1
            if char == "}":
                self.parseDatum()
                self.resetBuffer()
            elif char == ")":
                self.datumBuffer += char
                if self.depth == 0:
                    self.performActions()
        else:
            self.appendBuffer(char)
        if self.depth == 0:
            self.writeOut(char)
        
    def parse(self):
        with open(self.inputFileName,"r+") as file:
            self.outputFP = open(self.outputFileName,"w+")
            while True:
                line = file.readline()
                self.parseLine(line)
                if line == '':
                    if self.depth != 0:
                        print("Reached EOF with nonzero depth level!")
                    else:
                        print("Reached EOF")
                    self.outputFP.close()
                    return

a = SubpositionDataReader(subpositiondataPath, outputPath)
#a = SubpositionDataReader(new2, outputPath)
a.parse()