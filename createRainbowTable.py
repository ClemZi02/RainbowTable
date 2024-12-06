import config
from tqdm import tqdm
from reduceFunction import reduce1, reduce2  # Importer reduce1 et reduce2 ici

def generer_rainbow_table(fichier_mots, taille_table, iterations=config.REDUCTION_ITERATIONS):
    """Génère une rainbow table avec le mot de base et le dernier hashage, et l'enregistre dans un fichier texte."""
    mots = reduce2.charger_mots(fichier_mots)  # Utiliser la fonction de chargement des mots depuis reduce2.py
    
    # Si la taille de la liste de mots est inférieure à taille_table, répéter ou sélectionner des mots au hasard
    if len(mots) < taille_table:
        mots = mots * (taille_table // len(mots)) + mots[:(taille_table % len(mots))]

    # Ouvrir le fichier texte pour écrire la rainbow table
    with open("txtFile/rainbow_table.txt", "w") as file:
        # Initialiser la barre de progression avec tqdm
        with tqdm(total=taille_table, desc="Génération de la rainbow table", unit="entrée") as pbar:
            for mot_de_base in mots[:taille_table]:
                # Appliquer la réduction sur le mot de base
                mot_reduit_final = reduce2.appliquer_reduction_multiple(mot_de_base, mots, iterations)  # Appliquer la réduction à partir de reduce2.py
                
                # Calculer les hashages du mot réduit final
                hash_mot_genere = reduce2.generer_hash_md5(mot_reduit_final)  # Calculer le hash

                # Vérifier le premier caractère du hash
                if hash_mot_genere[0].isdigit():  # Si le premier caractère est un chiffre
                    # Appliquer reduce2
                    dernier_mot = reduce2.obtenir_mot_reduit(mot_reduit_final, mots)
                    dernier_mot_avec_chiffres = reduce2.generer_chiffres_a_partir_du_hash(dernier_mot)
                    dernier_hash = reduce2.generer_hash_md5(dernier_mot_avec_chiffres)
                else:  # Si le premier caractère est une lettre
                    # Appliquer reduce1
                    dernier_mot = reduce1.obtenir_mot_reduit(mot_reduit_final, mots)
                    dernier_mot_avec_chiffres = reduce1.generer_chiffres_a_partir_du_hash(dernier_mot)
                    dernier_hash = reduce1.generer_hash_md5(dernier_mot_avec_chiffres)

                # Écrire le premier mot et le dernier hashage dans le fichier texte
                file.write(f"{mot_de_base} {dernier_hash}\n")  # Chaque entrée sur une nouvelle ligne avec mot de base et dernier hash
                
                # Mise à jour de la barre de progression
                pbar.update(1)
    
    print(f"Rainbow table générée et enregistrée dans rainbow_table.txt avec {taille_table} entrées.")

# Exemple d'utilisation avec tes variables
generer_rainbow_table("txtFile/words_ccm_2023.txt", taille_table=config.NUM_ENTREES_RAINBOW_TABLE, iterations=config.REDUCTION_ITERATIONS)
