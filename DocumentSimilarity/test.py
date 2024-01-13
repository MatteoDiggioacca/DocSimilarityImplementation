import DEF.SHINGLING as shin
import DEF.MIN_HASHING as minhash
import DEF.LSH as lsh
import time

tic_0 = time.perf_counter() # inizializzo un timer per contare i tempi di esecuzione di ogni step della pipeline
n_docs = 48 # variabile globale



#------------------ SHINGLING ------------------

dir_path = "./coppie" # path della directory che contiene i documenti da confrontare
result_file_name = "result_file.pdf" # nome del file che conterrà il merge di tutti i documenti (per facilitare lo shingling)
result_file_path = "./"+result_file_name # path del file che conterrà il merge di tutti i documenti (per facilitare lo shingling)
all_shingles = set() # creo il set che conterrà gli shingles
k=3 # dimensione dei singoli shingles

shin.merge_pdfs(dir_path,result_file_name) # faccio il merge dei doc
shin.get_shingles(result_file_path,k,all_shingles) # faccio il loro shingling
n = len(all_shingles) # vedo quanti shingle ho in totale
Matrix = shin.create_shingle_matrix(dir_path,n) # creo la matrice degli shingles...
shin.populate_matrix_2(dir_path,Matrix) # ... e la popolo

toc_1 = time.perf_counter() # prendo il tempo di esecuzione



#------------------ MIN_HASHING ------------------

num_hashes = 250 #numero di funzioni hash da usare per il min-hash

M = minhash.min_hash(Matrix,num_hashes,n_docs) # effettuo il MinHashing

toc_2 = time.perf_counter() # prendo il tempo di esecuzione


#--------------------- LSH ----------------------

threshold = 0.8 # threshold per la Jaccard's Similarity

Matrix_LSH = lsh.LSH(M,threshold) # effettuo LSH
comparable_docs = lsh.docs_to_compare(Matrix_LSH,len(M)) #estraggo i documenti da comparare
toc_3 = time.perf_counter() # prendo il tempo di esecuzione


# TEST PER VEDERE DI QUANTO VENGONO RIDOTTI IL NUMERO DI CONFRONTI

number_compares_after_LSH = 0
for i in range(0,len(comparable_docs)):
    number_compares_after_LSH += len(comparable_docs[i][1])
    
# stampa dei risultati
print(comparable_docs) # stampo i documenti da comparare
print(f"number_compares_before_LSH: {len(M)*len(M)}\nnumber_compares_after_LSH: {number_compares_after_LSH}")
print(f"Tempo di esecuzione Shingling: {toc_1-tic_0:0.4f} secondi\nTempo di esecuzione MinHashing: {toc_2-toc_1:0.4f} secondi\nTempo di esecuzione LSH: {toc_3-toc_2:0.4f} secondi\nTempo di esecuzione totale: {toc_3-tic_0:0.4f} secondi")