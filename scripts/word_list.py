from nltk.corpus import wordnet


#TODO decide what to do about bigrams in wordnet

def strip_format(word) :
    return word.name().split('.')[0] #TODO not so sure this is fix, more like a hack. because we have synsets and lemmas here

def make_list(word) :

    ssets = wordnet.synsets(word)

    result = set()

    for s in ssets :

        for d in s.topic_domains() :
            result.add(strip_format(d))

        for h in s.hypernyms() :
            result.add(strip_format(h))

        for lemma in s.lemmas() :
            result.add(strip_format(lemma))
            
            for a in lemma.antonyms() :
                result.add(strip_format(a))

            for h in lemma.hyponyms() :
                result.add(strip_format(h))

            for h in lemma.hypernyms() :
                result.add(strip_format(h))

            for m in lemma.member_meronyms() :
                result.add(strip_format(m))
                
            for m in lemma.substance_meronyms() :
                result.add(strip_format(m))

            for m in lemma.part_meronyms() :
                result.add(strip_format(m))

            for h in lemma.substance_holonyms() :
                result.add(strip_format(h))
                
            for h in lemma.member_holonyms() :
                result.add(strip_format(h))
                
            for h in lemma.part_holonyms() :
                result.add(strip_format(h))

            for l in lemma.similar_tos() :
                result.add(strip_format(l))

            for d in lemma.topic_domains() :
                result.add(strip_format(d))


    return result

def make_deep_list(word) :
    result = make_list(word)

    for w in result :
        result = result.union(make_list(w))

    return result

class lexchain :
    ##NOTE all arguments into these functions need to be a tuple, of the form (id, word, make_deep_list(word))

    def __init__(self, branch1, branch2) :
        self.root = branch1[2].intersection(branch2[2])
        self.branches = [branch1, branch2]
        self.leaves = []

    def __repr__(self) :

        result = str(self.root) + " | "

        for w in self.branches + self.leaves :
            result += w[1] + " "

        return result

    #returns true if id is already in the chain
    def _check_id(self, id) :
        for b in self.branches :
            if (b[0] == id) :
                return True

        for l in self.leaves :
            if (l[0] == id) :
                return True

        return False

    ##attempts to add a word to the chain
    # returns true if succesful (there is a chain) false if otherwise
    def add_word(self, word) :
        if self._check_id(word[0]) :
            return False

        if (self.root.intersection(word[2])) :
            self.branches.append(word)
            return True

        for b in self.branches :
            if (b[2].intersection(word[2])) :
                self.leaves.append(word)
                return True

        return False

    ##checks to see if two branches (that could form a chain) are similar enough to be considered identical
    # returns true if similar, false if otherwise
    def check_similarity(self, branch1, branch2) :
        if (self.root.intersection(branch1[2].intersection(branch2[2]))) :
            return True
        else :
            return False


#this will add a chain to the list of chains given, only if there is not already a matching one in existence
def add_chain(chains, branch1, branch2) :
    #okay first check that these are even viable

    if not (branch1[2].intersection(branch2[2])) :
        return False

    for c in chains :
        if c.check_similarity(branch1, branch2) :
            return False

    chains.append(lexchain(branch1, branch2))

    return True


def syn_score(word) :
    ssets = wordnet.synsets(word)
    count = 0

    for s in ssets :
        count += 1

        for l in s.lemmas() :
            count += 1

            for s in l.similar_tos() :
                count += 1

    return count


def poc_score(words) :
    words = words.split(' ')
    words = [w.lower() for w in words]

    result = [syn_score(w) for w in words]

    display = ''
    for w, r in zip(words, result) :

        display += "{} : {}; ".format(w, r)

    display += 'Total : {}'.format(sum(result))

    print(display)

    return result



def poc (words) :

    words = words.split(' ')
    words = [w.lower() for w in words]

    chains = []

    for i in range(len(words)) :
        words[i] = (i, words[i], make_list(words[i]))

    for i in range(1, len(words)) :
        working = words[i:] + words[0:-len(words) + 1]

        for j in range(len(working)) :
            add_chain(chains, words[j], working[j])

    for c in chains :
        for w in words :
            c.add_word(w)


    return chains
