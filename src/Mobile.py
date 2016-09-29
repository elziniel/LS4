from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import math
import random
import sys

class Fenetre():

    # Initialisation de la fenetre (taille, menu, canvas)
    def __init__(self, width = 800, height = 600):
        self.fenetre = Tk()
        self.fenetre.resizable(width = False, height = False)

        self.width = int(width)
        self.height = int(height)
        self.arbre = Arbre()
        self.arbre.generer2arbre(10, 10)

        self.canvas = Canvas(self.fenetre, width = self.width, height = self.height, background = "white")
        self.canvas.pack()

        self.affiche_menu()

        self.initialise(self.arbre)
        self.fenetre.mainloop()

    # Affichage de la barre de menu
    def affiche_menu(self):
        self.barre_menu = Menu(self.fenetre)

        self.menu_fichier = Menu(self.barre_menu, tearoff=0)
        self.menu_fichier.add_command(label = "Nouveau", command = lambda modification = False: self.nouveau(modification))
        self.menu_fichier.add_command(label = "Ouvrir...", command = self.ouvrir)
        self.menu_fichier.add_command(label = "Generer", command = self.generer)
        self.menu_fichier.add_command(label = "Modifier", command = lambda modification = True: self.nouveau(modification))
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label = "Enregistrer...", command = self.enregistrer)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label = "Quitter", command = self.fenetre.destroy)

        self.barre_menu.add_cascade(label = "Fichier", menu = self.menu_fichier)

        self.menu_affichage = Menu(self.barre_menu, tearoff=0)
        self.menu_affichage.add_command(label = "Normal", command = self.normal)
        self.menu_affichage.add_command(label = "Croissant", command = lambda croissant = True: self.ordre(croissant))
        self.menu_affichage.add_command(label = "Decroissant", command = lambda croissant = False: self.ordre(croissant))

        self.barre_menu.add_cascade(label = "Affichage", menu = self.menu_affichage)

        self.fenetre.config(menu = self.barre_menu)

    # Initialisation de l'affichage de l'arbre
    def initialise(self, arbre):
        self.fenetre.title(arbre.arbre2liste())

        self.arbre = arbre
        self.intervalle = (self.width)/(self.arbre.nbr()+1)
        self.max = self.arbre.max()
        self.min = self.arbre.min()

        self.canvas.delete(ALL)

        self.arbre.equilibre(self, 1, [0])

    # Definition d'un nouveau mobile par texte
    def nouveau(self, modification):

        fenetre = Tk()
        fenetre.resizable(width = False, height = False)

        if modification:
            fenetre.title("Modifier un mobile")
            nouveau_mobile = Entry(fenetre)
            nouveau_mobile.insert(END, str(self.arbre.arbre2liste()))
            nouveau_mobile.pack(side = LEFT, padx = 5, pady = 5)
        else:
            fenetre.title("Nouveau mobile")
            nouveau_mobile = Entry(fenetre)
            nouveau_mobile.pack(side = LEFT, padx = 5, pady = 5)

        btn_valider = Button(fenetre, text = 'Valider', command = lambda mobile = nouveau_mobile: self.nouveau_2(mobile, fenetre))
        btn_valider.pack(side = LEFT, padx = 5, pady = 5)

        btn_annuler = Button(fenetre, text = 'Annuler', command = fenetre.destroy)
        btn_annuler.pack(side = LEFT, padx = 5, pady = 5)

    # Initialisation du nouveau mobile
    def nouveau_2(self, mobile, fenetre):
        arbre = Arbre()
        try:
            arbre.liste2arbre(eval(mobile.get()))
        except:
            showwarning("Erreur d'affichage", "Le mobile propose est invalide")
            fenetre.destroy()
            return

        self.canvas.delete(ALL)
        fenetre.destroy()

        self.initialise(arbre)

    # Definition et initialisation d'un nouveau mobile par ouverture de fichier
    def ouvrir(self):
        fichier = askopenfilename(title = "Ouvrir un mobile", filetypes = [('txt files','.txt'),('all files','.*')])
        if fichier:
            self.arbre.fichier2liste(fichier)

            self.canvas.delete(ALL)

            self.initialise(self.arbre)

    # Definition d'un nouveau mobile par generation aleatoire en fonction des parametres
    def generer(self):
        fenetre = Tk()
        fenetre.resizable(width = False, height = False)
        fenetre.title("Generer un mobile")

        lbl_nombre_poids = Label(fenetre, text = "Nombre de poids : ")
        lbl_nombre_poids.pack()
        lbl_nombre_poids.grid(row = 0, column = 0)

        nombre_poids = Entry(fenetre)
        nombre_poids.pack()
        nombre_poids.grid(row = 0, column = 1, columnspan = 2)

        lbl_taille_poids = Label(fenetre, text = "Taille maximal d'un poids : ")
        lbl_taille_poids.pack()
        lbl_taille_poids.grid(row = 1, column = 0)

        taille_poids = Entry(fenetre)
        taille_poids.pack()
        taille_poids.grid(row = 1, column = 1, columnspan = 2)

        btn_valider = Button(fenetre, text = 'Valider', command = lambda nombre = nombre_poids, taille = taille_poids: self.generer_2(nombre, taille, fenetre))
        btn_valider.pack()
        btn_valider.grid(row = 3, column = 1)

        btn_annuler = Button(fenetre, text = 'Annuler', command = fenetre.destroy)
        btn_annuler.pack()
        btn_annuler.grid(row = 3, column = 2)

    # Initialisation du nouveau mobile
    def generer_2(self, nombre, taille, fenetre):
        arbre = Arbre()
        try:
            n = int(nombre.get())//2
            t = int(taille.get())//2
        except:
            showwarning("Erreur d'affichage", "Les parametres proposes sont invalides")
            fenetre.destroy()
            return

        arbre.generer2arbre(nombre.get(), taille.get())

        self.canvas.delete(ALL)
        fenetre.destroy()

        self.initialise(arbre)

    # Definition et application de l'enregistrement du mobile actuel dans un fichier
    def enregistrer(self):
        fichier = asksaveasfilename(title = "Enregistrer un mobile", filetypes = [('txt files','.txt'),('all files','.*')])
        if fichier:
            fichier = open(fichier, 'w')
            fichier.write(str(self.arbre.arbre2liste()))
            fichier.close()

    # Classement du mobile dans l'ordre croissant ou decroissant
    def ordre(self, ordre):
        arbre = Arbre()
        arbre.copie(self.arbre)

        liste = arbre.liste_simple()
        liste.sort()
        if not ordre:
            liste.reverse()

        arbre.classer(liste, [0, 0])

        self.fenetre.title(arbre.arbre2liste())
        self.canvas.delete(ALL)

        arbre.equilibre(self, 1, [0])

    # Classement du mobile dans son ordre normal
    def normal(self):
        self.canvas.delete(ALL)
        self.fenetre.title(self.arbre.arbre2liste())

        self.arbre.equilibre(self, 1, [0])

class Arbre():

    # Initialisation de l'arbre
    def __init__(self, valeur = 0):
        self.tige = 0
        self.valeur = valeur
        self.gauche = None
        self.droite = None

    # Passage d'une liste representant un arbre a un arbre
    def liste2arbre(self, liste):
        if "[" in str(liste):
            self.gauche = Arbre()
            self.gauche.liste2arbre(liste[0])

            self.droite = Arbre()
            self.droite.liste2arbre(liste[1])
        else:
            self.valeur = liste

    # Passage d'un arbre a une liste representant un arbre
    def arbre2liste(self, liste = [None, None]):
        if self.gauche != None and self.gauche.valeur == 0:
            liste[0] = [None, None]
            self.gauche.arbre2liste(liste[0])

        if self.gauche != None and self.gauche.valeur != 0:
            if self.droite.valeur != 0 and liste == None:
                liste = [None, None]
            liste[0] = self.gauche.valeur
            self.droite.arbre2liste(liste[1])

        if self.droite != None and self.droite.valeur == 0:
            liste[1] = [None, None]
            self.droite.arbre2liste(liste[1])

        if self.droite != None and self.droite.valeur != 0:
            liste[1] = self.droite.valeur

        return liste

    # Copiage de l'arbre passe en parametre
    def copie(self, arbre):
        if arbre.valeur != 0:
            self.valeur = arbre.valeur

        if arbre.gauche != None:
            self.gauche = Arbre()
            self.gauche.copie(arbre.gauche)

        if arbre.droite != None:
            self.droite = Arbre()
            self.droite.copie(arbre.droite)

    # Calcul du poids de part et d'autre de l'arbre
    def poids(self):
        g = self.gauche.poids_2([0])
        d = self.droite.poids_2([0])

        return g, d

    def poids_2(self, n):
        if self.valeur != 0:
            n[0] += self.valeur

        if self.gauche != None:
            self.gauche.poids_2(n)

        if self.droite != None:
            self.droite.poids_2(n)

        return n[0]

    # Calcul de la position de la tige par rapport au poids de part et d'autre
    def calcul_tige(self, longueur):
        poids = self.poids()

        return poids[1]*longueur/(poids[0]+poids[1])

    # Calcul du poids maximum de l'arbre
    def max(self):
        return self.max_2([0])

    def max_2(self, n):
        if self.valeur != 0:
            if n[0] < self.valeur:
                n[0] = self.valeur

        if self.gauche != None:
            self.gauche.max_2(n)

        if self.droite != None:
            self.droite.max_2(n)

        return n[0]

    # Calcul du poids minimum de l'arbre
    def min(self):
        return self.min_2([self.max()])

    def min_2(self, n):
        if self.valeur != 0:
            if n[0] > self.valeur:
                n[0] = self.valeur

        if self.gauche != None:
            self.gauche.min_2(n)

        if self.droite != None:
            self.droite.min_2(n)

        return n[0]

    # Calcul du nombre de poids dans l'arbre
    def nbr(self):
        return self.nbr_2([0])

    def nbr_2(self, n):
        if self.valeur != 0:
            n[0] += 1

        if self.gauche != None:
            self.gauche.nbr_2(n)

        if self.droite != None:
            self.droite.nbr_2(n)

        return n[0]

    # Regroupement des valeurs de l'arbre dans une liste
    def liste_simple(self):
        return self.liste_simple_2([])

    def liste_simple_2(self, liste = []):
        if self.valeur != 0:
            liste.append(self.valeur)

        if self.gauche != None:
            self.gauche.liste_simple_2(liste)

        if self.droite != None:
            self.droite.liste_simple_2(liste)

        return liste

    # Classement des poids de l'arbre en fonction d'une liste simple
    def classer(self, liste, n):
        if self.valeur != 0:
            n[1] = self.valeur
            self.valeur = liste[n[0]]
            n[0] += 1

        if self.gauche != None:
            self.gauche.classer(liste, n)

        if self.droite != None:
            self.droite.classer(liste, n)

    # Fonction principale permettant l'affichage du mobile dans la fenetre
    def equilibre(self, fenetre, h, n):
        if self.valeur != 0:
            n[0] += 1
            d = fenetre.intervalle*(1-math.pow(math.e, -self.valeur/(fenetre.max*1.5)))
            fenetre.canvas.create_line(fenetre.intervalle*n[0], 10+(h-1)*30, fenetre.intervalle*n[0], 10+h*30)

            if fenetre.max != fenetre.min:
                couleur = hex(int(255*(self.valeur-fenetre.min)/(fenetre.max-fenetre.min))*16**4+int(255-255*(self.valeur-fenetre.min)/(fenetre.max-fenetre.min))).split('x')[1]
            else:
                couleur = 'ff0000'
            if couleur == 'ff' and self.valeur == fenetre.max:
                couleur = 'ff0000'
            elif couleur == 'ff' and self.valeur == fenetre.min:
                couleur = '0000ff'
            if len(couleur) < 6:
                couleur = "0"+couleur

            fenetre.canvas.create_oval(fenetre.intervalle*n[0]-d, 10+h*30, fenetre.intervalle*n[0]+d, 10+h*30+d*2, fill='#'+couleur)
            fenetre.p = Label(fenetre.canvas, text = self.valeur, bg = "white")
            fenetre.p.pack()
            fenetre.canvas.create_window(fenetre.intervalle*n[0], (h+1)*30+d*2, window = fenetre.p)
        if self.gauche != None:
            h += 1
            self.gauche.equilibre(fenetre, h, n)
        if self.droite != None:
            self.droite.equilibre(fenetre, h, n)
            if self.droite.valeur != 0:
                if self.gauche.valeur != 0:
                    # Horizontal
                    fenetre.canvas.create_line(fenetre.intervalle*(n[0]-1), 10+30*(h-1), fenetre.intervalle*(n[0]), 10+30*(h-1))
                    # Vertical
                    fenetre.canvas.create_line(fenetre.intervalle*(n[0]-1)+self.calcul_tige(fenetre.intervalle), 10+30*(h-2), fenetre.intervalle*(n[0]-1)+self.calcul_tige(fenetre.intervalle), 10+30*(h-1))

                    self.tige = fenetre.intervalle*(n[0]-1)+self.calcul_tige(fenetre.intervalle)
                else:
                    # Horizontal
                    fenetre.canvas.create_line(self.gauche.tige, 10+30*(h-1), fenetre.intervalle*(n[0]), 10+30*(h-1))
                    # Vertical
                    fenetre.canvas.create_line(self.gauche.tige+self.calcul_tige(fenetre.intervalle*(n[0])-self.gauche.tige), 10+30*(h-2), self.gauche.tige+self.calcul_tige(fenetre.intervalle*(n[0])-self.gauche.tige), 10+30*(h-1))

                    self.tige = self.gauche.tige+self.calcul_tige(fenetre.intervalle*(n[0])-self.gauche.tige)
            else:
                if self.gauche.valeur != 0:
                    # Horizontal
                    fenetre.canvas.create_line(fenetre.intervalle*(n[0]-self.droite.nbr()), 10+30*(h-1), self.droite.tige, 10+30*(h-1))
                    # Vertical
                    fenetre.canvas.create_line(fenetre.intervalle*(n[0]-self.droite.nbr())+self.calcul_tige(self.droite.tige-fenetre.intervalle*(n[0]-self.droite.nbr())), 10+(h-2)*30, fenetre.intervalle*(n[0]-self.droite.nbr())+self.calcul_tige(self.droite.tige-fenetre.intervalle*(n[0]-self.droite.nbr())), 10+(h-1)*30)

                    self.tige = fenetre.intervalle*(n[0]-self.droite.nbr())+self.calcul_tige(self.droite.tige-fenetre.intervalle*(n[0]-self.droite.nbr()))
                else:
                    # Horizontal
                    fenetre.canvas.create_line(self.gauche.tige, 10+30*(h-1), self.droite.tige, 10+30*(h-1))
                    # Vertical
                    fenetre.canvas.create_line(self.gauche.tige+self.calcul_tige(self.droite.tige-self.gauche.tige), 10+(h-2)*30, self.gauche.tige+self.calcul_tige(self.droite.tige-self.gauche.tige), 10+(h-1)*30)

                    self.tige = self.gauche.tige+self.calcul_tige(self.droite.tige-self.gauche.tige)

    # Passage d'une representation de l'arbre d'un fichier a une liste simple
    def fichier2liste(self, s):
        try:
            f = open(s, "r")
        except:
            showwarning("Erreur de chargement", "Le fichier "+s+" n'existe pas")
            return
        r = f.readline()
        if not r:
            showwarning("Erreur de chargement", "Le fichier "+s+" est vide")
            return
        if '[' in r:
            return self.liste2arbre(eval(r))
        liste = [int(r)]
        for r in f.readlines():
            liste.append(int(r.split("\n")[0]))
        f.close()
        return self.liste2arbre(self.liste2liste(liste))

    # Passage d'une liste simple a une liste representant un arbre
    def liste2liste(self, liste):
        if len(liste) == 1:
            nouvelle_liste = liste[0]
        else:
            nouvelle_liste = [None, None]
            if len(liste) > 2:
                nouvelle_liste[0] = self.liste2liste(liste[:len(liste)//2+1])
                nouvelle_liste[1] = self.liste2liste(liste[len(liste)//2+1:])
            else:
                nouvelle_liste[0] = liste[0]
                nouvelle_liste[1] = liste[1]
        return nouvelle_liste

    # Generation aleatoire d'un arbre
    def generer2arbre(self, nombre, taille):
        liste = []
        for i in range(int(nombre)):
            liste.append(random.randint(1, int(taille)))
        return self.liste2arbre(self.liste2liste(liste))

try:
    if len(sys.argv) == 3:
        fenetre = Fenetre(sys.argv[1], sys.argv[2])
    else:
        fenetre = Fenetre()
except:
    fenetre = Fenetre()