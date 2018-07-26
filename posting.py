class Posting(object):


    def __init__(self, docs_enum, max_weights, ub_cursor):
        self.docs_enum = docs_enum
        self.max_weights = max_weights
        self.df = len(self.docs_enum) / 2
        self.cursor = 0
        self.ub_cursor = ub_cursor


    def get_current_doc_id(self):
        if self.cursor == -1:
            return -1
        return self.docs_enum[self.cursor*2]


    def get_current_freq(self):
        if self.cursor == -1:
            return -1
        return self.docs_enum[(self.cursor*2)+1]


    def next(self):
        if self.cursor == (self.df  - 1):
            self.cursor = -1
        else:
            self.cursor += 1


    def next_geq(self, doc_id):
        while self.get_current_doc_id() < doc_id and self.cursor > -1:
            self.next()


    def get_current_max_weight(self):
        while self.ub_cursor < len(self.max_weights) - 2 and self.max_weights[self.ub_cursor+2] <= self.cursor:
            self.ub_cursor += 2
            if self.ub_cursor == len(self.max_weights) - 2:
                break
        return self.max_weights[self.ub_cursor+1]


    def __str__(self):
        return str(self.get_current_doc_id()) + "\t" +  str(self.get_current_freq()) + "\t" + str(self.get_current_max_weight())


class SmartPosting(Posting):


    def __init__(self, docs_enum, max_weights, ub_cursor):
        super(SmartPosting, self).__init__(docs_enum, max_weights, ub_cursor)
        self.ub_has_changed = False

    def set_ub_changed(self, changed):
        self.ub_has_changed = changed

    def get_ub_changed(self):
        return self.ub_has_changed


    def next(self):
        if self.cursor == (self.df  - 1):
            self.cursor = -1
        else:
            #import pdb; pdb.set_trace()
            previous_ub = self.get_current_max_weight()
            self.cursor += 1
            if previous_ub != self.get_current_max_weight():
                self.ub_has_changed = True

    def get_current_max_weight(self):
        while self.ub_cursor < len(self.max_weights) - 2 and self.max_weights[self.ub_cursor+2] <= self.cursor:
            self.ub_cursor += 2
            if self.ub_cursor == len(self.max_weights) - 2:
                break
        return self.max_weights[self.ub_cursor+1]
