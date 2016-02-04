from nltk.corpus import wordnet


def strip_format(word) :
    return word.name()

def make_list(word) :

    ssets = wordnet.synsets(word)

    result = set()

    for s in ssets :

        for lemma in s.lemmas() :
            result.add(strip_format(lemma))
            
            for a in lemma.antonyms() :
                result.add(strip_format(a))

            for h in lemma.hyponyms() :
                result.add(strip_format(h))

            for h in lemma.hypernyms() :
                result.add(strip_format(h))

            #for m in lemma.meronyms() :
            #    result.add(strip_format(m))

            #for h in lemma.holonyms() :
            #    result.add(strip_format(h))

            for l in lemma.similar_tos() :
                result.add(strip_format(l))


    return result

def make_deep_list(word) :
    result = make_list(word)

    for w in result :
        result = result.union(make_list(w))

    return result

