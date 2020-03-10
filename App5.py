
###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)
import math
import argparse
import glob
import sys
import os
import networkx as nx
from pathlib import Path
from random import randint
from random import choice


import time
### Ajouter ici les signes de ponctuation Ã  retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_", "\'", "\"", "\\", "»", "«", "\n"]

###  Vous devriez inclure vos classes et méthodes ici, qui seront appellées Ã  partir du main
def Generation(graph1):
    i = 1
    NText = ''
    di2 = dict()
    NText = list(graph1)[randint(0, len(list(graph1))-args.m)]
    i = args.m - 1
    while i < args.G:
        if args.m == 1:
            NText = NText + ' ' + k[randint(0, len(k)-1)]
        else:
            NText = NTextGramme(NText, k)
        i += 1
    print(NText)
    mots = NText.split()
    di2 = gramme(mots, di2)
    di2 = valeurPourCent(di, len(mots))
    return di2
def NTextGramme(NText,k):
    A = NText.split()
    B = A[len(A)-args.m]
    i = args.m-1
    while i > 0:
        B = B + ' ' + A[len(A)-i]
        i -= 1
    print(B)
    time.sleep(2.4)
    D = ''
    while D != B:
        E = randint(0, len(k) - args.m)
        C = k[E].split()
        D = C[0]
        i = 1
        while i < args.m:
            print(i)
            print(C)
            D = D + ' ' + C[i]
            i += 1
        print(D)
    i=1
    print(C)
    while i<len(C):
        NText = NText + ' ' + C[i]
        i+=1
    return NText
def comparaison(text, librairie):
    ressemblence=0
    for k, v in text.items():
        if k in librairie:
            ressemblence += ((v ** 2) + (librairie[k] ** 2)) ** 0.5
    if ressemblence > 1:
        ressemblence = 1
    return ressemblence
def grammeG(mots,GMots):
    i = 0
    for w in mots:
        if len(w) >= 3:
            w = str.lower(w)
            g = 1
            if w not in GMots:
                GMots.add_node(w)
            while i + g < len(mots) and len(mots[i + g]) < 3:
                g = g + 1
            if g + i < len(mots):
                mots[i + g] = str.lower(mots[i + g])
                if mots[i+g] not in GMots:
                    GMots.add_node(mots[i+g])
                GMots.add_edge(w, mots[i+g])
            g = g + 1
        i = i + 1
    return GMots
def gramme(mots,di):
    i = 0
    mots2 = mots
    for w in mots:
        if len(w) >= 3:
            k = 1
            g = k
            mots2[i] = w
            while k < args.m:

                while i+g < len(mots) and len(mots[i+g]) < 3:
                    g = g+1
                if g+i < len(mots):
                    mots2[i] = mots2[i] + ' ' + mots[g+i]
                else:
                    k=args.m
                k = k+1
                g = g + 1
            mots2[i] = str.lower(mots2[i])
            di[mots2[i]] = di.get(mots2[i], 0.0) + 1
        i = i + 1
    return di
def valeurPourCent(di,nbMots):
    di2=dict()
    for k, v in di.items():
        di2[k] = di2.get(k, v/nbMots)
    return di2
def Ponctuation(ligne):
    args.p = True
    no_punct = ' '
    for char in ligne:
        if char not in PONC:
            no_punct = no_punct + char
    return no_punct
def lecture(di, G):
    longeur = 0
    for file in glob.glob('*.txt'):
        print(file + '\n')
        f = open(file, 'r', encoding='utf-8')
        line2 = ''
        for line in f:
            line2 = line2 + ' ' + Ponctuation(line)
        mots = line2.split()

        di = gramme(mots, di)
        G = grammeG(list(di),G)
        print(G.nodes())
        print(G.edges())

        longeur = longeur + len(mots)
        f.close()
    di= valeurPourCent(di, longeur)
    return di, G


### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 4),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du rÃ©pertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des rÃ©pertoires d'auteurs, peu importe le systÃ¨me d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - DÃ©finis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code
    j = 1
    librairieDI = []
    librairieG = []
    G = nx.Graph()
    ##Lecture et enregistrement
    for a in authors:
        aut = a.split("/")
        di = dict()
        if aut[-1] != '.DS_Store':
            os.chdir(cwd+'\\'+args.d + '\\' + 'Isack')
            di = dict()
            (di, G) = lecture(di, G)
            ##for k, v in di.items():
                ##print(k,v)

        librairieDI.append(di)
        librairieG.append(G)
        j += 1
    i = 1
    ## génération
    ##librairieDI.append(Generation(choice(librairieG)))
    ##Comparaison
    for a in authors:
        if a != '.DS_Store':
            R = comparaison(librairieDI[len(authors)-1], librairieDI[i]) ## remplacer ***librairi[1]*** par le dict() du nouveau text
            print(a+" : %0.2f" % R)
            i += 1