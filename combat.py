
import pygame

# Chaque joueur commence avec 100 points de vie
vie_naruto = 100
vie_goku = 100


# Cette fonction permet d'attaquer un adversaire
def attaquer(attaquant, adversaire, degats, vie):

    # On calcule la distance entre les deux joueurs
    distance = abs(attaquant.centerx - adversaire.centerx)

    # On vérifie aussi qu'ils sont à une hauteur proche
    hauteur = abs(attaquant.bottom - adversaire.bottom)

    # Si les joueurs sont assez proches, l'attaque touche
    if distance < 250 and hauteur < 150:

        # On enlève les dégâts à la vie
        vie -= degats

    # La vie ne peut jamais être négative
    return max(0, vie)


# Cette fonction dessine les deux barres de vie
def dessiner_vies(fenetre, vie_naruto, vie_goku):

    largeur = fenetre.get_width()

    # Fond rouge des barres
    pygame.draw.rect(fenetre, (180, 0, 0), (50, 40, 400, 30))
    pygame.draw.rect(fenetre, (180, 0, 0), (largeur - 450, 40, 400, 30))

    # Partie verte correspondant à la vie restante
    pygame.draw.rect(fenetre, (0, 220, 0), (50, 40, vie_naruto * 4, 30))
    pygame.draw.rect(fenetre, (0, 220, 0), (largeur - 450, 40, vie_goku * 4, 30))

    # On écrit les noms et les PV
    police = pygame.font.Font(None, 32)

    texte_naruto = police.render(f"Naruto : {vie_naruto} PV", True, (255, 255, 255))
    texte_goku = police.render(f"Goku : {vie_goku} PV", True, (255, 255, 255))

    fenetre.blit(texte_naruto, (50, 10))
    fenetre.blit(texte_goku, (largeur - 450, 10))
