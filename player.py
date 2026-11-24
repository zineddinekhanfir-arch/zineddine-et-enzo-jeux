import pygame
from pathlib import Path
from settings import gravite, force_saut, rouge

def creer_joueurs(fenetre):
    dossier = Path(__file__).resolve().parent / "sprit1"
    images_idle = sorted(dossier.rglob("walk/*.png"))
    if not images_idle:
        raise FileNotFoundError("Aucune image trouvée dans sprit1/walk")
    image_naruto = pygame.image.load(str(images_idle[0])).convert_alpha()
    image_naruto = pygame.transform.scale(image_naruto, (500, 400))
    largeur = fenetre.get_width()
    hauteur = fenetre.get_height()
    joueur1 = pygame.Rect(largeur // 5, hauteur - 250, 100, 390)
    joueur2 = pygame.Rect(largeur * 4 // 5, hauteur - 250, 100, 200)
    return joueur1, joueur2, image_naruto

def deplacer_joueurs(joueur1, joueur2, touches, largeur, hauteur, vitesse_y1, vitesse_y2):

    # on garde les anciennes positions des perso
    ancienne_x1 = joueur1.x
    ancienne_x2 = joueur2.x

    if touches[pygame.K_d]:
        joueur1.x += 10
    if touches[pygame.K_q]:
        joueur1.x -= 10
        touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        joueur2.x -= 10
    if touches[pygame.K_RIGHT]:
        joueur2.x += 10
    if touches[pygame.K_z] and joueur1.bottom == hauteur - 100:
        vitesse_y1 = force_saut
    if touches[pygame.K_UP] and joueur2.bottom == hauteur - 100:
        vitesse_y2 = force_saut
    vitesse_y1 += gravite
    vitesse_y2 += gravite
    joueur1.y += vitesse_y1
    joueur2.y += vitesse_y2
    if joueur1.bottom >= hauteur - 100:
        joueur1.bottom = hauteur - 100
        vitesse_y1 = 0
    if joueur2.bottom >= hauteur - 100:
        joueur2.bottom = hauteur - 100
        vitesse_y2 = 0
    if joueur1.left < -100:
        joueur1.left = -100
    if joueur1.right > largeur:
        joueur1.right = largeur
    if joueur2.left < 0:
        joueur2.left = 0
    if joueur2.right > largeur:
        joueur2.right = largeur

    # si les perso se rentrent dedans on annule leurs deplacement
    if joueur1.colliderect(joueur2):
        joueur1.x = ancienne_x1
        joueur2.x = ancienne_x2

    return vitesse_y1, vitesse_y2

def dessiner_joueurs(fenetre, joueur1, joueur2, image_naruto):
    fenetre.blit(image_naruto, joueur1)
    pygame.draw.rect(fenetre, rouge, joueur2)


# AJOUT : LA ON CHARGE LES SPRITES DE GOKU

# la ont cree une fonction pour recuperer tt les animations
def charger_goku():

    # la ont trouve notre dossier GOKU
    dossier = Path(__file__).resolve().parent / "GOKU"

    # la ont cree un dictionnaire pour ranger les images
    animations = {}

    # la ont met les noms des dossiers
    dossiers = {
        "marche": "Goku_Marche_Detaillee",
        "course": "Goku_Course",
        "saut": "Goku_Saut_3_Frames",
        "dash": "Goku_Dash_2_Frames",
        "kamehameha": "Goku_Kamehameha_Postures_4_Frames",
        "jajanken": "Goku_Jajanken_Corrige_3_Frames"
    }

    # la ont charge goku quand il bouge pas
    image = pygame.image.load(str(dossier / "goku.png")).convert_alpha()

    # la ont choisit la hauteur de goku
    hauteur_goku = 400

    # la ont calcule sa largeur pour pas qu'il soit etire
    largeur_goku = int(image.get_width() * hauteur_goku / image.get_height())

    # la ont change sa taille sans le deformer
    image = pygame.transform.scale(image, (largeur_goku, hauteur_goku))

    # la ont garde cette image dans repos
    animations["repos"] = [image]

    # la ont passe dans chaque dossier
    for action, nom_dossier in dossiers.items():

        # la ont cree une liste vide pour les images
        animations[action] = []

        # la ont cherche tt les png sauf les grandes planches
        chemins = sorted((dossier / nom_dossier).glob("*.png"))

        # la ont passe sur chaque image
        for chemin in chemins:

            # la ont ignore les planches completes
            if "planche" in chemin.name:
                continue

            # la ont charge notre image
            image = pygame.image.load(str(chemin)).convert_alpha()

            # la ont choisit la hauteur de goku
            hauteur_goku = 400

            # la ont calcule sa largeur pour pas qu'il soit etire
            largeur_goku = int(image.get_width() * hauteur_goku / image.get_height())

            # la ont met la taille de goku sans le deformer
            image = pygame.transform.scale(image, (largeur_goku, hauteur_goku))

            # la ont ajoute l'image dans la liste
            animations[action].append(image)

    # la ont renvoie tt les animations
    return animations


# AJOUT : LA ON DESSINE GOKU

def dessiner_goku(fenetre, joueur2, animations, action, numero_image, direction):

    # la ont recupere les images de l'action
    images = animations[action]

    # la ont choisit l'image a afficher
    image = images[numero_image % len(images)]

    # la si goku regarde a gauche
    if direction == "gauche":

        # la ont retourne son image
        image = pygame.transform.flip(image, True, False)

    # la ont place ses pieds au niveau du joueur 2
    position = image.get_rect(midbottom=joueur2.midbottom)

    # la ont affiche goku
    fenetre.blit(image, position)


# AJOUT : LA ON CHARGE LES ANIMATIONS DE NARUTO

def charger_naruto():

    # la ont trouve le dossier des nouveaux sprites
    dossier = Path(__file__).resolve().parent / "sprit1"

    # la ont cree un dictionnaire pour ranger les animations
    animations = {}

    # la ont met les noms des animations et leurs dossiers
    dossiers = {
        "repos": "idle",
        "marche": "walk",
        "course": "walk",
        "saut": "walk",
        "dash": "walk",
        "attaque1": "attack",
        "attaque2": "attack",
        "special": "attack"
    }

    # la ont passe dans chaque dossier
    for action, nom_dossier in dossiers.items():

        # la ont cree une liste vide
        animations[action] = []

        # la ont recupere les images dans l'ordre
        chemins = sorted(dossier.rglob(f"{nom_dossier}/*.png"))

        # AJOUT : la ont regarde combien d'images ont a trouve
        print("Animation Naruto :", action, "- Images trouvées :", len(chemins))

        # AJOUT : la si aucune image est trouvee ont explique le probleme
        if not chemins:
            print("ATTENTION : aucune image dans", dossier / nom_dossier)

        # la ont charge chaque image
        for chemin in chemins:

            # la ont ouvre l'image
            image = pygame.image.load(str(chemin)).convert_alpha()

            # la ont choisit une taille identique pour toutes les animations
            # On garde la hauteur de Naruto
            hauteur_naruto = 400

            # On calcule la largeur pour conserver ses proportions
            largeur_naruto = int(
            image.get_width() * hauteur_naruto / image.get_height()
)

# On redimensionne sans déformer Naruto
            image = pygame.transform.scale(
    image,
    (largeur_naruto, hauteur_naruto)
)

            # la ont ajoute l'image dans son animation
            animations[action].append(image)

    # la ont renvoie toutes les animations
    return animations


# AJOUT : LA ON DESSINE NARUTO AVEC SES ANIMATIONS

def dessiner_naruto(fenetre, joueur1, animations, action, numero_image, direction):

    # la ont recupere les images de l'animation
    images = animations[action]

    # AJOUT : la si aucune image est trouvee ont evite de faire planter le jeu
    if not images:
        return

    # la ont choisit l'image a afficher
    image = images[numero_image % len(images)]

    # la ont retourne naruto si il regarde a gauche
    if direction == "gauche":
        image = pygame.transform.flip(image, True, False)

    # la ont place ses pieds au niveau du joueur 1
    position = image.get_rect(midbottom=joueur1.midbottom)

    # la ont affiche naruto
    fenetre.blit(image, position)