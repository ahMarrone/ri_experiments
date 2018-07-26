
from topk import TopK
from posting import *
from utils import *

from sys import argv



# DATA

query_terms_ii = get_extended_index()
num_docs = 10000000
wand_data = create_wand_data(query_terms_ii)
print wand_data


docs_proccessed = 0
sorts = 0

def init_postings():
    postings = [SmartPosting(query_terms_ii[i], wand_data[i], 0) for i in xrange(0, len(query_terms_ii))]
    return postings


def print_postings_data(postings):
    print "Postings data ->"
    for p in postings:
        print p


def maxscore(postings):
    # init data
    global docs_proccessed, sorts
    non_essential_lists = 0
    cur_doc = 1
    topk = TopK(2)
    sort_postings_by_upperbound(postings)
    sorts += 1
    maxscores = calc_maxscores(postings)
    ## 
    # bucle principal
    while non_essential_lists < len(query_terms_ii) and cur_doc <= num_docs and cur_doc > -1:
        score = 0
        next_doc = num_docs
        print "Proccessing DOC " + str(cur_doc) 
        # evaluacion de los terminos esenciales
        for i in xrange(non_essential_lists, len(query_terms_ii)):
            if postings[i].get_current_doc_id() == cur_doc:
                score += postings[i].get_current_freq()
                postings[i].next()

            if postings[i].get_current_doc_id() < next_doc:
                next_doc = postings[i].get_current_doc_id()

        # completo evaluacion con score de los terminos no esenciales
        for i in xrange(0, non_essential_lists, 1):
            postings[i].next_geq(cur_doc)
            if (postings[i].get_current_doc_id() == cur_doc):
                score += postings[i].get_current_freq()
                postings[i].next()
        
        print "Trying insert -> " + str(cur_doc) + "\t" + str(score)
        topk.put(score, cur_doc)
        while non_essential_lists < len(postings) and not topk.wouldEnter(maxscores[non_essential_lists]):
            non_essential_lists += 1

        docs_proccessed += 1
        cur_doc = next_doc
    topk.dump()

def maxscore_dyn(postings):
    # init data
    global docs_proccessed, sorts
    non_essential_lists = 0
    cur_doc = 1
    topk = TopK(2)
    sort_postings_by_upperbound(postings)
    sorts += 1
    maxscores = calc_maxscores(postings)
    ## 
    # bucle principal
    while non_essential_lists < len(query_terms_ii) and cur_doc <= num_docs and cur_doc > -1:
        score = 0
        next_doc = num_docs
        print "Proccessing DOC " + str(cur_doc) 
        # evaluacion de los terminos esenciales
        for i in xrange(non_essential_lists, len(query_terms_ii)):
            if postings[i].get_current_doc_id() == cur_doc:
                score += postings[i].get_current_freq()
                postings[i].next()

            # Notar que las siguientes dos lineas estan comentadas
            #if postings[i].get_current_doc_id() < next_doc:
            #    next_doc = postings[i].get_current_doc_id()

        # completo evaluacion con score de los terminos no esenciales
        for i in xrange(0, non_essential_lists, 1):
            postings[i].next_geq(cur_doc)
            if (postings[i].get_current_doc_id() == cur_doc):
                score += postings[i].get_current_freq()
                postings[i].next()
        
        print "Trying insert -> " + str(cur_doc) + "\t" + str(score)
        topk.put(score, cur_doc)

        # Recalculos necesarios por maxscore_dyn
        # Necesito reordenar las postings por su actual ub, y calcular los maxscores nuevamente
        non_essential_lists = 0
        sort_postings_by_upperbound(postings)
        maxscores = calc_maxscores(postings)
        while non_essential_lists < len(postings) and not topk.wouldEnter(maxscores[non_essential_lists]):
            non_essential_lists += 1

        for i in xrange(non_essential_lists, len(query_terms_ii)):
            if postings[i].get_current_doc_id() < next_doc:
                next_doc = postings[i].get_current_doc_id()
        sorts += 1
        docs_proccessed += 1
        cur_doc = next_doc
    topk.dump()



def maxscore_smart_dyn(postings):
    # init data
    global docs_proccessed, sorts
    non_essential_lists = 0
    cur_doc = 1
    topk = TopK(2)
    sort_postings_by_upperbound(postings)
    sorts += 1
    maxscores = calc_maxscores(postings)
    ## 
    # bucle principal
    while non_essential_lists < len(query_terms_ii) and cur_doc <= num_docs and cur_doc > -1:
        score = 0
        next_doc = num_docs
        need_sort = False
        print "Proccessing DOC " + str(cur_doc) 
        # evaluacion de los terminos esenciales
        #import pdb; pdb.set_trace()
        for i in xrange(non_essential_lists, len(query_terms_ii)):
            if postings[i].get_current_doc_id() == cur_doc:
                score += postings[i].get_current_freq()
                postings[i].next()
                need_sort = need_sort or postings[i].get_ub_changed()
                postings[i].set_ub_changed(False)

            # Notar que las siguientes dos lineas estan comentadas
            #if postings[i].get_current_doc_id() < next_doc:
            #    next_doc = postings[i].get_current_doc_id()

        # completo evaluacion con score de los terminos no esenciales
        for i in xrange(0, non_essential_lists, 1):
            postings[i].next_geq(cur_doc)
            if (postings[i].get_current_doc_id() == cur_doc):
                score += postings[i].get_current_freq()
                postings[i].next()
        
        print "Trying insert -> " + str(cur_doc) + "\t" + str(score)
        topk.put(score, cur_doc)

        # Recalculos necesarios por maxscore_dyn
        # Necesito reordenar las postings por su actual ub, y calcular los maxscores nuevamente
        if need_sort:
            non_essential_lists = 0
            sort_postings_by_upperbound(postings)
            maxscores = calc_maxscores(postings)
            while non_essential_lists < len(postings) and not topk.wouldEnter(maxscores[non_essential_lists]):
                non_essential_lists += 1
            sorts += 1

        for i in xrange(non_essential_lists, len(query_terms_ii)):
            if postings[i].get_current_doc_id() < next_doc:
                next_doc = postings[i].get_current_doc_id()
        docs_proccessed += 1
        cur_doc = next_doc
    topk.dump()





postings_lists = init_postings()
sort_postings_by_upperbound(postings_lists)
print_postings_data(postings_lists)

strategy = argv[1]
if strategy == "maxscore":
    maxscore(postings_lists)
elif strategy == "maxscore_dyn":
    maxscore_dyn(postings_lists)
elif strategy == "maxscore_smart_dyn":
    maxscore_smart_dyn(postings_lists)

print "DOCS PROCCESSED -> " +  str(docs_proccessed)
print "SORTS -> " +  str(sorts)

