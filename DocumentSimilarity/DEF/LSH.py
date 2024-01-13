import copy

# prende in input "s" ed "n" e restituisce "b" ed "r" tali che "b*r = n" && "(1/b)^(1/r) ~ s"
def find_closest_values(s, n):
    closest_diff = float('inf')  
    result = (1, n)  
    for r in range(1, n + 1):
        if n % r == 0:  
            b = n // r  
            diff = abs(s - (1 / b) ** (1 / r)) 
            if diff < closest_diff: 
                closest_diff = diff
                result = (r, b)
    return result


# prendo in input la matrice "M" ed i valori di "b" ed "r", partiziono "M" in una matrice M_partition formata da 
# "b" sottomatrici, ognuna di esse formata da "numero_doc" sottorighe di size "r", in questo modo divido la matrice 
# di min_hashing in "b" bande da "r" righe ciascuna

def partition(M,b,r):
    M_partition = []
    for _ in range(0,b):
        M_bands = []
        for i in range(0,len(M)):
            band = M[i][0:r]
            M[i] = M[i][r:]
            tuple_band = (band,i) #ogni colonna della banda è una coppia (banda_doc_X,indice_doc_X), in questo modo quando dobbiamo comprarare i Doc guardiamo solo l'indice X
            M_bands.append(tuple_band)
        M_partition.append(M_bands)
    return M_partition


# prende in input la matrice di MinHashing ed il threshold per la Jaccard Similarity, restituisce la matrice di LSH

def LSH(M,threshold):
    n = len(M[0])
    #print(f"n: {n}")
    r, b = find_closest_values(threshold, n)
    #print(f"b: {b}, r: {r}\n")
    M_copy = copy.deepcopy(M) 
    M_partition = partition(M_copy,b,r)
    C = 1000 #Prendo C >> r
    Matrix_LSH = [[] for _ in range(C)]
    for band in M_partition:
        for sub_band in band:
            #per generare il valore da hashare concateno ogni signature contenuta in ogni sottobanda, poi lo converto in un valore intero e poi lo hasho
            to_hash = ""
            for elem in sub_band[0]:
                to_hash += str(elem)
            to_hash = int(to_hash)
            index = hash(to_hash)%C
            Matrix_LSH[index].append(sub_band[1]) # e' inutile inserire tutta la sottobanda, mi serve solo come chiave da hashare, inserisco solo l'indice del doc che la contiene
    # Sorto i bucket per indici dei doc in modo tale che ci risulteranno più facili da analizzare in fase di comparazione
    for i in range (0,len(Matrix_LSH)):
        Matrix_LSH[i] = sorted(Matrix_LSH[i], key=lambda x: x)
    return Matrix_LSH


# Prende in input la matrice di LSH e genera una lista di tuple (documento,lista_documenti_comparabili) per aiutarci a leggere la matrice di LSH ed effettuare i confronti

def docs_to_compare(Matrix_LSH,n_docs):
    comparable_docs = []
    for i in range(0,n_docs):
        docs_to_compare_with_doc_i = set()
        for j in range(0,len(Matrix_LSH)):
            if ( i in Matrix_LSH[j] ):
                for elem in Matrix_LSH[j]:
                    docs_to_compare_with_doc_i.add(elem)
        comparable_docs.append((i,docs_to_compare_with_doc_i))
    return comparable_docs
# Quindi, preso "comparable_docs[i]", L'i-esimo documento va comparato con tutti quelli in comparable_docs[i][1], che è una lista di documenti (indici di documenti) 