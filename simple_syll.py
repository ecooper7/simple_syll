## an attempt at a simple syllabification algorithm
## ecooper 6/13/2017
## the basic idea is that each syllable should have a vowel, and after the vowel
## you have to decide whether the consonant that follows should be part of the
## current or the next syllable.  if it's a single consonant, then have it start
## its own syllable.  if it's a double consonant, then have the first consonant
## end the current syllable, and the second consonant start the next one.
## this is not perfect and may not apply in every language, but it is good
## enough for certain applications.  in particular it does not handle semivowels
## like 'y' well, which sometimes act like vowels and sometimes act like
## consonants.  

## define consonants and vowels
## you will have to replace these with your lexicon's phoneset
cs = ['tS', 'ts', 'nf', 'ng', 'dZ', 'J', 'L', 'S', 'dz', 'b', 'd', 'g', 'f', 'k', 'm', 'l', 'n', 'p', 's', 'r', 't', 'w', 'v', 'z']
vs = ['O1', 'u1', 'E1', 'o1', 'i1', 'a1', 'e1', 'a', 'e', 'i', 'j', 'o', 'u']

## replace this with the file containing words you want to syllabify
## in a format like
## word    w eh r d
lexfile = 'oov.prons'

def syl(phones):
    ## reverse the phones so you can treat them like a stack
    phones.reverse()
    output_sylls = [] list of lists
    state = 'START'
    this_syll = []
    memory = ''
    while phones != []:
        ## state machine implementation
        if state == 'START':
            p = phones.pop()
            this_syll.append(p)
            if phones == []:
                ## end of word, close it out
                output_sylls.append(' '.join(this_syll))
                break
            elif p in cs:
                ## stay in START state
                continue
            elif p in vs:
                state = 'SEENVOWEL'
                continue
        elif state == 'SEENVOWEL':
            p = phones.pop()
            if phones == []:  ## check for end of word
                this_syll.append(p)
                output_sylls.append(' '.join(this_syll))
                break
            elif p in vs:
                this_syll.append(p) ## vowel cluster; stay in state SEENVOWEL
            elif p in cs:
                state = 'VC'
        elif state == 'VC':
            if phones == []:  ## check for end of word
                this_syll.append(p)
                output_sylls.append(' '.join(this_syll))
                break
            memory = p
            p = phones.pop()
            if p in cs:  ## double const
                ## if double const on end of word, just add it to last syl
                if phones == []:
                    ## put both p and mem on the last syl and end the word
                    this_syll.append(memory)
                    this_syll.append(p)
                    output_sylls.append(' '.join(this_syll))
                    break
                phones.append(p) # put it back and go back to START
                this_syll.append(memory)
                output_sylls.append(' '.join(this_syll))
                this_syll = []
                state = 'START'
            elif p in vs:
                ## put back TWO phonemes
                phones.append(p)
                phones.append(memory)
                memory = ''
                output_sylls.append(' '.join(this_syll))
                this_syll = []
                state = 'START'

    return output_sylls
                    
import codecs
f = codecs.open(lexfile, mode='r', encoding='utf-8')
for line in f:
    word = line.split('\t')[0]
    pron = line.split('\t')[1].strip().split(' ')
    syllabification = syl(pron)
    ## basic unformatted output
    #print word + '  ' + '[' + line.split('\t')[1].strip() + ']  ' + str(syllabification)
    ## format the output for Festival
    out = '( "' + word + '" nil ('
    for s in syllabification:
        out += '(('
        stress = '0'
        if '1' in s:  ## if your phoneset contains stressed phones.  modify for your phoneset.
            stress = '1'
        for phone in s.split(' '):
            p = phone.strip('1') ## if necessary
            out += p + ' '
        out += ') ' + stress + ' ) '
    out = out.strip()
    out += ') )'
    print out
