from music21 import *
import sys
import copy
import operator
import Tinctoris3

# Takes a musicXML file as input. Expects four voices.
# Naples 6 works since only four voices active at a time.
# Analyses the cantus-tenor hard-coded around line 590.
# Changing pair analysis requires placing a different part in the 'cantus' etc.

# Returns a list of contrapuntal anomalies i.e. progressions inconsistent with the Liber
# and a score-form that contains a contrapuntal reduction on the inner parts
# and a version of the original note values on the outer staves.

# Creates a VoicePair object (testObject) consisting of an array of CPFragment objects by
# segmenting the assigned cantus firmus voice and matching with notes from remaining voices
# at same offsets.

# Third and fourth voices retained only for testing consonance of fourths.

# Call to resolveChain method has testObject step through and resolve each fragment in turn,
# with the closing consonance of one fragment providing the opening consonance of the next.

# Weaknesses: segments cantus firmus without reference to partner voice
# Does not account for changees in mensuration
# Fragile if presented with unexpected notation at times: e.g. consecutive semiminim rests in cf break it.
        
class CPFragment(object):           # Object that holds each component segment of a passage
    'An object for handling bites of counterpoint'
    
    def __init__(self, notelist, cpStream, uSub, lSub, startOffset, duration, index, position):
        self.notelist = notelist
        self.cpstream = cpStream
        self.position = position #offset of cfnote from start of parent stream
        self.index = index
        self.prevConsonance = -1 #set by resolveChain. Represents initial value only. Use consonance for working values
        self.cache = []
        self.cpOut = stream.Part()
        self.cfOut = stream.Part()
        self.progression = []
        self.duration = duration
        self.prevCF = note.Note()
        self.prevFrame = note.Note()
        self.nextFrame = note.Note()
        self.indices = []
        self.resultFlag = False
        self.pitchOffset = 0
        self.uSub = uSub
        self.lSub = lSub
        self.consonance = -144 # Working/changeable version of prevConsonance. Set as impossible value to mark first use.
        self.notSet = []
        self.resultSet = []
        
    def analyseCRhythm(self, tStream, mStream): #add something to check for rests and segment accordingly.
        indices = []
        
        if len(tStream) > 1:
            if tStream[0].duration.quarterLength != 2:
                return([1])
            
            elif tStream[1].duration.quarterLength == 2 and Tinctoris3.getInterval(tStream[1], tStream[0]) == Tinctoris3.getInterval(mStream[1], mStream[0]):
                return([1])
            
            else:
                return([2,2,(tStream[-1].offset + tStream[-1].duration.quarterLength)])
        
        if len(mStream) == 1:
            return([1])
        
        item = tStream.flat.notesAndRests[0]
        if item.isRest:
            return([1])
        
        if item.duration.quarterLength == 6:
            if len(mStream)< 2:
                return([1])
            elif mStream[0].duration.quarterLength == 2 and mStream[1].duration.quarterLength == 2:
                return([3, 2, 4, (tStream[-1].offset + tStream[-1].duration.quarterLength)])
            elif mStream.duration.quarterLength > 2:
                return ([2, 4, (tStream[-1].offset + tStream[-1].duration.quarterLength)])

            else:
                return([2, 2, (tStream[-1].offset + tStream[-1].duration.quarterLength)])
        
        if item.duration.quarterLength in {8,12}:
            indices.append(item.duration.quarterLength/4)
            x = 1
            while x * 4 < item.duration.quarterLength:
                indices.append(x * 4)
                x += 1
            indices.append((tStream[-1].offset + tStream[-1].duration.quarterLength))
            return(indices)
           
        

        if item.duration.quarterLength == 2:
            return([1])
        
        if item.duration.quarterLength == 4:
            if len(mStream) == 2 and mStream[0].duration.quarterLength == 2:
                return ([1, 2, (tStream[-1].offset + tStream[-1].duration.quarterLength)])
            else:
                return([1])

        print("Something we didn't account for in the analyse function", self.position) # Can't happen.
        return([1])  
            
    def findCFNote(self, stream): # creates sorted dictionary of potential cf notes, returns longest. Unreliable on crotchet pairs.
        if len(stream) == 1:
            return stream[0]
        
        dict1 = {}
        for subject in stream:
            if subject.isRest:
                continue
            if subject.nameWithOctave in dict1:
                dict1[subject.nameWithOctave] += subject.duration.quarterLength
            else:
                dict1[subject.nameWithOctave] = subject.duration.quarterLength
        
        list1 = sorted(dict1.items(), key=operator.itemgetter(1), reverse = True)
        temp = note.Note(list1[0][0])
        temp.duration.quarterLength = stream[-1].offset + stream[-1].duration.quarterLength
        return (temp)
        
    def fragStream(self, aStream, offOne, offTwo): #returns contents of stream between two offsets
    
        x = offOne
        rStream = stream.Part()
        
        while x < offTwo:
            temp = aStream.flat.notesAndRests.getElementAtOrBefore(x)
            y = x - temp.offset
            rStream.append(copy.deepcopy(temp))
            if y > 0:
                rStream.flat.notesAndRests[-1].duration.quarterLength -= y
                
            x += rStream.flat.notesAndRests[-1].duration.quarterLength 
        
            if 0.9 < (x - int(x)) < 1:
                x = int(x) + 1
                
        if x > offTwo:
            rStream.flat.notesAndRests[-1].duration.quarterLength -= x - offTwo
            
        return(rStream)

    def resolveBite(self, cf, cp, upper, lower, lFrame, rFrame): #takes four streams (upper/lower for fourth adjudication)
        # Returns list (sorted?) of pitches as keys with weighting as favoured cp note
        
        
        if cp.flat.notesAndRests[0].isRest:
            self.consonance = -1
        
        if self.consonance == -144:
            self.consonance = self.prevConsonance
        
        if self.consonance == -1 or self.consonance %7 == 3 and self.consonance > 0 \
                or self.consonance % -7 == -3 and self.consonance < 0:
            theSet = Tinctoris3.konsonances
            
        elif not cf.isRest and not self.prevCF.isRest:
            steps = Tinctoris3.getInterval(cf, self.prevCF) #reduce everything to single octave - convert 6ths to 3rds etc.
            if steps > 4:
                x = steps % 7
                if x > 4:
                    x -= 7
                steps = x
            
            if steps < -4:
                x = steps % -7
                if x < -4:
                    x += 7
                steps = x
                
            theSet = Tinctoris3.progressions[Tinctoris3.konsonanzen[self.consonance]][steps + 4]
        
        if theSet == Tinctoris3.konsonances:
            testSet = Tinctoris3.filterNotes(cp, cf, cf, theSet, upper, lower)
        else:
            testSet = Tinctoris3.filterNotes(cp, self.prevCP, cf, theSet, upper, lower)
        rSet = {}
        
        for subject in cp:              # one pass to create list of permitted notes weighted by duration
            if subject.isRest:
                stri = 'rest'
                
            else:
                stri = subject.nameWithOctave
                if len(stri) > 2:
                    stri = stri[0] + stri[-1]
            if stri in testSet or stri == 'rest':
                if stri in rSet:
                    rSet[stri] += subject.duration.quarterLength
                else:
                    rSet[stri] = subject.duration.quarterLength
        
        if lFrame.isRest:
            q = 0
            while lFrame.isRest and q < len(cp):
                lFrame = cp.flat.notesAndRests[q] 
                q+= 1
        if lFrame.isRest:
            rList = []
            rList.append(['rest', 4])
            return(rList)     
                    
        if len(lFrame.nameWithOctave) > 2:
            lFrame.nameWithOctave = lFrame.nameWithOctave[0] + lFrame.nameWithOctave[-1]   
        
        if len(rSet) > 1:
            if rFrame.isRest and self.nextFrame.isRest:
                rFrame = cp.flat.notesAndRests[-1]
            elif rFrame.isRest:
                rFrame = self.nextFrame
            
            if  rFrame.isRest:
                rFrame = lFrame
            else:
                if len(rFrame.nameWithOctave) > 2:
                    rFrame.nameWithOctave = rFrame.nameWithOctave[0] + rFrame.nameWithOctave[-1]   
            
                                   
            pitchOffset = (Tinctoris3.voces[lFrame.nameWithOctave] + Tinctoris3.voces[rFrame.nameWithOctave])/2
            
            for subject in rSet:        # another pass to weight by pitch offset (i.e. closest to mid-point weighted higher)
                if subject == 'rest':   # Perhaps reimplement as a tiebreaker only.
                    continue
                #if pitchOffset == Tinctoris3.voces[subject]:
                    #pass
                else:
                    x = abs(int(Tinctoris3.voces[subject] - pitchOffset))
                    if x < 5:
                        q = (5-float(x))/5
                    else:
                        q = 0.1
                        
                    rSet[subject] *= q

        rList = sorted(rSet.items(), key=operator.itemgetter(1), reverse = True)
        return(rList)
    
    def __iter__(self):
        self.cache_index = 0
        return self
    
    def __next__(self):
        self.cache_index += 1
        if len(self.cache) >= self.cache_index:
            return self.cache[self.cache_index - 1]
        else:
            raise StopIteration
 
        
    def resolveFragment(self):     #resolves contrapuntal movement in fragment, returns last resulting consonance & cf and contrapuntal notes
        result = []

        # Should be two steps: analyse the fragment for number of cp notes, set cfOut accordingly.
        
        self.indices = self.analyseCRhythm(self.notelist, self.cpstream)
        # print(self.position/4 + 1)   # debugging
        x = 0
        while x < self.indices[0]:
            self.notSet.append([])
            x += 1

        lFrame = self.prevFrame
        rFrame = note.Note()
        if self.indices[0] == 1:
            cfNote = self.findCFNote(self.notelist)
            cfNote.duration.quarterLength = self.duration
            if cfNote.isRest:
                self.cpOut = self.cpstream
                self.cfOut.append(cfNote)
                self.cfOut[-1].duration.quarterLength = self.duration
                return (-1, self.cfOut[-1], self.cpOut[-1], 0)
            
            
            result = self.resolveBite(cfNote, self.cpstream, self.uSub, self.lSub, self.prevFrame, self.nextFrame)#need to determin correct cf note here.
            self.resultSet.append([result])
            self.prevCF = cfNote
            if len(result) > 0:
                if result[0][0] == 'rest':
                    temp = note.Rest()
                else:
                    temp = note.Note(result[0][0])
                temp.duration.quarterLength = self.duration
                cfNote.duration.quarterLength = temp.duration.quarterLength
                self.cfOut.append(cfNote)
                self.cpOut.append(temp)
                self.prevCP = temp
                if  temp.isRest:
                    self.consonance = -1
                    return (self.consonance, self.notelist[0], temp, 0)
                else:
                    self.consonance = Tinctoris3.getInterval(temp, cfNote)
                    return (self.consonance, cfNote, temp, 0)
            else:
                print('Something rotten in the state of Denmark', self.position/4 + 1 )
                cfNote.duration.quarterLength = self.duration
                self.cfOut.append(cfNote)
                temp = note.Rest()
                temp.duration.quarterLength = self.duration
                self.cpOut.append(temp)   
                return (-1, cfNote, note.Rest(),1)
        else:
            etest = 0
            x = 0
            y = 1
            
            while y < len(self.indices):
                if y < len(self.indices) - 1:
                    rFrame = self.cpstream.flat.notesAndRests.getElementAtOrBefore(self.indices[y] + .125)
                    if rFrame.isRest:
                        rFrame = self.cpstream.flat.notesAndRests.getElementAtOrBefore(self.indices[y] - .125)
                else:
                    rFrame = self.nextFrame
                
                if rFrame.isRest:
                    q = len(self.cpstream) - 1
                    while self.cpstream.flat.notesAndRests[q].isRest and q > 0:
                        q -=1
                    rFrame = self.cpstream[q]
                    
                cfNote = self.findCFNote(self.fragStream(self.notelist, x, self.indices[y]))
                if cfNote.isRest:
                    self.cpOut = self.fragStream(self.cpsteam, x, self.indices[y])
                    self.cfOut.append(note.Rest())
                    self.cfOut[-1].duration.quarterLength = self.indices[y] - x
                    self.consonance = -1
                    
                else:
                    result = self.resolveBite(cfNote, \
                        self.fragStream(self.cpstream, x, self.indices[y]), self.fragStream(self.uSub, x, self.indices[y]), \
                        self.fragStream(self.lSub, x, self.indices[y]), lFrame, rFrame)
                    self.resultSet.append([result])
                    lFrame = self.cpstream.flat.notesAndRests.getElementAtOrBefore(self.indices[y] - .125)
                
                self.prevCF = cfNote   
                z = 0
                
                if len(result) > 0:
                    if result[0][0] == 'rest':
                        temp = note.Rest()
                    else:
                        temp = note.Note(result[0][0])
                    temp.duration.quarterLength = self.duration
                    
                else:
                    etest = 1
                    print("Result missing at fragment beginning ", self.position/4 + 1, " bite number",  y)
                    temp = note.Rest()
                    
                temp.duration.quarterLength = cfNote.duration.quarterLength
                
                self.cfOut.append(cfNote)
                self.cpOut.append(temp)
                self.prevCP = temp
                
                aNote = self.notelist.flat.notesAndRests.getElementAtOrBefore(x)
                if aNote.isRest or self.cpOut[-1].isRest:
                    self.consonance = -1
                else:
                    self.consonance = Tinctoris3.getInterval(self.cpOut[-1], self.cfOut[-1])
                
                if y < len(self.indices):
                    x = self.indices[y]
                else:
                    x = self.duration
                
                y += 1
                
        return(self.consonance, self.cfOut[-1], self.cpOut[-1], etest)

           
class VoicePair(object):        # Object that holds passage in voice-pair form.
    
    def __init__(self, tenorist, cantorist, altist, bassist):
         

        self.tenorist = tenorist
        self.cantorist = cantorist
        self.thisPair = []
        maxOffset = tenorist[(len(tenorist) - 1)].offset # the outer limits
        # maxOffset = 156 # hardcoded for testing
        
        localOffset = 0
        noteIndex = 0
        index = 0
        
        
        while localOffset < maxOffset:
            
            rUnit = 0 # holds length of cf-based contrapuntal fragment
            
            suspEnding = 0
            
            cfNote = stream.Part()
            cpStream = stream.Part()
            uSub = stream.Part()
            lSub = stream.Part()
            z = tenorist[noteIndex].offset
            
            while rUnit < 2 or rUnit % 2 > 0: #find cf values divisible by minims

                cfNote.append(tenorist[noteIndex])
                rUnit += cfNote[-1].duration.quarterLength
                noteIndex += 1
                
            counter = z
            while counter < localOffset + rUnit:
                copytemp = note.Note()
                temp = cantorist.flat.notesAndRests.getElementAtOrBefore(counter)
                if temp.offset >= maxOffset - temp.duration.quarterLength:
                    x = maxOffset
                else:  
                    x = cantorist.getElementAfterElement(temp).offset 
                copytemp = copy.deepcopy(temp) #forces copy of value rather than copying pointer to existing - probably a better way.
                
                if temp.offset < counter:
                    copytemp.duration.quarterLength -= (counter - temp.offset)
                    
                if x <= localOffset + rUnit:
                    copytemp.duration.quarterLength = x - counter
                else:
                    copytemp.duration.quarterLength = localOffset + rUnit - counter
                
                cpStream.append(copytemp)
                counter += cpStream[-1].duration.quarterLength
                q = counter - int(counter) #Ugly workaround for irrational rhythmic values
                if 0.9 < q < 1:
                    cpStream[-1].duration.quarterLength += (1-q)
                    counter = int(counter) + 1
                    
            counter = z
            while counter < localOffset + rUnit:
                copytemp = note.Note()
                temp = altist.flat.notesAndRests.getElementAtOrBefore(counter)
                if temp.offset >= maxOffset - temp.duration.quarterLength:
                    x = maxOffset
                else:  
                    x = altist.getElementAfterElement(temp).offset 
                copytemp = copy.deepcopy(temp)
                
                if temp.offset < counter:
                    copytemp.duration.quarterLength -= (counter - temp.offset)
                    
                if x <= localOffset + rUnit:
                    copytemp.duration.quarterLength = x - counter
                else:
                    copytemp.duration.quarterLength = localOffset + rUnit - counter
                
                uSub.append(copytemp)
                counter += uSub[-1].duration.quarterLength
                q = counter - int(counter)
                if 0.9 < q < 1:
                    uSub[-1].duration.quarterLength += (1-q)
                    counter = int(counter) + 1
                    
            counter = z
            while counter < localOffset + rUnit:
                copytemp = note.Note()
                temp = bassist.flat.notesAndRests.getElementAtOrBefore(counter)
                if temp.offset >= maxOffset - temp.duration.quarterLength:
                    x = maxOffset
                else:  
                    x = bassist.getElementAfterElement(temp).offset 
                copytemp = copy.deepcopy(temp)
                
                if temp.offset < counter:
                    copytemp.duration.quarterLength -= (counter - temp.offset)
                    
                if x <= localOffset + rUnit:
                    copytemp.duration.quarterLength = x - counter
                else:
                    copytemp.duration.quarterLength = localOffset + rUnit - counter
                
                lSub.append(copytemp)
                counter += lSub[-1].duration.quarterLength  #leads to rounding errors with tuplets. Kludge incoming
                q = counter - int(counter)
                if 0.9 < q < 1:
                    lSub[-1].duration.quarterLength += (1-q)
                    counter = int(counter) + 1
                
            self.thisPair.append(CPFragment(cfNote, cpStream,uSub, lSub, suspEnding, rUnit, index, localOffset ))
            print(noteIndex)
            localOffset += rUnit
            index += 1       
            
    def resolveChain(self):
        x = -1
        z = 0.0 # testing only
        y = 0.0
        prevCF = note.Note("e~") # arbitrary value that should never arise in real counterpoint
        prevCP = note.Note("e~")
        for fragment in self.thisPair:
            fragment.prevConsonance = x
            fragment.prevCP = prevCP
            if prevCF != "e~":
                fragment.prevCF = prevCF
            result = fragment.resolveFragment()                
            x = result[0]
            prevCF = result[1]
            prevCP = result[2]
            if result[3] == 1:
                y += 1
            if fragment.prevConsonance != -1:
                z += 1
                # print(z) #tracks resolution of fragments for testing
        foo = float(y/z *100)
        print("%i progressions, %i anomalies, %f percentage of fragments have anomalies" %(z+y, y, foo))

            
    def outputScore(self): # Build score from components
        theScore = stream.Score()
        cpPart = stream.Part()
        cfPart = stream.Part()
        cfFrame = stream.Part()
        cpFrame = stream.Part()

        for subject in self.thisPair:
            
            for item in subject.cpstream.flat.notesAndRests:
                cpPart.append(Tinctoris3.fixNote(item))
            for item in subject.notelist.flat.notesAndRests:
                cfPart.append(Tinctoris3.fixNote(item))
            for item in subject.cpOut.flat.notesAndRests:
                cpFrame.append(Tinctoris3.fixNote(item))
            for item in subject.cfOut.flat.notesAndRests:
                cfFrame.append(Tinctoris3.fixNote(item))
                
        theScore.insert(0, cpPart.makeMeasures())
        theScore.insert(0, cpFrame.makeMeasures())
        theScore.insert(0, cfFrame.makeMeasures())
        theScore.insert(0, cfPart.makeMeasures())
        theScore.show()
            
    def frameNotes(self):
        #Rewrite as loop setting variables on each iteration?
        x = 0
        y = len(self.thisPair)
        prevN = note.Note()
        nextN = note.Note()
        while x < y: # need to handle rests in here as well.
            if x > 0 and not self.thisPair[ x -1].cpstream[-1].isRest:
                prevN = self.thisPair[ x -1].cpstream[-1]
            else:
                prevN = self.thisPair[x].cpstream[0]
            
            if x < y -1 and not self.thisPair[x +1].cpstream[0].isRest:
                nextN = self.thisPair[x +1].cpstream[0]
            else:
                nextN = self.thisPair[x].cpstream[-1]
            
            self.thisPair[x].prevFrame = prevN
            self.thisPair[x].nextFrame = nextN
            x += 1
            
    def setPitchOffset(self): # Sets pitchOffset for each fragment to median pitch position between frames per Tinctoris3.voces
        q = 0
        for subject in self.thisPair:
            
            if not subject.nextFrame.isRest:
                x = subject.nextFrame.nameWithOctave
                if len(x) > 2:
                    x = x[0] + x [-1]
            
            if not subject.prevFrame.isRest:
                y = subject.prevFrame.nameWithOctave
                if len(y) > 2:
                    y = y[0] + y[-1]
            
            if subject.prevFrame.isRest or subject.nextFrame.isRest:
                subject.pitchOffset = -1
            else:  
                subject.pitchOffset = (Tinctoris3.voces[x] + Tinctoris3.voces[y])/2
                
            #print(q)
            q += 1   
            
    def setIndices(self):
        for subject in self.thisPair:
            subject.indices = subject.analyseCRhythm(subject.notelist, subject.cpstream)        #
        
inputStream = converter.parse('/Path/To/musicXML/File.xml')  #source xml file


partList = inputStream.getElementsByClass(stream.Part)
cantusVoice = partList[0].flat.notesAndRests        # Set which two voices are treated as main pair
altusVoice = partList[1].flat.notesAndRests         # Analysis assumes cantus + tenor, so re-index as needed
tenorVoice = partList[2].flat.notesAndRests         # Remaining two voices retained for fourths adjudication
bassusVoice = partList[3].flat.notesAndRests        # Creates an object with these voice settings

# Breaks voice pair into a series of contrapuntal fragments based on presumed cf values.
testObject = VoicePair(tenorVoice, cantusVoice, altusVoice, bassusVoice)
testList = testObject.thisPair

# Looks for notes either side of given fragment for help with selecting cf notes in florid textures
# Largely unhelpful at present
testObject.frameNotes()

# Identifies median position between framing notes for use in selecting between pitches with even duration
# Largely unhelpful at present
testObject.setPitchOffset()

# Step through each element of the CPFragment array and attempt to solve.
testObject.resolveChain()

# Output xmlScore to system XMLreader.
# If no default reader linked in Music21, advise changing to write a file.
testObject.outputScore()

print('the end')

