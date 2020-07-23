#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script takes as its input a set of corrected outlines generated by the contrapuntal sieve
# and retrieves a list of patterns matching the length and frequency parameters at line 178.

# Requires the suffixTables file to provide character mapping of progressions.

# There is a character set problem that prevents this script working on Windows.
# This should be easily fixable, but I have simply stuck to Linux for pattern extraction.


from music21 import *
import suffixtables
from rstr_max import *
import sys
from os import walk

def parseCPString():

    stringdex = 0
    stringArray = []

    indices = []
    rstr = Rstr_max()
    f = []
    forfs = {3, -3, 10, -10}                    # Arithmetic values of fourths for separate treatment
    for (dirpath, dirnames, filenames) in walk('/Path/To/xmlFiles/'):
        f.extend(filenames)
        break

    for item in f:
        stringArray.insert(stringdex, item)
        stringdex += 1
        dircty = '/Path/To/xmlFiles/'
        dircty += item
        contrapair = converter.parse(dircty)

        upV = 0                                 # If using purely two voice reduction (as early in project)
        downV = 1


        partList = contrapair.getElementsByClass(stream.Part)

        if len(partList) == 4:                  # i.e. is sieve extracted outline w/ reduction in inner voices
            upV = 1
            downV = 2


        counter = partList[upV].flat.notesAndRests
        firmus = partList[downV].flat.notesAndRests

        lindex = 0
        steps = 0
        consonance = -1
        prevCounter = note.Note()
        prevFirmus = note.Note()
        offset = 0
        string = ""
        locator = 0
        index = []


        print(item)     # for tracking/testing/debugging; can be commented out

        while lindex < len(firmus):

            lower = firmus[lindex]
            upper = counter.getElementAtOrBefore(lower.offset)
            locator += lower.duration.quarterLength


            if upper.isRest or lower.isRest:
                # stringList[steps] = string
                # string = ""
                steps += 1
                consonance = -1
                lindex += 1
                continue

            if suffixtables.getInterval(prevCounter, upper) == 0 and suffixtables.getInterval(prevFirmus, lower) == 0 and consonance != -1:
                lindex += 1
                continue

            elif consonance == -1:
                consonance = suffixtables.getInterval(upper,lower)
                if consonance not in forfs:
                    char = suffixtables.konsonances[consonance]
                    string += char
                    indices.append(locator/4)
                    prevCounter = upper
                    prevFirmus = lower
                else:
                    z = suffixtables.getInterval(upper,lower)
                    if consonance == 3:
                       char =  suffixtables.fourthUOut[z]
                    elif consonance == -3:
                        char = suffixtables.fourthLOut[z]
                    elif consonance == 10:
                        char = suffixtables.eleventhUOut[z]
                    elif consonance == -10:
                        char = suffixtables.eleventhLOut[z]

            elif consonance in forfs:
                z = suffixtables.getInterval(upper,lower)
                if consonance == 3:
                   char =  suffixtables.fourthUOut[z]
                elif consonance == -3:
                    char = suffixtables.fourthLOut[z]
                elif consonance == 10:
                    char = suffixtables.eleventhUOut[z]
                elif consonance == -10:
                    char = suffixtables.eleventhLOut[z]

                consonance = z
            else:

                x = suffixtables.getInterval(upper, prevCounter)

                if x > 4:
                    x = x % 7
                    if x > 4:                   # Treats motion of greater than a fifth as implied
                        x -= 7                  # octave transpostion of reverse complementary motion
                if x < -4:                      # i.e. ascending 6th = descending third + octave
                    x = x % -7
                    if x < -4:
                        x += 7

                y = suffixtables.getInterval(lower, prevFirmus)
                if y > 4:
                    y = y % 7
                    if y > 4:
                        y -= 7
                if y < -4:
                    y = y % -7
                    if y < -4:
                        y += 7

                z = suffixtables.getInterval(upper, lower)
                if z in forfs:
                    if z == 3:
                        char = suffixtables.fourthUIn[consonance]
                    elif z == -3:
                        char = suffixtables.fourthLIn[consonance]
                    elif z == 10:
                        char = suffixtables.eleventhUIn[consonance]
                    elif z == -10:
                        char = suffixtables.eleventhLIn[consonance]
                else:
                    interval = suffixtables.progressions[suffixtables.konsonanzen[consonance]]
                    theSet = interval[y + 4]
                    if x not in theSet:
                        char = suffixtables.illegals[z]
                    else:
                        char = theSet[x] #.encode('utf-8') used when trying to solve character encoding issues

                string += char
                indices.append(locator/4)   # record location of progression
                # print(locator/4)  # More testing/debugging
                consonance = z

                prevCounter = upper
                prevFirmus = lower

            offset += lower.duration.quarterLength
            lindex += 1


        #str1_unicode = unicode(string,'utf-8','replace')
        rstr.add_str(string)
        print(string)               # Print the resulting contrapuntal string and
        print(len(string))          # its length for each completed file

    r = rstr.go()                                       # Hereon largely cut-and-paste from example code for bindings
                                                        # Jammed in location markers for pattern strings
    numPatts = 0                                        # And reverse-encoding of patterns.
    for (offset_end, nb), (l, start_plage) in r.iteritems():
        if l < 3 or nb < 5:                             # Parameters: l = min. length, nb = min. number of occurrences
            continue
        print('----------------------------------------------------------')
        print(nb)
        print('----------------------------------------------------------')
        ss = rstr.global_suffix[offset_end-l:offset_end]
        id_chaine = rstr.idxString[offset_end-1]
        s = rstr.array_str[id_chaine]
        print '[%s] %d'%(ss.encode('utf-8'), nb)
        for o in range(start_plage, start_plage + nb) :
            offset_global = rstr.res[o]
            offset = rstr.idxPos[offset_global]
            id_str = rstr.idxString[offset_global]
            print '   (%i,%i, %s)'%(indices[offset],l, stringArray[id_str]) # Print location of following string

            sss = rstr.global_suffix[offset_global:offset_global+l]
            strung = ""
            for char in sss:                             # Map each character back to a progression
                it = char.encode('utf-8')
                strung += suffixtables.reverseCP[it]     # Windows breaks on character encoding here.
                strung += ';'
            print(strung)                         # Print reverse-mapped contrapuntal pattern.

        numPatts += 1

    print('Number of patterns matching parameters:\t%s' %(numPatts))
    print("The end!")


parseCPString()