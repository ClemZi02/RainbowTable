import hashlib

def charger_mots(fichier):
    """Charge le fichier contenant la liste de mots (un mot par ligne)."""
    with open(fichier, 'r') as f:
        mots = [ligne.strip() for ligne in f.readlines()]  # Charger tous les mots dans une liste
    return mots

def generer_hash_md5(mot):
    """Génère un hash MD5 et le convertit en nombre entier (base 10)."""
    hash_md5 = hashlib.md5(mot.encode()).hexdigest()
    return hash_md5  # Retourne le hash en format hexadécimal

def obtenir_mot_reduit(mot, mots):
    """Fonction de réduction avec davantage de diversité pour éviter les collisions."""
    # Calcul du hash MD5 du mot de base
    hash_valeur = generer_hash_md5(mot)
    
    # Convertir le hash MD5 hexadécimal en entier
    hash_int = int(hash_valeur, 16)
    
    # Transformation du hash MD5 pour plus de diversité
    # Utiliser une combinaison de racine carrée, multiplication et modulo
    indice = int(((hash_int ** 0.5 * hash_int // 3) + 9) % len(mots))  # Racine carrée + multiplication pour casser les patterns
    
    # Sélectionner le mot correspondant à cet indice
    mot_reduit = mots[indice]
    
    return mot_reduit

def generer_chiffres_a_partir_du_hash(mot_reduit):
    """Génère des chiffres à partir du hash MD5 du mot réduit tout en conservant les lettres du mot."""
    hash_md5_reduit = hashlib.md5(mot_reduit.encode()).digest()  # Obtenir les octets du hash
    
    # Combiner différentes parties du hash pour obtenir des valeurs utilisables comme chiffres
    partie1 = hash_md5_reduit[0] + hash_md5_reduit[1]
    partie2 = hash_md5_reduit[2] + hash_md5_reduit[3]
    partie3 = hash_md5_reduit[4] + hash_md5_reduit[5]
    partie4 = hash_md5_reduit[6] + hash_md5_reduit[7]
    
    # Calculer les chiffres à partir de chaque partie du hash et appliquer un modulo 10
    chiffres = [
        (partie1 % 10),
        (partie2 % 10),
        (partie3 % 10),
        (partie4 % 10)
    ]
    
    # Convertir la liste de chiffres en chaîne
    chiffres_str = ''.j

def appliquer_reduction_multiple(mot, mots, iterations):
    """Applique plusieurs fois la fonction de réduction sur un mot."""
    for _ in range(iterations):
        mot = obtenir_mot_reduit(mot, mots)  # Applique une réduction à chaque itération
    return mot