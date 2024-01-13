import os
from pypdf import PdfMerger
import PyPDF2
import string
from primePy import primes as pms 
from bitarray import bitarray  

#come ti dicevo, ho considerato che il path base e' "./coppie/test", poi gli aggiungo + "1.pdf","2.pdf","2.pdf", etc...

# Prende in input il path della directory contenente i documenti in PDF ed il nome 
# del file PDF che servirà da merge di tutti i testi di tutti i documenti, in modo da facilitare
# la loro analisi tramite shingling
def merge_pdfs(dir_path,result_file_name):
    pdfs = os.listdir(dir_path)
    pdfs.sort()
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(dir_path + "/" + pdf)
    merger.write(result_file_name)
    merger.close()
    

#pdf to string, prende in input il path di un PDF e restituisce il testo in stringhe
def extract_text(file_path):
    with open(file_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = ""
        for page in reader.pages:
            content = page.extract_text()
            pdf_text += content
    return pdf_text

# rimuove tutti i caratteri speciali dal testo, ritornando il testo "ripulito"
def remove_special_characters(text):
    special_chars = [
            "!","#", ",", ".", ";", ":", "¬", "−",
            "§", "|", "?", "@", "[", "]", "∧", "”", '\\',
            "£", "$", "%", "&","/", "(", "’", "∨", "–"
            ")", "=", "''", "^", "*", "<", ")", "“", "\u02b1",
            ">", "{", "}", "∩", "∞", "→", "´", "–", "\u02c1",
            "′", "-", "+", "•", "≤", "∪", "<", "′" ]
    text = text.replace("-\n", "")
    text = text.replace("\n", " ")
    text = text.lower()
    for char in special_chars:
        text = text.replace(char, "")
    return text

# prende in input il path del file dal quale estrarre gli shingles, un valore "k" per determinare
# la lunghezza degli shingles ed un set nel quale inserire gli shingles
def get_shingles(file_path, k, all_shingles):
    global counter
    text = extract_text(file_path)
    parsed_text = remove_special_characters(text)
    words = parsed_text.split()
    for i in range(len(words) - k + 1):
        shingle = ""
        for j in range (0,k):
            if j == 0:
                shingle += words[i+j]
            else:
                shingle += " "+words[i+j]
        if all(c in string.ascii_lowercase + string.digits + " " for c in shingle):
            all_shingles.add(shingle)



# prende in input il path della directory contenente i documenti ".pdf" ed il num di shingles distinti
# dello step precedente, restituisce la matrice di minhashing vuota

def create_shingle_matrix(pdfs_path,num_shingles):
    pdfs = os.listdir(pdfs_path)
    N = pms.between(num_shingles, 2*num_shingles)[0] #dimensione bit array, primo compreso tra num_shingles e 2*num_shingles
    Matrix = []
    for _ in pdfs:
        Matrix.append(bitarray('0'*N))
    return Matrix



# prende in input il path di un singolo documento, il "k" per la size degli shingles, la matrice di min hashing e l'indice del bitarray 
# da modificare all'interno della matrice di minhashing

def get_doc_shingles_2(file_path, k, Matrix,index):
    text = extract_text(file_path)
    parsed_text = remove_special_characters(text)
    words = parsed_text.split()
    for i in range(len(words) - k + 1):
        shingle = ""
        for j in range (0,k):
            if j == 0:
                shingle += words[i+j]
            else:
                shingle += " "+words[i+j]
        if all(c in string.ascii_lowercase + string.digits + " " for c in shingle):
            pos = hash(shingle)%len(Matrix[index])
            Matrix[index][pos] = 1
            
            

# prende in input il path della directory contenente i pdf e popola la matrice di min hashing
            
def populate_matrix_2(pdfs_base_path,Matrix):
    pdfs = os.listdir(pdfs_base_path)
    pdfs.sort()
    i = 1
    for pdf in pdfs:
        file_to_shingle = pdfs_base_path + "/" + pdf
        get_doc_shingles_2(file_to_shingle,3,Matrix,i-1)
        i = i+1
