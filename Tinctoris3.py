# Build a data structure that leads to a list of possible step
# values required to build correct counterpoint according to the
# values provided in Tinctoris De arte contrapuncti Book 1.

# Build an x * y array where x = the present interval between two voices
# and y = possible movement of cantus firms in +/- steps on the staff. Reading the
# table leads to a list of permitted contrapuntal steps in response.

# Each matrix runs -4 to +4 steps in cantus firmus
# Arithmetic value of Cf motion + 4 points to correct array.
# i.e. Opening fifth to following third where cf descends a second:
# x = 4; y = -1. y + 4 = 3 which is index of step descent of cf
# from opening fifth.



# Unison = previous consonant interval, then dictionaries for cf steps -4, -3, -2, -1, 0, 1, 2, 3, 4
# Each list entry = permitted contrapuntal motion in steps on the staff

unison = [
          {0, -2, 3, 1},        # Descending fifth in tenor
          {-1, -3, 4, 1, 2},    # Descending fourth in tenor
          {0,  2, 3},           # Descending third in tenor
          {1, 4, 3, -3},        # Descending second in tenor
          {2, 0, 4, -4, -2},    # Repeated note in tenor
          {3, -1, -3, -4},      # Ascending second in tenor
          {-3, 4, 0, -2},       # Ascending third in tenor
          { -4,  -1, 1, -2},    # Ascending fourth in tenor
          {-1, -3, 2, 0}        # Ascending fifth in tenor
          ]

thirdU= [
          {-4, -2, -1, 1, 3},
          {-3, -1, 2, 4, 0},
          {-2, 0, 1, 3},
          {-1, 1, 2, 4},
          {-2, 0, -4, 2, 3},
          {4, 1, -1, -3},
          { 4, 2, -2},
          {-3, -4, -1, 3},
          {0, -3, -2, 4}
          ]

thirdL= [
          {0, -4, 3, 2},
          {1, -3, 4, 3},
          {2, -2, 4, -4},
          {1, -1, 3, -3, -4},
          {2, 0, 4, -2, -3},
          {1, -1, -2, -4},
          {2, 0, -1, -3},
          {3, 0, -2, -4},
          {4, 1, -1, -3}
          ]

fifthU= [
          {-1, 1, 3},
          {-2, 0, 2, 4},
          {-4, -1, 1, 3},
          {-3, 0, 2, 4},
          {-2, 0, 1, 3},
          {-1, 2},
          {-2, 0, -4, 3},
          {1, -3, 4},
          {2, -2, -4}
          ]

fifthL= [
          {-2, 2, 4},
          {-1, 3},
          {2, 0, 4, -3},
          { 1, -2, -4},
          {2, 0, -1, -3},
          {3, 0, -2, -4},
          {4, 1, -1, -3},
          {2, 0, -2, -4},
          {3, -1, -3}
          ]

sixthU= [
          {0},
          {-3, -1, 1, 3},
          {-2, 0, 2, 4},
          {-4, -1, 1, 3},
          {-3, -1, 0, 2, 4},
          {-2, 1},
          {-1, 2},
          {0, 3},
          {1}
          ]

sixthL= [
          {-1},
          {0, -3},
          {1, -2},
          {2, -1, -3},
          {3, 1, 0, -2, -4},
          {4, 1, -1, -3},
          {2, 0, -2},
          {3, -1, -3},
          {0, -2}
          ]

octaveU= [
          {-2, 0, 1, 3},        # Descending fifth in tenor
          {-1, 1, 2, 4},        # Descending fourth in tenor
          {-4, 0, 2, 3},        # Descending third in tenor
          {-3, 1, 3, 4},        # Descending second in tenor
          {-3, -2, 0, 2, 4},    # Repeated note in tenor
          {-4, -2, -1, 3},      # Ascending second in tenor
          {-3, -1, 0, 4},       # Ascending third in tenor
          {-2, 0, 1},           # Ascending fourth in tenor
          {-1, 1, 2}            # Ascending fifth in tenor
          ]

octaveL= [
          {1, -2},
          {2, 0, -1},
          {3, 1, 0, -4},
          {4, 2, 1, -3},
          {3, 2, 0, -2, -4},
          {4, 3, -1, -3, -4},
          {4, 0, -2, -3},
          {1, -1, -2, -4},
          {2, 0, -1, -3}
          ]

tenthU= [
          {-4, -2, -1, 1, 3},
          {-3, -1, 0, 2, 4},
          {-2, 0, 1, 3},
          {-1, 1, 2, 4},
          {-4, -2, 0, 2, 3},
          {-4, -3, -1, 1},
          {-3, -2, 0, 2},
          {-4, -2, -1, 1, 3},
          {-3, -1, 0, 4}
          ]

tenthL= [
          {3, 1, 0, -4, -3},
          {4, 2, 1, -3},
          {3, 2, 0, -2, -4},
          {4, 3, 1, -1, -3},
          {4, 2, 0, -2, -3},
          {3, 1, -1, -2, -4},
          {2, 0, -1, -3},
          {3, 0, -2, -4},
          {4, 1, -1, -3}
          ]

twelfthU= [
          {-1, 1, 3},
          {-2, 0, 2, 4},
          {-4, -1, 1, 3},
          {0, 2, 4, -3},
          {-4, -2, 0, 1, 3},
          {-1, 2},
          {-4, -2, 0, 3},
          {-4, -3, -1, 1, 4},
          {-3, -2, 0, 2}
          ]

twelfthL= [
          {3, 2, 0, -2},
          {4, 3, -1},
          {4, 0, 2, -3},
          {3, 1, -2, -4},
          {4, 2, 0, -1, -3},
          {3, 0, -2, -4},
          {4, 1, -1, -3},
          {2, 0, -2, -4},
          {3,-1, -3}
          ]

thirteenthU = [
          {0},
          {-3, -1, 1, 3},
          {-2, 0, 2, 4},
          {-4, -1, 1, 3},
          {-3, -1, 0, 2, 4},
          {-2, 1},
          {-1, 2},
          {0, 3},
          {1}
          ]

thirteenthL = [
          {-1},
          {0, -3},
          {1, -2},
          {2, -1, -3},
          {3, 1, 0, -2, -4},
          {4, 1, -1, -3},
          {2, 0, -2},
          {3, -1, -4},
          {0, -3}
          ]

fifteenthU = [
          {-2, 0, 1, 3},
          {-1, 1, 2, 4},
          {-4, 0, 2, 3},
          {-3, 1, 3, 4},
          {-3, -2, 0, 2, 4},
          {-4, -2, -1, 3},
          {-3, -1, 0, 4},
          {-2, 0, 1},
          {-1, 1, 2}
          ]


fifteenthL = [
          {1, -2},
          {2, 0, -1},
          {3, 1, 0, -4},
          {4, 2, 1, -3},
          {3, 2, 0,-2, -4},
          {4, 3, -1, -3, -4},
          {4, 0, -2, -3},
          {1, -1, -2, -4},
          {2, 0, -1, -3}
          ]
    
seventeenthU = [{-4, -2, -1, 1},
                {-3, -1, 0, 2},
                {-2, 0, 1, 3},
                {-1, 1, 2, 4},
                {0, -4, -2, 2, 3},
                {-4, -3, -1, 1},
                {-3, -2, 0, 2},
                {-4, -2, -1, 1, 3},
                {-3, -1, 0, 3}
                ]
    
seventeenthL = [{3, 1, 0, -4},
                {4, 2, 1, -3},
                {3, 2, 0, -2},
                {4, 3, 1, -1},
                {4, 2, 0, -2, -2},
                {3, 1, -1, -2},
                {2, 0, -1},
                {3, 0},
                {4, 1}]    

nineteenthU = [{-1},
               {-2, 0},
               {-4, -1, 1},
               {-3, 0, 2},
               {-4, -2, 0, 1, 3},
               {-1, 2},
               {-4, -2, 0, 3},
               {-4, -3, -1, 1, 4},
               {-3, -2, 0, 2}]

nineteenthL = [{3, 2, -2},
               {4, 3, 0, -1},
               {4, 2, 0},
               {3, 1, -4},
               {4, 2, 0, -1, -3},
               {3, 0, -2},
               {2, 1, 0},
               {2},
               {3}]

twentiethU = [{},
              {-3, -2},
              {-2, 0},
              {-4, -1, 1},
              {-3, -1, 0, 2},
              {-2, 1},
              {-1, 2},
              {0, 3},
              {1}]

twentiethL = [{-1},
              {0, -3},
              {1, -2},
              {2, -1, -3},
              {3, 1, 0, -2},
              {4, 1, -2},
              {2, 0},
              {3},
              {}]

twentysecondU = [{},
                {},
                {-4},
                {-3},
                {-3, 2, 0},
                {-4, -2, -1},
                {-3, -1, 0},
                {-2, 0, 1},
                {-1, 1, 2}]

twentysecondL = [{1,-2},
                 {2, 0, -1},
                 {3, 1, 0},
                 {4, 2, 1},
                 {3, 2, 0},
                 {3},
                 {4},
                 {},
                 {}]
# Setup up array of arrays
progressions = [fifteenthL, thirteenthL, twelfthL, tenthL, octaveL, sixthL, fifthL, thirdL, unison, thirdU,
                fifthU, sixthU, octaveU, tenthU, twelfthU, thirteenthU, fifteenthU, seventeenthU, seventeenthL, 
                nineteenthU, nineteenthL, twentiethU, twentiethL, twentysecondU, twentysecondL]

# Map such that interval maths  using pitch values from voces (below) as
# key points to the correct element of the preceding array
# i.e. A4 - C4 = 5 (i.e. a sixth). 5 keys to 11; Progressions from upper sixth
# are 12th (index 11) element of array progressions.
# Note both arithmetic rather than intervallic calculation of pitch
# and 0-based array addressing.

konsonanzen = {
                -14: 0,
                -12: 1,
                -11: 2,
                -9: 3,
                -7: 4,
                -5: 5,
                -4: 6,
                -2: 7,
                0: 8,
                2: 9,
                4: 10,
                5: 11,
                7: 12,
                9: 13,
                11: 14,
                12: 15,
                14: 16,
                16: 17,
                -16: 18, # extended beyond two octaves half-way through
                18: 19,
                -18: 20,
                19: 21,
                -19: 22,
                21: 23,
                -21: 24}


# Version of previous without the dictionary so it doesn't treat indices as being "in" the list
konsonances= {
                -14,
                -12,
                -11,
                -9,
                -7,
                -5,
                -4,
                -2,
                0,
                2,
                4,
                5,
                7,
                9,
                11,
                12,
                14,
                16,
                -16,
                18,
                -18,
                19,
                -19,
                21,
                -21}

# Map pitches to numeric values for interval mathematics
# Inflections ignored and removed by getInterval function below.
# A third is a third and a sixth is a sixth.
# Range reflects limited compass of repertoire.

voces ={"B1": -1,
        "C2": 0,
        "D2": 1,
        "E2": 2,
        "F2": 3,
        "G2": 4,
        "A2": 5,
        "B2": 6,
        "C3": 7,
        "D3": 8,
        "E3": 9,
        "F3": 10,
        "G3": 11,
        "A3": 12,
        "B3": 13,
        "C4": 14,
        "D4": 15,
        "E4": 16,
        "F4": 17,
        "G4": 18,
        "A4": 19,
        "B4": 20,
        "C5": 21,
        "D5": 22,
        "E5": 23,
        "F5": 24,
        "G5": 25,
        "A5": 26,
        "B5": 27,
        "C6": 28,
        "D6": 29
        }

from music21 import *

# Filter notes for possible contrapuntal continuation. Add available fourths to candidates
# if supported by lower voices.
def filterNotes(noteStream, compNote, cf, testSet, upper, lower): # add ability to read fourths
    forfs = {2, 4} # required intervals between tenor and other voice to allow fourths
    aList = []
    
    for subject in noteStream:     
        if not subject.isRest:
            x = getInterval(subject, compNote)
            if len(subject.nameWithOctave) > 2: 
                subject.nameWithOctave = subject.nameWithOctave[0] + subject.nameWithOctave[-1]
        if subject.isRest:
            continue
        elif subject.nameWithOctave in aList:
            continue
        elif x in testSet:
            aList.append(subject.nameWithOctave)
        elif getInterval(subject, cf)% 7 == 3 and getInterval(subject, cf) > 0:
            temp1 = upper.flat.notesAndRests.getElementAtOrBefore(subject.offset)
            temp2 = lower.flat.notesAndRests.getElementAtOrBefore(subject.offset)
            if not temp1.isRest:
                t1 = getInterval(cf, temp1) % 7
            else:
                t1 = -1
            if not temp2.isRest:
                t2 = getInterval(cf, temp2) % 7
            else:
                t2 = -1
            
            if t1 in forfs or t2 in forfs:
                aList.append(subject.nameWithOctave)  
                
        elif getInterval(subject, cf)% -7 == -3 and getInterval(subject, cf) < 0:       
            temp1 = upper.flat.notesAndRests.getElementAtOrBefore(subject.offset)
            temp2 = lower.flat.notesAndRests.getElementAtOrBefore(subject.offset)
            if not temp1.isRest:
                t1 = getInterval(subject, temp1) % 7
            else:
                t1 = -1
            if not temp2.isRest:
                t2 = getInterval(subject, temp2) % 7
            else:
                t2 = -1
            
            if (t1 in forfs or t2 in forfs) and subject.nameWithOctave not in aList:
                aList.append(subject.nameWithOctave)      
        
                                             
    return(aList)

# Does interval mathematics using values in voces array
def getInterval(cant, ten):
    c = cant.nameWithOctave
    t = ten.nameWithOctave
    if len(c) > 2:
        c = c[0] + c[-1]
    if len (t) > 2:
        t = t[0] + t[-1]  #removes sharp/flat accidentals/signed inflections
    return (voces[c] - voces[t])

# Old kludge to handle inconvenient rests. May be obsolete
def fixNote(aNote):
    if aNote.isRest:
        theNote = note.Rest()
        theNote.duration = aNote.duration
        return(theNote)
    else:
        theNote = note.Note()
        theNote.duration = aNote.duration
        theNote.pitch = aNote.pitch
        return(theNote)
