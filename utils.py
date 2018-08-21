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


def get_large_index_test():
    return [
        [447,1,457,3,489,1,517,2,603,1,622,3,718,2,801,1,811,1,840,1,859,1,879,1,902,1,950,2,1012,1,1014,1,1022,15,1026,6,1060,1,1089,1,1098,1,1105,13,1156,2,1391,1,1812,1,1817,8,1821,1,1840,6,1844,7,1852,1,1870,6,1878,10,1893,1,1911,6,1918,10,1950,8,1959,9,1972,31,1976,27,1979,3,1985,3,1986,3,1987,3,1989,31,1991,41,1998,1,1999,1,2001,1,2003,2,2006,40,2075,1,2223,1,2245,1,2337,2,2503,1,2508,1,2676,1,2694,3,2696,1,2715,1,2717,1,2718,5,3138,2,3158,1,3164,1,3172,9,3173,4,3174,5,3175,4,3176,4,3177,4,3178,4,3179,4,3180,4,3181,4,3182,4,3183,4,3184,4,3185,4,3186,4,3187,4,3188,4,3189,4,3190,48,3220,1,3231,2,3236,2,3373,1,4478,1,4489,4,4503,1,4505,8,4512,2,4514,1,4527,1,4789,1,4921,1,4974,1,5213,1,5247,3,5248,2,5452,1,5542,1,5556,1,5559,1,5692,2,5904,1,5919,1,6041,5,6273,1,6297,1,6535,1,6571,1,7239,1,8157,1,8219,1,8221,2,8623,1,8654,1,8756,1,8791,1,8804,2,8906,3,8909,1,9250,3,9290,1,9295,1,9298,1,9463,3,9822,1,9863,1,9864,1,9865,1,9935,1],
        [444,1,455,1,472,1,473,1,476,1,617,1,618,1,619,1,685,2,784,1,857,1,903,1,928,4,938,2,939,1,1076,1,1078,1,1092,2,1196,1,2003,1,2065,1,2075,5,2225,3,2241,1,2248,2,2540,3,2682,1,3164,3,3165,3,3203,1,3900,1,3901,1,3915,1,4120,1,4169,4,4563,1,4927,1,4946,3,4955,1,4956,2,5038,1,5040,1,5093,1,5213,1,5350,2,5390,4,5463,1,5470,1,5539,1,5556,1,5559,1,5567,1,5581,2,5894,1,6029,1,6151,2,6179,1,6233,2,6267,1,6273,45,6275,1,6276,2,6277,3,6643,1,6672,1,7159,1,7163,5,7943,1,7969,2,7997,1,8003,4,8015,1,8211,1,8219,14,8220,4,8444,2,8792,1,8794,6,8823,1,8824,4,8836,1,8878,1,8906,16,8909,9,9250,148,9256,1,9292,1,9308,1,9321,3,9463,16,9472,9,9475,12,9476,3,9826,50,9827,6,9829,4,9830,9,9831,5,9868,1,9885,2,9886,1,9930,1,9932,1,9933,1,9936,3,9966,2,9989,1]
    ]