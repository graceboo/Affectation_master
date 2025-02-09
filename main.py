import exemple # Pour pouvoir utiliser les methodes de exemple.py
import random as rd
import numpy as np
import time
import matplotlib.pyplot as plt


maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
print(maListe)
print(len(maListe)) #Longueur de la liste.
exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier


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

def pref_alea_etudiants(n) :
    pref_etudiants = [rd.sample(range(9),9) for i in range(n)]
    return pref_etudiants
    
def pref_alea_parcours(n) :  
    pref_parcours = [rd.sample(range(n),n) for i in range(9)] 
    return pref_parcours
   
print(lire_PrefEtu("./PrefEtu.txt"))
print(lire_PrefSpe("./PrefSpe.txt"))

# Lecture des fichiers
pref_etudiants,nb_etu = lire_PrefEtu("./PrefEtu.txt")
pref_parcours, capacites = lire_PrefSpe("./PrefSpe.txt")

# Conversion des préférences en noms pour l'algorithme
etudiants = list(range(nb_etu))
parcours = list(range(len(capacites)))



# Capacités des parcours (dictionnaire)
capacites_list = [capacites[i] for i in range(len(parcours))]


# Test de l'algorithme
resultat = gale_shapley_hopitaux_etudiants(
    etudiants,
    parcours,
    pref_etudiants,
    pref_parcours,
    capacites_list
)
resultat2 = gale_shapley_hopitaux_parcours(
    etudiants,
    parcours,
    pref_etudiants,
    pref_parcours,
    capacites_list
)
# Affichage du résultat
print(resultat2)
print(resultat)

affectations_bis=[[3, 5], [4], [2], [8], [10], [1], [0], [7], [9, 6]]
print("les paires instables retournées avec coté étudiant : ",paires_instables(resultat,pref_etudiants,pref_parcours,capacites))
print("les paires instables retournées avec coté parcours : ",paires_instables(resultat2,pref_etudiants,pref_parcours,capacites))


valeurs_X = []
valeurs_Y = []
for i in range(200,2001,200):
    valeurs_X.append(i)
    tab=[]
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
    moy = np.mean(np.array(tab))
    valeurs_Y.append(moy)
    print("Pour n = ",i," le temps moyen est de : ",moy )
    
fig , ax = plt.subplots()
ax.plot(valeurs_X,valeurs_Y)
ax.set_xlabel("nombre d'étudiants")
ax.set_ylabel("temps d'execution ")
plt.title("courbe des temps d'execution ")
plt.show()



valeurs_X = []
valeurs_Y = []
for i in range(200,2001,200):
    valeurs_X.append(i)
    tab=[]
    for j in range(10):
        p=pref_alea_parcours(i)
        e=pref_alea_etudiants(i)
        etudiants=list(range(len(e)))
        parcours=list(range(9))
         # Calcul des capacités approximatives
        capacites_list = [i // 9] * 9  # Répartition égale des étudiants

        # Ajuster la capacité pour que la somme soit égale au nombre total d'étudiants
        reste =  i % 9
        for j in range(reste):
            capacites_list[j] += 1
        
        start_time=time.process_time()
        gale_shapley_hopitaux_parcours(etudiants, parcours,e, p,capacites_list)
        end_start = time.process_time()
        tab.append(end_start-start_time)
    moy = np.mean(np.array(tab))
    valeurs_Y.append(moy)
    print("Pour n = ",i," le temps moyen est de : ",moy )
    
fig , ax = plt.subplots()
ax.plot(valeurs_X,valeurs_Y)
ax.set_xlabel("nombre d'étudiants")
ax.set_ylabel("temps d'execution ")
plt.title("courbe des temps d'execution ")
plt.show()

