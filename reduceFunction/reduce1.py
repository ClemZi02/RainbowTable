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
    """Fonction de réduction pour obtenir un autre mot à partir du hash MD5 avec une méthode plus robuste."""
    # Calcul du hash et conversion en base 10
    hash_valeur = generer_hash_md5(mot)
    
    # Appliquer le modulo pour trouver un indice dans la liste, mais avec une transformation du hash plus complexe
    hash_int = int(hash_valeur, 16)
    indice = (hash_int + hash_int // len(mots)) % len(mots)  # Transformation du hash pour rendre l'indice plus variable
    
    # Sélectionner le mot correspondant à cet indice
    mot_reduit = mots[indice]
    
    return mot_reduit

def generer_chiffres_a_partir_du_hash(mot_reduit):
    """Génère des chiffres à partir des octets du hash MD5 du mot réduit et les insère dans le mot réduit."""
    hash_md5_reduit = hashlib.md5(mot_reduit.encode()).digest()  # Obtenir les octets du hash
    
    # Extraire 4 chiffres (par exemple en utilisant les premiers octets du hash)
    chiffres = ''.join(str(hash_md5_reduit[i] % 10) for i in range(4))  # Utiliser 4 chiffres
    
    # Insérer les chiffres dans le mot réduit de manière intercalée
    mot_genere = ''.join(
        [mot_reduit[i] + chiffres[i] if i < len(chiffres) else mot_reduit[i] for i in range(len(mot_reduit))]  # Ajout des chiffres
    )
    return mot_genere

def appliquer_reduction_multiple(mot, mots, iterations):
    """Applique plusieurs fois la fonction de réduction sur un mot."""
    for _ in range(iterations):
        mot = obtenir_mot_reduit(mot, mots)  # Applique une réduction à chaque itération
    return mot
