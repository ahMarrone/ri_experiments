import math


def calc_maxscores(postings):
    maxscores = [postings[0].get_current_max_weight()]
    for x in xrange(1, len(postings)):
        maxscores.append(postings[x].get_current_max_weight()+maxscores[x-1])
    return maxscores


def sort_postings_by_upperbound(postings):
    postings.sort(key=lambda x: x.get_current_max_weight())


def sort_postings_by_docid(postings):
    postings.sort(key=lambda x: x.get_current_doc_id(), reverse=True)


def create_wand_data(postings):
    wand_data = []
    for i in xrange(0, len(postings)):
        df_posting = len(postings[i]) / 2
        step = int(math.floor(math.sqrt(df_posting)))
        print "STEP " + str(step)
        current_wand_data = []
        for j in xrange(0, len(postings[i]), step*2):
            #print j
            upperbound = 0
            for k in xrange(j, len(postings[i]), 2):
                if postings[i][k+1] > upperbound:
                    upperbound = postings[i][k+1]
            current_wand_data.append(j/2)
            current_wand_data.append(upperbound)
        wand_data.append(current_wand_data)
    return wand_data


# retorna lista de listas
# [0] -> indice invertido
# [1] -> ub_lists
def get_simple_index():
    return [
            [1, 10, 2, 9, 3, 8, 4, 1, 5, 1, 6, 1, 8, 1], # docid, freq, docid, freq ...
            [1, 1, 3, 7, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1],
            [7, 1, 8, 1]
        ]
        

#[
#            [0, 10, 2, 8, 4, 1, 6, 1],  # pos, ub, pos, ub, ...
#            [0, 7, 2, 1, 4, 1, 6, 1],
#            [0, 1, 1, 1]
#        ]

def get_extended_index():
    index = get_simple_index()
    for i in xrange(9, 1000):
        index[0].append(i)
        index[0].append(1)
    index[0].append(1000)
    index[0].append(100)
    for i in xrange(1001, 5000):
        index[0].append(i)
        index[0].append(1)
    return index