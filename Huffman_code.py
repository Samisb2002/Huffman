import os 
class CharNode:
    def __init__(self, char, freq):
        # Initialise un nœud avec un caractère et sa fréquence
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def calcul_de_frequence(text):
    # Cette fonction calcule la fréquence de chaque caractère dans le texte
    alphabet = {}
    for char in text:
        # Parcourt chaque caractère du texte et compte sa fréquence
        if char in alphabet:
            alphabet[char] += 1
        else:
            alphabet[char] = 1
    return alphabet

def get_noeudss(alphabet):
    # Cette fonction crée des nœuds pour chaque caractère avec sa fréquence
    char_nodes = []
    for char, freq in alphabet.items():
        char_node = CharNode(char, freq)
        char_nodes.append(char_node)
    # Trie les nœuds par fréquence croissante et par ordre lexicographique si égalité
    return sorted(char_nodes, key=lambda cn: (cn.freq, ord(cn.char)))

def arbre(char_nodes):
    # Cette fonction construit l'arbre de Huffman
    while len(char_nodes) > 1:
        # Fusionne les deux nœuds de fréquence la plus basse
        t1 = char_nodes.pop(0)
        t2 = char_nodes.pop(0)
        new_node = CharNode(None, t1.freq + t2.freq)
        new_node.left = t1
        new_node.right = t2
        # Insère le nouveau nœud dans la liste et la trie à nouveau
        char_nodes.append(new_node)
        char_nodes = sorted(char_nodes, key=lambda cn: (
            cn.freq, ord(cn.char) if cn.char is not None else float('inf')))
    return char_nodes[0]  # Renvoie la racine de l'arbre Huffman

def table_codage(root):
    # Cette fonction crée une table de codage avec les codes binaires pour chaque caractère
    encoding_table = {}

    def table_codage_rec(node, code):
        # Parcourt récursivement l'arbre et génère les codes binaires pour chaque caractère
        if node.char:  
            # Si le nœud représente un caractère (feuille de l'arbre)
            # Alors, on associe ce caractère à son code binaire dans la table de codage
            encoding_table[node.char] = code
        else:
            table_codage_rec(node.left, code + '0')
            table_codage_rec(node.right, code + '1')
    table_codage_rec(root, '')  # Appel initial avec la racine de l'arbre
    return encoding_table

def texte_code(text, encoding_table):
    # Cette fonction remplace chaque caractère du texte par son code binaire correspondant
    encoded_text = ''
    for char in text:
        encoded_text += encoding_table[char]
    return encoded_text

def pack_bits(encoded_text):
    # Cette fonction regroupe les bits par paquets de 8 pour former des octets
    packed_bits = []#Initialise une liste vide qui stockera les octets regroupés.
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        byte += '0' * (8 - len(byte))
        packed_bits.append(int(byte, 2))
    return packed_bits  

def compress(text):
    # Cette fonction exécute toutes les étapes de compression de Huffman
    alphabet = calcul_de_frequence(text)  # Calcule les fréquences des caractères
    char_nodes = get_noeudss(alphabet)   # Crée des nœuds pour chaque caractère
    root = arbre(char_nodes)  # Construit l'arbre de Huffman
    encoding_table = table_codage(root)  # Crée la table de codage
    encoded_text = texte_code(text, encoding_table)  # Encode le texte
    packed_bits = pack_bits(encoded_text)  # Met les bits en paquets
    return packed_bits

# Lecture du fichier et compression
monfichier = open("C:/Users/samis/Desktop/9raya/S6/Huffman/alice.txt", "r")
lines = monfichier.read().splitlines()
text = ""
for j in range(len(lines)):
    text += lines[j]
ga = calcul_de_frequence(text)
dic=""
for caractere, valeur in ga.items():
    dic += f"{caractere}: {valeur}\n"
compressed_text = compress(text)  # Compression du texte
liste=""
for element in compressed_text:
    liste+=f"-{element}"
with open("frequence","a",encoding='utf-8') as f:
    f.write(f"{len(ga)}\n")
    f.write(f"{"frequence de chaque lettre  :"+" "+dic}\n")
    f.write(f"{"texte compressé :"+" "+liste}\n")
for bit in compressed_text:
    print(bin(bit)[2:].zfill(8), end=' ')  # Affiche la représentation binaire de chaque entier compressé
fichier = bytes(text, 'utf-8')
with open('text-compressé.bin', 'wb') as file_comp:
    file_comp.write(fichier)  # Enregistre le texte compressé dans un fichier binaire

chemin_entree = "C:/Users/samis/Desktop/9raya/S6/Huffman/alice.txt"
chemin_sortie="C:/Users/samis/Desktop/9raya/S6/Huffman/text-compressé.bin"

original_size = os.path.getsize(chemin_entree)
compressed_size = os.path.getsize(chemin_sortie)
compression_rate = (original_size - compressed_size)*100/original_size
# average_bits_per_character = len(texte_encode) / len(texte)
with open("frequence","a",encoding='utf-8') as f:
    f.write(f"{"taux de compression : " + str(compression_rate)+ " % " }")

