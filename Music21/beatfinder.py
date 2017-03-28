'''function that reads in results of ngram indexer ("ng") and iterates
through the total number of ng columns ('num') one line at a time, checking
for where any index value matches an index value in the time signature
dictionary (timedict, collected from parsed music21 score object passed as
3rd variable "m21score") and whether that time
signature is duple or triple.It uses the index value and the meter to calculate
the beat position. It assumes all parts have the same time sig changes.
Returns a list of beat values (one per index).'''

def beatfinder(num, ng, m21score):

    import pandas as pd

    indexvals = []
    beats = []
    keys = []
    values = []

    for i in m21score.parts[0].getTimeSignatures():
        keys.append(i.offset)
        values.append(i.numerator)

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
