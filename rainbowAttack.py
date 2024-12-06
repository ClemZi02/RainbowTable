import hashlib

def charger_mots(fichier):
    """Charge le fichier contenant la liste de mots (un mot par ligne)."""
    with open(fichier, 'r') as f:
        return [ligne.strip() for ligne in f.readlines()]

def generer_hash_md5(mot):
    """Génère un hash MD5 en hexadécimal."""
    return hashlib.md5(mot.encode()).hexdigest()

def obtenir_mot_reduit(mot, mots):
    """Réduit un hash en sélectionnant un mot depuis la liste."""
    # Générer le hash MD5 du mot
    hash_valeur = generer_hash_md5(mot)
    
    # Convertir le hash hexadécimal en un entier
    hash_int = int(hash_valeur, 16)
    
    # Calculer un indice modulo la taille de la liste des mots
    indice = (hash_int + hash_int // len(mots)) % len(mots)
    
    # Retourner le mot correspondant à cet indice
    return mots[indice]

def generer_chiffres_a_partir_du_hash(mot_reduit):
    """Génère des chiffres à partir des octets du hash MD5 du mot réduit et les insère dans le mot réduit."""
    hash_md5_reduit = hashlib.md5(mot_reduit.encode()).digest()  # Obtenir les octets du hash
    
    # Extraire 4 chiffres (par exemple en utilisant les premiers octets du hash)
    chiffres = ''.join(str(hash_md5_reduit[i] % 10) for i in range(4))  # Utiliser 4 chiffres
    
    # Insérer les chiffres dans le mot réduit de manière intercalée
    mot_genere = ''.join(
        [mot_reduit[i] + chiffres[i] if i < len(chiffres) else mot_reduit[i] for i in range(len(mot_reduit))]
    )
    return mot_genere

def attaquer_hashs(mots, hash_challenges, iterations):
    """Essaye de retrouver les mots initiaux correspondant aux hashs cibles."""
    correspondances = {}

    # Pour chaque mot dans la liste
    for mot in mots:
        mot_actuel = mot
        hash_actuel = generer_hash_md5(mot)  # Hash initial

        # Appliquer la réduction et le rehashage plusieurs fois
        for _ in range(iterations):
            # Vérifier si le hash actuel correspond à un hash cible
            if hash_actuel in hash_challenges:
                correspondances[hash_actuel] = mot
                break
            
            # Réduction
            mot_actuel = obtenir_mot_reduit(mot_actuel, mots)
            
            # Génération des chiffres
            mot_genere_avec_chiffres = generer_chiffres_a_partir_du_hash(mot_actuel)
            
            # Recalcul du hash
            hash_actuel = generer_hash_md5(mot_genere_avec_chiffres)
        
        # Si une correspondance a été trouvée, sortir de la boucle principale
        if hash_actuel in correspondances:
            break

    return correspondances

if __name__ == "__main__":
    # Configurations
    fichier_mots = "words_ccm_2023.txt"  # Fichier contenant les mots
    fichier_hashs = "hash_challenges.txt"  # Fichier contenant les hashs à attaquer
    REDUCTION_ITERATIONS = 1000  # Nombre d'itérations de réduction

    # Charger les données
    mots = charger_mots(fichier_mots)
    hash_challenges = charger_mots(fichier_hashs)

    # Lancer l'attaque
    correspondances = attaquer_hashs(mots, hash_challenges, REDUCTION_ITERATIONS)

    # Afficher les résultats
    for hash_cible, mot_trouve in correspondances.items():
        print(f"Hash : {hash_cible} → Mot trouvé : {mot_trouve}")
