from Queue import PriorityQueue

class TopK(object):

    def __init__(self, _k):
        self.q = PriorityQueue()
        self.k = _k
        self.s = 0
        self.min = 0

    def put(self, _value, _item):
        insert = False
        dummy = ""
        if (self.s == self.k):
            if (_value > self.min):
                dummy = self.q.get()
                self.s = self.k - 1
                insert = True
        else:
            insert = True
        #
        if (insert):
            item = (_value, _item)
            self.q.put(item)
            self.min = self.getMinScore()
            self.s += 1
            #print "Insert: ", item, "\t Evict: ", dummy

    def get(self):
        self.s-=1
        return self.q.get()

    def full(self):
        return True if (self.s == self.k) else False

    def empty(self):
        return True if (self.s == 0) else False

    def dump(self):
        print "q.queue  : ", self.q.queue

    def getk(self):
        l = []
        while not self.q.empty():
            l.append(self.get())
        return reversed(l)

    def getMinScore(self):
        item = self.q.get()
        self.q.put(item)
        return item[0]

    def getActualSize(self):
        return self.s


    def wouldEnter(self, score):
        return self.getActualSize() < self.k or score > self.getMinScore() 

