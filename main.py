import exemple # Pour pouvoir utiliser les methodes de exemple.py
import random as rd
import numpy as np
import time
import matplotlib.pyplot as plt


maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
print(maListe)
print(len(maListe)) #Longueur de la liste.
exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier

#Q1
def lire_PrefEtu(name_f):
    file = open(name_f,"r")
    contenu = file.readlines() 
    file.close()
    nb_students = int(contenu[0])
    classement = []
    for i in range(nb_students) :
        line = contenu[i+1].split()
        liste=[]
        for j in range(2,len(line)):
            liste.append(int(line[j]))
        classement.append(liste)

    return classement,nb_students

def lire_PrefSpe(name_f):
    file = open(name_f,"r")
    contenu = file.readlines() 
    file.close()
    capacites = list(map(int, contenu[1].strip().split()[1:]))
    line2=contenu[1].split()
    nb_parcours = len(line2) - 1
    classement = []
    for i in range(nb_parcours) :
        line = contenu[i+2].split()
        liste=[]
        for j in range(2,len(line)):
            liste.append(int(line[j]))
        classement.append(liste)

    return classement,capacites
#Q3
def gale_shapley_hopitaux_etudiants(etudiants, parcours, pref_etudiants, pref_parcours, capacites):
    libres = list(etudiants)  # Pile pour les étudiants libres
    propositions = [0] * len(etudiants)  # Index des prochaines propositions pour chaque étudiant
    affectations = [[] for _ in parcours]  # Affectations courantes pour chaque parcours

    # Matrice de classement des étudiants dans les préférences des parcours
    classement_parcours = [[-1] * len(etudiants) for _ in range(len(parcours))]
    for i in range(len(parcours)):
        for j in range(len(etudiants)):
            etudiant = pref_parcours[i][j]
            classement_parcours[i][etudiant] = j  

    def moins_prefere(idx_parcours):
        """Retourne l'étudiant le moins préféré actuellement affecté au parcours donné."""
        return max(affectations[idx_parcours], key=lambda etu: classement_parcours[idx_parcours][etu])

    def mieux_classe(etu1, etu2, idx_parcours):
        """Vérifie si etu1 est mieux classé que etu2 dans pref_parcours[idx_parcours]."""
        return classement_parcours[idx_parcours][etu1] < classement_parcours[idx_parcours][etu2]

    while libres:
        etudiant = libres.pop()  # Prendre un étudiant libre

        choix_parcours = pref_etudiants[etudiant][propositions[etudiant]]  # Prochain parcours à proposer
        propositions[etudiant] += 1  # Mise à jour de l'index de proposition

        if len(affectations[choix_parcours]) < capacites[choix_parcours]:
            # Ajouter directement si le parcours n'est pas plein
            affectations[choix_parcours].append(etudiant)
        else:
            # Comparer avec le moins préféré
            etudiant_rejete = moins_prefere(choix_parcours)
            if mieux_classe(etudiant, etudiant_rejete, choix_parcours):
                # Remplacer le moins préféré
                affectations[choix_parcours].remove(etudiant_rejete)
                affectations[choix_parcours].append(etudiant)
                libres.append(etudiant_rejete)  # Remettre l'étudiant rejeté en libre
            else:
                # Remettre l'étudiant libre
                libres.append(etudiant)

    return affectations

#Q4
def gale_shapley_hopitaux_parcours(etudiants, parcours, pref_etudiants, pref_parcours, capacites):
    libres = list(parcours)  # Pile pour les parcours libres
    propositions = [0] * len(parcours)  # Index des prochaines propositions pour chaque parcours
    affectations = [None for _ in etudiants]  # Affectations courantes pour chaque étudiant

    # Nombre d'étudiants affectés à chaque parcours
    affectations_parcours = [0] * len(parcours)
    # Matrice qui permet d'avoir la position du parcours pour chaque étudiant
    classement_etudiants = [[-1] * len(parcours) for _ in range(len(etudiants))]

    for i in range(len(etudiants)):
        for j in range(len(parcours)):
            idx_parcours = pref_etudiants[i][j]
            classement_etudiants[i][idx_parcours] = j  

    def mieux_classe(p1, p2, etu):
        """Vérifie si p1 est mieux classé que p2 dans pref_etudiants[etu]."""
        return classement_etudiants[etu][p1] < classement_etudiants[etu][p2]

    while libres:
        idx_parcours = libres.pop()  # Prendre un parcours libre
        if propositions[idx_parcours] >= len(pref_parcours[idx_parcours]):
            # Si le parcours a déjà proposé à tous les étudiants, on passe au suivant
            continue
        
        etudiant = pref_parcours[idx_parcours][propositions[idx_parcours]]  # Prochain étudiant à proposer
        propositions[idx_parcours] += 1  # Mise à jour de l'index de proposition

        if affectations[etudiant] is None:
            # Ajouter directement si l'étudiant n'est pas encore affecté
            affectations[etudiant] = idx_parcours
            affectations_parcours[idx_parcours] += 1  # Incrémenter le nombre d'étudiants affectés à ce parcours
        else:
            # Comparer avec le parcours déjà affecté
            parcours_actuel = affectations[etudiant]
            if mieux_classe(idx_parcours, parcours_actuel, etudiant):
                # Remplacer l'affectation actuelle
                affectations[etudiant] = idx_parcours
                affectations_parcours[idx_parcours] += 1
                affectations_parcours[parcours_actuel] -= 1
                libres.append(parcours_actuel)  # Remettre l'ancien parcours dans les libres

        if affectations_parcours[idx_parcours] < capacites[idx_parcours]:
            libres.append(idx_parcours)

    # Transformer les affectations en une liste d'étudiants pour chaque parcours
    resultat = [[] for _ in parcours]
    for etu, p in enumerate(affectations):
        resultat[p].append(etu)

    return resultat
#Q6
def mieux_classe_e(e1, e2, p,pref_parcours ):
        """Vérifie si e1 est mieux classé que e2 dans pref_parcours[p]."""
        return pref_parcours[p].index(e1) < pref_parcours[p].index(e2)

def mieux_classe_p(p1, p2, e, pref_etudiants):
        """Vérifie si e1 est mieux classé que e2 dans pref_parcours[p]."""
        return pref_etudiants[e].index(p1) < pref_etudiants[e].index(p2)

def paires_instables(affectations,pref_etudiants,pref_parcours,capacites) :
    liste_couples = []
    liste_instables = set()
    for i in range(len(affectations)) :
        for j in range(capacites[i]) :
            liste_couples.append((i,affectations[i][j]))

    for (parcours_1,etudiant_1)  in liste_couples : 
        for (parcours_2,etudiant_2) in liste_couples :
            if(parcours_1 != parcours_2):
               if(mieux_classe_e(etudiant_2,etudiant_1,parcours_1,pref_parcours) and mieux_classe_p(parcours_1,parcours_2,etudiant_2,pref_etudiants)) :
                   liste_instables.add((parcours_1,etudiant_2))
    return liste_instables

#Q7
def pref_alea_etudiants(n) :
    pref_etudiants = [rd.sample(range(9),9) for i in range(n)]
    return pref_etudiants
    
def pref_alea_parcours(n) :  
    pref_parcours = [rd.sample(range(n),n) for i in range(9)] 
    return pref_parcours


def Borda_scores(pref) :
    nb_colonnes = len(pref[0])
    nb_lignes = len(pref)
    classement = [[-1] * nb_colonnes for _ in range(nb_lignes)]

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            idx_parcours = pref[i][j]
            classement[i][idx_parcours] = nb_colonnes - (j + 1)  # Cast en entier si nécessaire 
    return classement
#Q12
def fichier_lp_kpremiers(nom_fichier, pref_etudiants, pref_parcours, capacites, k=3):
    nb_etudiants = len(pref_etudiants)
    nb_parcours = len(pref_parcours)
    scores_etudiants = Borda_scores(pref_etudiants)
    
    with open(nom_fichier, "w") as f:
        f.write("Maximize\n")
        variables = [f"x{i}_{pref_etudiants[i][j]}" for i in range(nb_etudiants) for j in range(k)]
        f.write(" + ".join(variables) + "\n")
        f.write("Subject To\n")

        for j in range(nb_parcours):
            f.write(f"constr_capacite_{j}: ")
            c = " + ".join([f"x{i}_{j}" for i in range(nb_etudiants) if scores_etudiants[i][j] >= (nb_parcours - k)])
            if c:
                f.write(c + f" <= {capacites[j]}\n")

        for i in range(nb_etudiants):
            f.write(f"constr_kpremiers_{i}: ")
            f.write(" + ".join([f"x{i}_{pref_etudiants[i][j]}" for j in range(k)]) + " <= 1\n")

        f.write("Binary\n")
        for i in range(nb_etudiants):
            for j in range(k):
                f.write(f"x{i}_{pref_etudiants[i][j]} ")
        f.write("\nEnd")

#Q13
def fichier_lp_equitable(nom_fichier, pref_etudiants, pref_parcours, capacites):
    nb_etudiants = len(pref_etudiants)
    nb_parcours = len(pref_parcours)
    
    scores_etudiants = Borda_scores(pref_etudiants)
    
    with open(nom_fichier, "w") as f:
        # Déclaration de l'objectif : maximiser z
        f.write("Maximize\n")
        f.write(" z\n")
        
        # Contraintes
        f.write("Subject To\n")
        
        # Contrainte : z <= somme des utilités des étudiants
        for i in range(nb_etudiants):
            f.write(f" constr_utilite_etudiant_{i}: " + " + ".join([f"{scores_etudiants[i][j]} x{i}_{j}" for j in range(nb_parcours)]) + " - z >= 0\n")
        
        
        # Contrainte : chaque étudiant est affecté à un seul parcours
        for i in range(nb_etudiants):
            f.write(f" constr_affectation_{i}: " + " + ".join([f"x{i}_{j}" for j in range(nb_parcours)]) + " = 1\n")
        
        # Contrainte : respect des capacités des parcours
        for j in range(nb_parcours):
            f.write(f" constr_capacite_{j}: " + " + ".join([f"x{i}_{j}" for i in range(nb_etudiants)]) + f" <= {capacites[j]}\n")
        
        # Déclaration des variables binaires
        f.write("Binary\n")
        for i in range(nb_etudiants):
            for j in range(nb_parcours):
                f.write(f"x{i}_{j} ")
        f.write("\n")
        
        
        f.write("Generals\n")
        f.write(" z\n")
        
        
        f.write("End\n")

#Q14
def fichier_lp_efficace(nom_fichier, pref_etudiants, pref_parcours, capacites, k=3):
    nb_etudiants = len(pref_etudiants)
    nb_parcours = len(pref_parcours)
    scores_parcours = Borda_scores(pref_parcours)
    scores_etudiants = Borda_scores(pref_etudiants)
    
    with open(nom_fichier, "w") as f:
        f.write("Maximize\n")
        variables = [f"{scores_etudiants[i][j] + scores_parcours[j][i]} x{i}_{j}" for i in range(nb_etudiants) for j in range(nb_parcours)]
        f.write(" + ".join(variables) + "\n")
        f.write("Subject To\n")

        for i in range(nb_etudiants):
            f.write(f"constr_affectation_{i}: ")
            f.write(" + ".join([f"x{i}_{j}" for j in range(nb_parcours)]) + " <= 1\n")

        for j in range(nb_parcours):
            f.write(f"constr_capacite_{j}: ")
            f.write(" + ".join([f"x{i}_{j}" for i in range(nb_etudiants)]) + f" <= {capacites[j]}\n")

        f.write("Binary\n")
        for i in range(nb_etudiants):
            for j in range(nb_parcours):
                f.write(f"x{i}_{j} ")
        f.write("\nEnd")

#Q15
def fichier_lp_kpremiers_efficace(nom_fichier, pref_etudiants, pref_parcours, capacites, k):
    nb_etudiants = len(pref_etudiants)
    nb_parcours = len(pref_parcours)
    scores_parcours = Borda_scores(pref_parcours)
    scores_etudiants = Borda_scores(pref_etudiants)
    
    with open(nom_fichier, "w") as f:
        f.write("Maximize\n")
        variables = [f"{scores_etudiants[i][j] + scores_parcours[j][i]} x{i}_{j}" for i in range(nb_etudiants) for j in range(nb_parcours)]
        f.write(" + ".join(variables) + "\n")
        f.write("Subject To\n")

        for j in range(nb_parcours):
            f.write(f"constr_capacite_{j}: ")
            c = " + ".join([f"x{i}_{j}" for i in range(nb_etudiants) ])
            if c:
                f.write(c + f" <= {capacites[j]}\n")

        for i in range(nb_etudiants):
            f.write(f"constr_kpremiers_{i}: ")
            f.write(" + ".join([f"x{i}_{pref_etudiants[i][j]}" for j in range(k)]) + " = 1\n")
        
        
        f.write("Binary\n")
        for i in range(nb_etudiants):
            for j in range(nb_parcours):
                f.write(f"x{i}_{j} ")
        f.write("\n")
        
        f.write("End\n")

#Q1
print(lire_PrefEtu("./PrefEtu.txt"))
print(lire_PrefSpe("./PrefSpe.txt"))

# Lecture des fichiers
pref_etudiants,nb_etu = lire_PrefEtu("./PrefEtu.txt")
pref_parcours, capacites = lire_PrefSpe("./PrefSpe.txt")

#Q5 Test de l'algorithme
# Conversion des préférences en noms pour l'algorithme
etudiants = list(range(nb_etu))
parcours = list(range(len(capacites)))

# Capacités des parcours (dictionnaire)
capacites_list = [capacites[i] for i in range(len(parcours))]

affectations_cote_etudiant = gale_shapley_hopitaux_etudiants(
    etudiants,
    parcours,
    pref_etudiants,
    pref_parcours,
    capacites_list
)
affectations_cote_parcours = gale_shapley_hopitaux_parcours(
    etudiants,
    parcours,
    pref_etudiants,
    pref_parcours,
    capacites_list
)

#Q8
valeurs_X = []
valeurs_Y = []
valeurs_Y1 = []
for i in range(200,2001,200):
    valeurs_X.append(i)
    tab=[]
    tab1=[]
    for j in range(10):
        p = pref_alea_parcours(i)
        e = pref_alea_etudiants(i)
        etudiants = list(range(len(e)))
        parcours = list(range(9))

        # Calcul des capacités approximatives
        capacites_list = [i // 9] * 9  # Répartition égale des étudiants

        # Ajuster la capacité pour que la somme soit égale au nombre total d'étudiants
        reste =  i % 9
        for j in range(reste):
            capacites_list[j] += 1
    
        start_time = time.process_time()
        gale_shapley_hopitaux_etudiants(etudiants, parcours,e, p,capacites_list)
        end_start=time.process_time()
        tab.append(end_start-start_time)

        start_time1 =time.process_time()
        gale_shapley_hopitaux_parcours(etudiants, parcours,e, p,capacites_list)
        end_start1 = time.process_time()
        tab1.append(end_start1-start_time1)

    moy = np.mean(np.array(tab))
    valeurs_Y.append(moy)
    print("Pour n = ",i," le temps moyen est de : ",moy )
    moy1 = np.mean(np.array(tab1))
    valeurs_Y1.append(moy1)
    print("Pour n = ",i," le temps moyen est de : ",moy1 )

    

plt.plot(valeurs_X,valeurs_Y,label="côté étudiant", color="red")
plt.plot(valeurs_X,valeurs_Y1,label="côté parcours", color="blue")
plt.xlabel("nb étudiants")
plt.ylabel("temps d'exécution")
plt.legend()
plt.title("courbe des temps d'execution ")
plt.show()

# Appels avec noms de fichiers
fichier_lp_kpremiers("probleme_kpremiers.lp", pref_etudiants, pref_parcours, capacites, 5)
fichier_lp_efficace("probleme_efficace.lp", pref_etudiants, pref_parcours, capacites)
fichier_lp_equitable("probleme_equitable.lp", pref_etudiants, pref_parcours, capacites)
fichier_lp_kpremiers_efficace("kpremier_efficace.lp", pref_etudiants, pref_parcours, capacites, 5)

def recuperer_affectations( nom_f, nb_etudiants=11, nb_parcours=9):
    with open(nom_f ,"r") as f :
        contenu = f.readlines() 
        affectations = [[] for _ in range(nb_parcours)]
        for i in range(1,len(contenu)) :
            line = contenu[i].split()
            if int(line[1]) == 1 :
                var = line[0]
                etudiant , parcours = map(int ,var[1:].split("_"))
                affectations[parcours].append(etudiant)
    return affectations

print("affectations coté étudiant : ",affectations_cote_etudiant)
print("affectations coté parcours : ",affectations_cote_parcours)
affectations_14 = recuperer_affectations("probleme_efficace.sol")
affectations_12 = recuperer_affectations("probleme_kpremiers.sol")
affectations_13 = recuperer_affectations("probleme_equitable.sol")
affectations_15 = recuperer_affectations("kpremier_efficace.sol")
print("affectation12 : ",affectations_12)
print("affectation13 : ",affectations_13)
print("affectation14 : ",affectations_14)
print("affectation15 : ",affectations_15)

def utilite_minimale(affectations, scores):
    utilites = [scores[etu][p] for p in range(len(affectations)) for etu in affectations[p]]
    return min(utilites) if utilites else 0

def utilite_moyenne(affectations, scores):
    utilites = [scores[etu][p] for p in range(len(affectations)) for etu in affectations[p]]
    return sum(utilites) / len(utilites) if utilites else 0
scores_etudiants = Borda_scores(pref_etudiants)
#scores_parcours = Borda_scores(pref_parcours)

print(f"utilité minimale coté etudiant : {utilite_minimale(affectations_cote_etudiant,scores_etudiants)}",f" utilité moyenne coté étudiant : {utilite_moyenne(affectations_cote_etudiant, scores_etudiants)}",f"les paires instables : {paires_instables(affectations_cote_etudiant,pref_etudiants,pref_parcours,capacites)}")
print(f"utilité minimale coté parcours : {utilite_minimale(affectations_cote_parcours,scores_etudiants)}",f" utilité moyenne coté parcours : {utilite_moyenne(affectations_cote_parcours, scores_etudiants)}",f"les paires instables : {paires_instables(affectations_cote_parcours,pref_etudiants,pref_parcours,capacites)}")
print(f"utilité minimale q13 : {utilite_minimale(affectations_13,scores_etudiants)}",f" utilité moyenne Q13 : {utilite_moyenne(affectations_13,scores_etudiants)}",f"les paires insatbles : {paires_instables(affectations_13,pref_etudiants,pref_parcours,capacites)}")
print(f"utilité minimale q14 : {utilite_minimale(affectations_14,scores_etudiants)}",f" utilité moyenne Q14 : {utilite_moyenne(affectations_14,scores_etudiants)}",f"les paires instables : {paires_instables(affectations_14,pref_etudiants,pref_parcours,capacites)}")
print(f"utilité minimale q15 : {utilite_minimale(affectations_15,scores_etudiants)}",f" utilité moyenne Q15 : {utilite_moyenne(affectations_15,scores_etudiants)}",f"les paires instables : {paires_instables(affectations_15,pref_etudiants,pref_parcours,capacites)}")
