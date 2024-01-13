import random


# prende in input la matrice binaria degli Shingles, il numero di funzioni hash da utilizzare ed il numero totale di documenti

def min_hash(Matrix,num_hashes,n_doc):
    sim_matr = []
    N = len(Matrix[0])
    for i in range(num_hashes):
        sim_matr.append(['inf']*n_doc)
        a = random.randint(1,N)
        b = random.randint(1,N)
        for row in range(N):
            hash_row = (row*a + b)%N    # (ax + b) mod N
            for doc in range(n_doc):
                if Matrix[doc][row] == 1 and (sim_matr[i][doc] == 'inf' or hash_row < sim_matr[i][doc]):
                    sim_matr[i][doc] = hash_row
    M_da_trasporre = sim_matr
    M = [[M_da_trasporre[j][i] for j in range(len(M_da_trasporre))] for i in range(len(M_da_trasporre[0]))]
    return M