# la on importe les bibliotheques et les fonctions de nos autres fichiers
import pygame
from pathlib import Path
from settings import fond, bleu, gris
from player import creer_joueurs, deplacer_joueurs, dessiner_joueurs
from player import charger_goku, dessiner_goku
from player import charger_naruto, dessiner_naruto
from combat import attaquer, dessiner_vies

# on prepare pygame et on cree la fenetre du jeux
pygame.init()
fenetre = pygame.display.set_mode((1910, 1080), pygame.RESIZABLE)

# la on cherche le dossier du projet et toutes les images des maps
dossier = Path(__file__).resolve().parent

# on lance la musique du jeux en boucle
pygame.mixer.init()
pygame.mixer.music.load(str(dossier / "song 1.mp3"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

maps = sorted((dossier / "Maps").glob("*.png"))

# on charge les images une par une et on les met dans une liste
images_maps = []

for chemin in maps:
    image = pygame.image.load(str(chemin)).convert()
    images_maps.append(image)

print("Nombre de maps trouvées :", len(images_maps))

# on recupere les dimensions de notre fenetre et on cree les perso
largeur = fenetre.get_width()
hauteur = fenetre.get_height()

joueur1, joueur2, image_naruto = creer_joueurs(fenetre)

# les variables pour le fonctionnement du jeux et les sauts
jeu = True
vitesse_y1 = 0
vitesse_y2 = 0

horloge = pygame.time.Clock()


# partie du menu d'accueil

menu = True

# on prepare les tailles des textes pour le menu
police = pygame.font.Font(None, 100)
police_bouton = pygame.font.Font(None, 60)

# tant que le menu est vrai on reste dans cette boucle
while menu:

    # la on regarde si le joueur ferme la fenetre ou clique sur jouer
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            menu = False
            jeu = False

        if evenement.type == pygame.MOUSEBUTTONDOWN:
            if bouton.collidepoint(evenement.pos):
                menu = False

    # on met le fond et on affiche le titre au milieu
    fenetre.fill(fond)

    titre = police.render("STREET CLASH", True, (255, 255, 255))
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 300))

    # la on cree le bouton jouer avec le rectangle et le texte au milieu
    bouton = pygame.Rect(largeur // 2 - 150, 500, 300, 100)
    pygame.draw.rect(fenetre, bleu, bouton)

    texte = police_bouton.render("JOUER", True, (255, 255, 255))
    fenetre.blit(texte, (bouton.centerx - texte.get_width() // 2, bouton.centery - texte.get_height() // 2))

    pygame.display.flip()
    horloge.tick(60)


# partie pour choisir les maps

choix_map = jeu
map_selectionnee = 0
rectangles_maps = []

# on a mis le choix des maps dans une fonction pour pouvoir y revenir apres un combat
def choisir_map():

    global jeu, map_selectionnee

    choix_map = jeu
    rectangles_maps = []

    while choix_map:

        # on regarde les actions du joueur pour savoir si il quitte ou choisit une map
        for evenement in pygame.event.get():

            if evenement.type == pygame.QUIT:
                choix_map = False
                jeu = False

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    choix_map = False
                    jeu = False

            # la on regarde sur quelle map le joueur a cliquer
            if evenement.type == pygame.MOUSEBUTTONDOWN:

                for i, rectangle in enumerate(rectangles_maps):

                    if rectangle.collidepoint(evenement.pos):
                        map_selectionnee = i
                        choix_map = False
                        break

        if not jeu:
            break

        # on affiche le fond et le titre du choix des maps
        fenetre.fill(fond)

        titre = police_bouton.render("CHOISIS TA MAP", True, (255, 255, 255))
        fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 100))

        rectangles_maps = []

        # la on reduit les images pour faire des miniatures
        # avec les calculs de x et y on peut mettre 4 maps par ligne
        for i, image in enumerate(images_maps):

            miniature = pygame.transform.scale(image, (300, 180))

            x = 100 + (i % 4) * 400
            y = 250 + (i // 4) * 250

            rectangle = pygame.Rect(x, y, 300, 180)
            rectangles_maps.append(rectangle)

            fenetre.blit(miniature, (x, y))

        pygame.display.flip()
        horloge.tick(60)


# si le jeux est encore ouvert on lance le choix des maps
if jeu:
    choisir_map()


# la on prepare toutes les animations de goku
# au debut il bouge pas et regarde vers la gauche

animations_goku = charger_goku()
action_goku = "repos"
numero_image_goku = 0
compteur_goku = 0
direction_goku = "gauche"
temps_attaque = 0


# on fait la meme chose pour naruto sauf que lui regarde a droite

animations_naruto = charger_naruto()
action_naruto = "repos"
numero_image_naruto = 0
compteur_naruto = 0
direction_naruto = "droite"
temps_attaque_naruto = 0


# les deux perso commence avec 100 points de vie
vie_naruto = 100
vie_goku = 100

# au debut personne a gagner donc on met None
gagnant = None
police_victoire = pygame.font.Font(None, 130)

# on prepare le bouton pour recommencer une partie
bouton_restart = pygame.Rect(
    largeur // 2 - 150,
    hauteur // 2 + 100,
    300,
    80
)


# ici cest la boucle principale du jeux
while jeu:

    # on recupere les actions que font les joueurs
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            jeu = False

        # si la partie est finit et que le joueur clique sur restart
        # on le renvoie au choix des maps
        if evenement.type == pygame.MOUSEBUTTONDOWN and gagnant is not None:

            if bouton_restart.collidepoint(evenement.pos):

                choisir_map()

                if not jeu:
                    break

                # la on remet les perso a leurs positions de depart
                # et on remet toutes les valeurs comme au debut
                joueur1, joueur2, image_naruto = creer_joueurs(fenetre)

                vie_naruto = 100
                vie_goku = 100

                vitesse_y1 = 0
                vitesse_y2 = 0

                action_naruto = "repos"
                action_goku = "repos"

                numero_image_naruto = 0
                numero_image_goku = 0

                compteur_naruto = 0
                compteur_goku = 0

                temps_attaque_naruto = 0
                temps_attaque = 0

                direction_naruto = "droite"
                direction_goku = "gauche"

                gagnant = None

                continue

        # la on gere les touches du clavier
        if evenement.type == pygame.KEYDOWN:

            if evenement.key == pygame.K_ESCAPE:
                jeu = False

            # si quelqu'un a gagner on peut plus attaquer
            if gagnant is not None:
                continue

            # les animations d'attaque de goku
            # on remet l'image a 0 pour que l'animation recommence du debut
            if evenement.key == pygame.K_DOWN:

                action_goku = "kamehameha"
                numero_image_goku = 0
                temps_attaque = 32

            if evenement.key == pygame.K_RCTRL:

                action_goku = "jajanken"
                numero_image_goku = 0
                temps_attaque = 24

            # les 3 attaques de naruto avec les touches A E et R
            # chaque attaque fait pas le meme nombre de degats

            if evenement.key == pygame.K_a:

                action_naruto = "attaque1"
                numero_image_naruto = 0
                temps_attaque_naruto = 64

                vie_goku = attaquer(joueur1, joueur2, 5, vie_goku)

            if evenement.key == pygame.K_e:

                action_naruto = "attaque2"
                numero_image_naruto = 0
                temps_attaque_naruto = 64

                vie_goku = attaquer(joueur1, joueur2, 10, vie_goku)

            if evenement.key == pygame.K_r:

                action_naruto = "special"
                numero_image_naruto = 0
                temps_attaque_naruto = 96

                vie_goku = attaquer(joueur1, joueur2, 15, vie_goku)

            # la on recupere le caractere de la touche
            # pour que sa marche aussi avec un clavier azerty
            touche = evenement.unicode

            # les attaques de goku avec 8 9 et 0
            # comme naruto il a une attaque a 5 10 et 15 degats

            if touche in ("8", "_") or evenement.key == pygame.K_KP8:

                action_goku = "jajanken"
                numero_image_goku = 0
                temps_attaque = 24

                vie_naruto = attaquer(joueur2, joueur1, 5, vie_naruto)

            if touche in ("9", "ç") or evenement.key == pygame.K_KP9:

                action_goku = "jajanken"
                numero_image_goku = 0
                temps_attaque = 24

                vie_naruto = attaquer(joueur2, joueur1, 10, vie_naruto)

            if touche in ("0", "à") or evenement.key == pygame.K_KP0:

                action_goku = "kamehameha"
                numero_image_goku = 0
                temps_attaque = 32

                vie_naruto = attaquer(joueur2, joueur1, 15, vie_naruto)

            # on verifie les points de vie pour savoir qui a gagner
            if vie_naruto <= 0:
                gagnant = "GOKU"

            if vie_goku <= 0:
                gagnant = "NARUTO"

    if not jeu:
        break

    # on recupere les touches qui sont maintenu
    touches = pygame.key.get_pressed()

    # on laisse les perso bouger seulement si la partie est pas finit
    if gagnant is None:

        vitesse_y1, vitesse_y2 = deplacer_joueurs(
            joueur1, joueur2, touches, largeur, hauteur,
            vitesse_y1, vitesse_y2
        )

    # la on gere toutes les animations des deux perso
    if gagnant is None:

        # animation de goku
        # le compteur permet de changer d'image tout les 8 tours de boucle
        compteur_goku += 1

        if compteur_goku % 8 == 0:
            numero_image_goku += 1

        # on change le sens de goku selon la touche appuyer
        if touches[pygame.K_LEFT]:
            direction_goku = "gauche"

        if touches[pygame.K_RIGHT]:
            direction_goku = "droite"

        # tant que le temps d'attaque est pas a 0 on garde l'animation d'attaque
        # sinon on regarde si goku marche saute ou reste sur place
        if temps_attaque > 0:

            temps_attaque -= 1

        else:

            action_goku = "repos"

            if touches[pygame.K_LEFT] or touches[pygame.K_RIGHT]:

                action_goku = "marche"

            if joueur2.bottom < hauteur - 100:

                action_goku = "saut"


        # animation de naruto c'est le meme principe que goku
        compteur_naruto += 1

        if compteur_naruto % 8 == 0:
            numero_image_naruto += 1

        # la on change sa direction avec Q et D
        if touches[pygame.K_q]:
            direction_naruto = "gauche"

        if touches[pygame.K_d]:
            direction_naruto = "droite"

        # on attend que son attaque soit finit avant de changer d'animation
        if temps_attaque_naruto > 0:

            temps_attaque_naruto -= 1

        else:

            action_naruto = "repos"

            if touches[pygame.K_q] or touches[pygame.K_d]:

                action_naruto = "marche"

            if joueur1.bottom < hauteur - 100:

                action_naruto = "saut"


    # la on recupere la map que le joueur a choisit
    # et on l'agrandit pour qu'elle prenne toute la fenetre
    fenetre.fill(fond)

    image_fond = images_maps[map_selectionnee]
    image_fond = pygame.transform.scale(image_fond, (largeur, hauteur))
    fenetre.blit(image_fond, (0, 0))

    # ancien sol qu'on utilisait avant
    #pygame.draw.rect(fenetre, gris, (0, hauteur - 100, largeur, 100))

    # on affiche naruto avec sa position son action et son animation
    dessiner_naruto(
        fenetre,
        joueur1,
        animations_naruto,
        action_naruto,
        numero_image_naruto,
        direction_naruto
    )

    # on fait pareil pour goku
    dessiner_goku(
        fenetre,
        joueur2,
        animations_goku,
        action_goku,
        numero_image_goku,
        direction_goku
    )

    # on affiche les barres de vie des deux perso
    dessiner_vies(fenetre, vie_naruto, vie_goku)

    # si un joueur a gagner on affiche son nom avec WIN au milieu
    if gagnant is not None:

        texte_victoire = police_victoire.render(
            gagnant + " WIN !", True, (255, 215, 0)
        )

        rectangle_texte = texte_victoire.get_rect(
            center=(largeur // 2, hauteur // 2)
        )

        fenetre.blit(texte_victoire, rectangle_texte)

        # la on met le bouton restart en dessous du texte de victoire
        bouton_restart.center = (
            largeur // 2,
            hauteur // 2 + 140
        )

        pygame.draw.rect(
            fenetre,
            bleu,
            bouton_restart,
            border_radius=15
        )

        texte_restart = police_bouton.render(
            "RESTART", True, (255, 255, 255)
        )

        fenetre.blit(
            texte_restart,
            texte_restart.get_rect(center=bouton_restart.center)
        )

    # on actualise la fenetre et on limite le jeux a 60 fps
    pygame.display.flip()
    horloge.tick(60)

# quand on sort de la boucle sa ferme pygame
pygame.quit()