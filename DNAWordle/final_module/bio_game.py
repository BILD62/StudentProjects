def get_dna_strand():
    
    '''Gives user a random DNA strand from the list below'''
    
    import numpy as np
    
    dna_strands = ['GGAGAACGATTACTTTCA',
                   'TGAGCACGATAATTAAGA',
                   'ACCCGATGACTTGCATCA',
                   'CTATCTCGATAATTAAGA',
                   'CTACGATTAACACTTAGA',
                   'AGATGAGCACGATTACTA',
                   'AAACGATACTAAGAAATA',
                   'AAAGAACGATTTCTTTCA',
                   'TAATACGGACGAGAACTT',
                   'TCATAATACGGAGAACTT']
    
    dna_strand = np.random.choice(dna_strands)
    
    print('Your DNA strand is: ' + dna_strand)


def dna_to_rna(dna_strand): 
    
    '''Loops though the DNA strand chosen above and returns the complementary RNA strand'''
    
    rna_strand = ''
    
    for base in dna_strand: 
        
        if base == 'A': 
            
            rna_strand = rna_strand + 'U'
            
        elif base == 'T': 
            
            rna_strand = rna_strand + 'A'
            
        elif base == 'G': 
            
            rna_strand = rna_strand + 'C'
            
        elif base == 'C': 
            
            rna_strand = rna_strand + 'G'
            
        else:
            
            raise NameError('Remember, your DNA strand can only have A, T, C, and G. Please check your strand.')
            
              
    return rna_strand
        
def rna_to_aa(rna_strand):
    
    '''Loops through the RNA strand, identifies the codons, and returns the single letter abbreviations for
    each codon within the RNA'''
    
    import random
    
    codon_abbreviations = {'UUU':'F','UUC':'F','UUA':'L','UUG':'L','CUU':'L',
                           'CUC':'L','CUA':'L','CUA':'L','CUG':'L','AUU':'I',
                           'AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V',
                           'GUA':'V','GUG':'V','UCU':'S','UCC':'S','UCA':'S',
                           'UCG':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
                           'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A',
                           'GCC':'A','GCA':'A','GCG':'A','UAU':'Y','UAC':'Y',
                           'CAU':'H','CAC':'H','CAA':'Q','CAG':'Q','AAU':'N',
                           'AAC':'N','AAA':'K','AAG':'K','GAU':'D','GAC':'D',
                           'GAA':'E','GAG':'E','UGU':'C','UGC':'C','UGG':'W',
                           'CGU':'R','CGC':'R','CGA':'R','CGG':'R','AGU':'S',
                           'AGC':'S','AGA':'R','AGG':'R','GGU':'G','GGC':'G',
                           'GGA':'G','GGG':'G'}
    
    num_codons= int(len(rna_strand)/3)
    print(num_codons)
    
    aa = []
    
    for i in range(num_codons):
        
        start_id=i*3
        stop_id=(i+1)*3
    
        this_codon= rna_strand[start_id: stop_id]
        
        if this_codon in codon_abbreviations:
            
            aa.append(codon_abbreviations[this_codon])
            
        else:
            
            raise NameError('Codon does not have a matching amino acid, please check your strand again') 
            
    
    random.shuffle(aa) #randomly shuffles the amino acid codes
    
    print(aa)
    
    
    
def guess_the_word():
    
    '''Allows the user to unscramble the 6 letters given above and guess until the word matches one of the
    words in the list'''
    
    response = input('Unscramble your RNA codon appreviations in order to guess your word: ')
    
    response_list = ['planes', 
                     'trains', 
                     'waters', 
                     'drains', 
                     'dances', 
                     'strand', 
                     'family', 
                     'flakes', 
                     'impale', 
                     'simple']

    while response.lower() not in response_list:
            
        response = input('Please try again: ')
        
    print('YOU GOT IT!!!! Thanks for playing!')