import config
from tqdm import tqdm
from reduceFunction import reduce1, reduce1  # Importer reduce1 et reduce1 ici

def generer_rainbow_table(fichier_mots, taille_table, iterations=config.REDUCTION_ITERATIONS, max_attempts=10):
    """Génère une rainbow table avec le mot de base et le dernier hashage, et l'enregistre dans un fichier texte."""
    mots = reduce1.charger_mots(fichier_mots)  # Utiliser la fonction de chargement des mots depuis reduce1.py
    
    # Si la taille de la liste de mots est inférieure à taille_table, répéter ou sélectionner des mots au hasard
    if len(mots) < taille_table:
        mots = mots * (taille_table // len(mots)) + mots[:(taille_table % len(mots))]
    
    rainbow_table = {}  # Dictionnaire pour gérer les collisions
    
    # Ouvrir le fichier texte pour écrire la rainbow table
    with open("txtFile/rainbow_table.txt", "w") as file:
        # Initialiser la barre de progression avec tqdm
        with tqdm(total=taille_table, desc="Génération de la rainbow table", unit="entrée") as pbar:
            for mot_de_base in mots[:taille_table]:
                mot_reduit_final = reduce1.appliquer_reduction_multiple(mot_de_base, mots, iterations)
                hash_mot_genere = reduce1.generer_hash_md5(mot_reduit_final)
                
                # Vérification de collision : si le hash existe déjà dans la rainbow table
                attempts = 0
                while hash_mot_genere in rainbow_table and attempts < max_attempts:
                    # Si une collision est détectée, appliquer une réduction alternative
                    # Essayer différentes méthodes de réduction de manière séquentielle
                    if attempts % 2 == 0:
                        # Appliquer reduce1 si c'est la première tentative
                        mot_reduit_final = reduce1.appliquer_reduction_multiple(mot_de_base, mots, iterations)
                    else:
                        # Appliquer reduce1 si c'est la deuxième tentative
                        mot_reduit_final = reduce1.appliquer_reduction_multiple(mot_de_base, mots, iterations)
                    
                    hash_mot_genere = reduce1.generer_hash_md5(mot_reduit_final)
                    attempts += 1
                

                # Ajouter à la rainbow table sans collision
                rainbow_table[hash_mot_genere] = mot_de_base
                file.write(f"{mot_de_base} {hash_mot_genere}\n")
                
                pbar.update(1)
    
    print(f"Rainbow table générée avec {len(rainbow_table)} entrées sans collision.")

# Exemple d'utilisation avec tes variables
generer_rainbow_table("txtFile/words_ccm_2023.txt", taille_table=config.NUM_ENTREES_RAINBOW_TABLE, iterations=config.REDUCTION_ITERATIONS)
