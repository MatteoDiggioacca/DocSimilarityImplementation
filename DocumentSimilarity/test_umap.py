import DEF.SHINGLING as shin
import DEF.MIN_HASHING as minhash
import DEF.LSH as lsh
import DEF.umap as our_umap
import time

tic_0 = time.perf_counter() # inizializzo un timer per contare i tempi di esecuzione di ogni step della pipeline


#------------------ SHINGLING ------------------

dir_path = "./coppie" # path della directory che contiene i documenti da confrontare
result_file_name = "result_file.pdf" # nome del file che conterrà il merge di tutti i documenti (per facilitare lo shingling)
result_file_path = "./"+result_file_name # path del file che conterrà il merge di tutti i documenti (per facilitare lo shingling)
all_shingles = set() # creo il set che conterrà gli shingles
k=3 # dimensione dei singoli shingles

#shin.merge_pdfs(dir_path,result_file_name) # faccio il merge dei doc
shin.get_shingles(dir_path,k,all_shingles) # faccio il loro shingling
n = len(all_shingles) # vedo quanti shingle ho in totale
Matrix = shin.create_shingle_matrix(dir_path,n) # creo la matrice degli shingles...
shin.populate_matrix_2(dir_path,Matrix) # ... e la popolo

toc_1 = time.perf_counter() # prendo il tempo di esecuzione

#--------------------- UMAP ----------------------

u = our_umap.our_umap(Matrix)
comparable_docs = our_umap.couples(u)

toc_2 = time.perf_counter() # prendo il tempo di esecuzione

    
# stampa dei risultati
print(comparable_docs) # stampo i documenti da comparare
print(f"Tempo di esecuzione Shingling: {toc_1-tic_0:0.4f} secondi\nTempo di esecuzione UMAP: {toc_2-toc_1:0.4f} secondi\nTempo di esecuzione totale: {toc_2-tic_0:0.4f} secondi")