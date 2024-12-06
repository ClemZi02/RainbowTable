import hashlib
import random

def charger_mots(fichier):
    """Charge le fichier contenant la liste de mots (un mot par ligne)."""
    with open(fichier, 'r') as f:
        mots = [ligne.strip() for ligne in f.readlines()]  # Charger tous les mots dans une liste
    return mots

def generer_hash_md5(mot):
    """Génère un hash MD5 et le convertit en nombre entier (base 10)."""
    hash_md5 = hashlib.md5(mot.encode()).hexdigest()
    return hash_md5  # Retourne le hash en format hexadécimal

def obtenir_mot_reduit(mot, mots, iteration):
    """Fonction de réduction améliorée pour éviter les collisions avec plus de transformations et permutations."""
    # Calcul du hash MD5 du mot de base
    hash_valeur = generer_hash_md5(mot)
    
    # Convertir le hash MD5 hexadécimal en entier
    hash_int = int(hash_valeur, 16)

    # Plusieurs transformations sur le hash pour augmenter la diversité
    if iteration % 5 == 0:
        # Transformation 1 : Utilisation d'un modulo de base
        indice = (hash_int % len(mots))  
    elif iteration % 5 == 1:
        # Transformation 2 : Modification plus complexe du hash (carré + division)
        indice = ((hash_int ** 2 + hash_int // 2) % len(mots))  # Carré et division
    elif iteration % 5 == 2:
        # Transformation 3 : Inversion des octets du hash
        byte_order = bytearray(hash_valeur.encode())  # Convertir en bytes
        byte_order.reverse()  # Inverser l'ordre des octets
        hash_int = int(byte_order.hex(), 16)  # Convertir en entier après inversion
        indice = (hash_int % len(mots))  # Nouveau indice basé sur la permutation
    elif iteration % 5 == 3:
        # Transformation 4 : Mélange des caractères aléatoires
        random.seed(hash_int)  # Utilisation du hash pour générer des éléments aléatoires
        indice = random.randint(0, len(mots)-1)
    else:
        # Transformation 5 : combinaison de bits et opérations arithmétiques sur le hash
        indice = ((hash_int + (hash_int >> 2)) ^ (hash_int >> 5)) % len(mots)

    # Sélectionner le mot correspondant à cet indice
    mot_reduit = mots[indice]
    
    return mot_reduit

def generer_chiffres_a_partir_du_hash(mot_reduit):
    """Génère des chiffres à partir du hash MD5 du mot réduit et les insère dans le mot réduit."""
    hash_md5_reduit = hashlib.md5(mot_reduit.encode()).digest()  # Obtenir les octets du hash
    
    # Extraire 4 chiffres (par exemple en utilisant les premiers octets du hash)
    chiffres = ''.join(str(hash_md5_reduit[i] % 10) for i in range(4))  # Utiliser 4 chiffres
    
    # Insérer les chiffres dans le mot réduit de manière intercalée
    mot_genere = ''.join(
        [mot_reduit[i] + chiffres[i] if i < len(chiffres) else mot_reduit[i] for i in range(len(mot_reduit))]  # Ajout des chiffres
    )
    return mot_genere

def appliquer_reduction_multiple(mot, mots, iterations):
    """Applique plusieurs fois la fonction de réduction sur un mot avec différentes transformations MD5."""
    for i in range(iterations):
        # Applique une réduction différente à chaque itération pour réduire les collisions
        mot = obtenir_mot_reduit(mot, mots, i)
    
    return mot
