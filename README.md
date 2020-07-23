This repository contains the key files for the contrapuntal sieve, the 
analytical tool used in my doctoral dissertation.

All files were created in Python 2.7, which was required by the bindings for 
the suffix array modules downloaded from: 
https://code.google.com/archive/p/pysuffix/ 

Python 2.7 is no longer officially supported by the latest versions of 
Music21, so some adjustments to the code or bindings may be required.
All code runs as of July 2020.

The sieve software consists of four files: Tinctoris3.py, contrapuntalSieve.py,
suffixTables.py and contrapuntalPatterns.py.

Tinctoris3 provides the digital representation of Tinctoris's counterpoint on 
which the sieve depends. In addition it maps note pitches to numerical values 
for interval arithmetic and provides a number of helper functions to identify 
candidate contrapuntal solutions and conduct interval maths.

The contrapuntal sieve itself lives in the contrapuntalSieve.py and does most 
of the work. Given a musicXML file with at least four voices and an 
instruction on which voices to treat as significant, it produces a 
contrapuntal reduction of the nominated voice pair along with a list of 
locations where no contrapuntal solution is available. 

The sieve was last updated in 2018, after which dealing with its output 
became more compelling than making further refinements. Several nascent 
features remain partially realised in the script, such as better techniques 
for deciding between potential contrapuntal solutions of equal duration 
and more sophisticated segmentation of the cantus firmus. The object-
based structure was originally intended to enable an iterative process 
that compared and selected between a range of contrapuntal solutions. 

The suffixTables.py file is an amended version of Tinctoris3.py. The 
relevant parts of this file are the two mapping arrays, one 
that maps progressions to characters for suffix-based pattern 
extraction and the second that maps the characters back to 
progressions. The notation of the progressions is in a form similar 
but not identical to n-gram notation that uses arithmetic rather 
than intervallic description of voice motion.

The contrapuntalPattern.py file takes a series of musicXML files created 
by the sieve and identifies recurring sequences of progressions across 
all files using the encodings in suffixTables.py. Return parameters are 
set in the script itself. There is a character-encoding issue that 
prevents this script running on Windows, but the script runs 
successfully under Ubuntu Linux.
