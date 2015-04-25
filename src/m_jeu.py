# # # # # # # # # # # # # # # # #
#				#
#         Projet de MDD         #
#                               #
#       fichier : m_jeu.py      #
#                               #
# # # # # # # # # # # # # # # # #

#-*-coding:utf-8-*-

#Importation des modules fournis avec python :
import time
import os

#Importation du module Pyglet pour python 3. Si il n'est pas trouvé sur le système, on utilise la version présente dans le dossier src :
try :
	import pyglet
except ImportError : 
	import pyglet_py3 as pyglet
	print("Bibliothèque pyglet non trouvée pour python3, utilisation de la version de pyglet du dossier src/ (",pyglet.version,").") 

#Importation des constantes :
import constantes as cs
#Importation de notre module qui gère la carte et la position du joueur :
import m_carte as mc

class Jeu :
	"""Classe qui gère le jeu, la Bibliothèque pyglet, les évènements claviers, la fenêtre et le son."""

	def __init__(self, carte_type = "defaut") :
		"""Constructeur : 
			carte_type : type de carte à utiliser durant le jeu. (carte nommée selon l'exemple : carte_NOM.txt et placée dans le dossier cartes)"""

		#Réglage du dossier de travail de pyglet pour le dossier racine du projet, sinon il ne trouve pas les différents composants :
		working_dir = os.path.dirname(os.path.realpath(__file__))
		pyglet.resource.path = [os.path.join(working_dir,'..')]
		pyglet.resource.reindex()

		#Chargement de la carte.
		self.carte = mc.Carte(carte_type)
		#Chargement des sons
		self.charger_sons()
		#Lecteurs (environnement(s), action(s), heartbeats,...)
		self.creer_lecteurs()	
		#Fenêtre (activation du plein écran ?par défaut?)
		self.creer_fenetre()
		#Création des evènements... (clavier, ...) ou utilisation de raw_input? 
		self.init_events()

		#Initialisation de la vie du personnage
		self.vie = 3 #A changer

	def charger_sons(self) :
		"""Charge tous les sons du dossier 'sons' et les range dans un dictionnaire avec pour étiquette le nom du fichier son sans l'etension '.wav'. """
	  
		#Peut-être charger les sons automatiquement avec os.listdir() et charger tous les sons au format wav du répertoire 'sons' : ("Un peu" BOURIN et peut-être bouffe-mémoire)
		#Pour les sons courts, peut-être : "sound = pyglet.resource.media('shot.wav', streaming=False)", prends plus de mémoire mais accès plus rapide.
		
		#On crée le dictionnaire de sons :
		self.sons = {}
		try :
			#On récupère la liste des fichiers du dossier 'sons' :
			liste_sons = os.listdir("sons")

			#On ne garde que les fichiers 'wav' :
			liste_sons = [ fichier for fichier in liste_sons if fichier.find(".wav") != -1]

			#On ouvre les sons avec pyglet et on les range dans le dictionnaire 'sons' avec pour étiquette le nom du fichier son sans l'etension '.wav' :
			for son in liste_sons :
				self.sons[son.replace(".wav",'')] = pyglet.resource.media(os.path.join("sons", son))

		except FileNotFoundError :
			print("Le dossier 'sons' contenant les sons (héhé) n'a pas été trouvé.")
			self.sons = None

	def creer_lecteurs(self) :
		"""Crée les lecteurs pyglet, les lecteurs env, eau, et heartbeat sont réglés pour tourner en boucle sur la musique en cours : 
			- env : Pour l'environnement.
			- eau : Pour l'eau à proximité de la case.
			- action : Pour les différentes actions (déplacements, coups,...).
			- monstre : Bruit du monstre qui indique que l'on est sur la case d'un monstre.
			- heartbeat : Si il ne reste qu'une vie, on entend un bâttement de coeur.
		"""
		
		self.lecteurs = {}
		for type in ("env", "eau", "monstre", "action", "heartbeat"):
			self.lecteurs[type] = pyglet.media.Player()
			if type in ("env", "eau", "heartbeat") :
				self.lecteurs[type].eos_action = self.lecteurs[type].EOS_LOOP
			if type in ("eau", "heartbeat") :
				self.lecteurs[type].queue(self.sons[type])
				self.lecteurs.volume = 0.1
 
	def creer_fenetre(self) :
		"""Crée la fenêtre pyglet en plein écran."""
		self.window = pyglet.window.Window(fullscreen = True)

	def init_events(self) :
		"""crée les évenements : 
	- claviers : 
		- flèches directionnelles : se déplacer
		- F : plein écran
		- H : aide
		- ..."""
		@self.window.event
		def on_key_press(symbol, modifiers):
			#Fullscreen
			if symbol == pyglet.window.key.F :
				self.window.set_fullscreen(not self.window.fullscreen)
			#Aide
			elif symbol == pyglet.window.key.H :
				self.afficher_aide()
			#déplacements
			elif symbol == pyglet.window.ket.UP :
				self.move("NORD")
			elif symbol == pyglet.window.ket.DOWN :
				self.move("SUD")
			elif symbol == pyglet.window.ket.RIGHT :
				self.move("EST")
			elif symbol == pyglet.window.ket.LEFT :
				self.move("OUEST")
				
		def on_draw():
			self.window.clear()
	
	def move(self, direction) :
		"""Fonction qui déplace le joueur et gère ce qui peut y arriver (mort si environnement dangereux, combat...).
			- direction : prend un chaîne de caractère parmis ("OUEST", "EST", "NORD", "SUD")."""
		
		#On déplace le joueur su la carte et on récupère le code de la case d'arrivée. 
		case = self.carte.move(direction)
		#On récupère les informations de proximité de la case (eau, pont...), qui sont écrits sous forme de centaines et au dessus.
		infos_prox = case / 100
		case = case - infos_prox
		print(case , infos_prox)
		
		
		if infos_prox & PROX_EAU == PROX_EAU :
			eau.play()
		else :
			eau.pause()
			
	def afficher_aide(self) :
		"""Fonction qui affiche l'aide (tiens, tiens...)."""
		pass

	def fin(self, type) :
		"""Fonction qui gère la fin selon s'il y a victoire ou mort.
			- type : chaîne de caractère décrivant la fin parmis celles se trouvant dans le fichier constantes, les fichiers sons associés doivent exister."""

		self.lecteurs["env"].queue(type)
		

	def run(self) :
	  
		pyglet.app.run()

	#Autres fonctions
