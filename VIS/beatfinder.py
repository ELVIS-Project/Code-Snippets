import pandas as pd
import music21
import vis
from vis.models.indexed_piece import Importer
    
def beatfinder(num, ng, m21score):
    
    """For finding beat values in midi files where there are no barlines (and
    thus music21's beat method returns nothing.)
    function reads in results of ngram indexer ('ng') and iterates
    through the total number of ng columns ('num') one line at a time, checking
    for where any index value matches an index value in the time signature
    dictionary (timedict, collected from parsed music21 score object passed as
    3rd variable 'm21score') and whether that time
    signature is duple or triple.It uses the index value and the meter to calculate
    the beat position. It assumes all parts have the same time sig changes.
    Returns a pandas series containing beat values (one per index)."""

    indexvals = []
    beats = []

    keys = [i.offset for i in m21score.parts[0].getTimeSignatures()]
    values = [i.numerator for i in m21score.parts[0].getTimeSignatures()]

    timedict = dict(zip(keys, values))
    triple = [3, 6, 9, 12]
    duple = [2, 4]
    cur_time = 'duple'

    for n in range(num):
        i = ng['ngram.NGramIndexer', ng['ngram.NGramIndexer'].columns[n]]
        for x in range(len(i)):
            indexvals.append(i.index[x])
            # check for match between current index and index at time change
            if i.index[x] in [k for k, v in timedict.items() if v in triple]:
                cur_time = 'triple'
                adj = i.index[x] % 6  # 6 quarter notes per "measure in 3/2"
            if i.index[x] in [k for k, v in timedict.items() if v in duple]:
                cur_time = 'duple'
                adj2 = i.index[x] % 8  # 8 quarter notes per "measure" in 4/2
            if cur_time == 'triple':
                beats.append(
                    ((i.index[x] - adj) % 6) / 2) # 1 beat = a minim or half n
            else:
                beats.append(((i.index[x] - adj2) % 8) / 2)

    return(pd.Series(data=beats, index=indexvals))
