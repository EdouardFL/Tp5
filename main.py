import random

import arcade

# import arcade.gui

from AttackAnimation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.


class MyGame(arcade.Window):

    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player = None
        self.computer = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.player_score = 0
        self.computer_score = 0
        self.computer_attack_type = None
        self.computer_attack_sprite = None
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = None
        self.winState = None

    def setup(self):
        """
        On initialise les variables du jeu ainsi que certains sprites. 
       """
        self.game_state = GameState.NOT_STARTED
        self.player = arcade.Sprite("Assets/faceBeard.png", 0.5, center_x=150, center_y=350)
        self.computer = arcade.Sprite("Assets/compy.png", 2.40, center_x=874, center_y=350)

        self.rock = AttackAnimation(AttackType.Rock)
        self.rock.center_x = 200
        self.rock.center_y = 100

        self.paper = AttackAnimation(AttackType.Paper)
        self.paper.center_x = 300
        self.paper.center_y = 100

        self.scissors = AttackAnimation(AttackType.Scissors)
        self.scissors.center_x = 400
        self.scissors.center_y = 100

    def victory_logic(self):
        """
        Logique qui représente les règles du jeu roche papier ciseaux.
        """
        if self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Rock:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Paper:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Scissors:
            return "Win"

        if self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Paper:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Scissors:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Rock:
            return "Win"

        if self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Scissors:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Rock:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Paper:
            return "Win"

    def validate_victory(self):
        """
        Fonction qui valide la victoire selon les règles du jeu.
        """
        Result = self.victory_logic()

        if Result:
            self.game_state = GameState.ROUND_DONE

        if Result == "Win":
            #Si le joeur gagne, on ajoute +1 a son score et on met le winState a Win
            self.player_score += 1
            self.winState = "Win"
            
        elif Result == "Loss":
            #Si le joeur perd, on soustrait -1 a son score et on met le winState a Loss
            self.computer_score += 1
            self.winState = "Loss"

        elif Result == "Draw":
            #Si il y a une égalité, on met le winState a Draw
            self.winState = "Draw"

        if self.player_score == 3 or self.computer_score == 3:
            #Si un des joeur gagne (score égale a trois), le partie est terminé
            self.game_state = GameState.GAME_OVER

    def draw_possible_attack(self):
        """
        Fonction qui dessine tout les actions possible lors de la sélection
        """  
        xPos = 200
        for i in range(1,4):
            #For loop qui dessiner les trois rectangles, on offset la position du rectangle de 100 pixel chaque fois
            arcade.draw_rectangle_outline(
                xPos,
                100,
                100,
                100,
                arcade.color_from_hex_string("F04848")
            )

            xPos += 100

        #On dessine le rectangle de l'ordinateur
        arcade.draw_rectangle_outline(
                800,
                100,
                100,
                100,
                arcade.color_from_hex_string("F04848")
            )

        #Si le joueur a déja séléctionner une attaque, on dessine seulement cette attaque 
        if self.player_attack_chosen == AttackType.Rock:
            self.rock.draw()
        elif self.player_attack_chosen == AttackType.Paper:
            self.paper.draw()
        elif self.player_attack_chosen == AttackType.Scissors:
            self.scissors.draw()
        else:
            #On dessine les images représentants les choix possibles
            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()
        

    def draw_computer_attack(self):
        """
        Fonction qui dessine le sprite choisi par l'ordinateur
        """
        if self.computer_attack_sprite:
            self.computer_attack_sprite.center_x = 800
            self.computer_attack_sprite.center_y = 100
            self.computer_attack_sprite.draw()


    def computer_attack(self):
        """
        Fonction qui effectue la logique derrière l'attaque de l'odinateur,
        On génére un nombre aléatoire et associe ce dernier a un type d'attaque,
        Ensuite, on change le type d'attaque de l'ordinateur et le sprite que l'ordinateur va dessiner
        """
        attack_index = random.randint(0, 2)
        if attack_index == 0:
            self.computer_attack_type = AttackType.Rock
            self.computer_attack_sprite = AttackAnimation(AttackType.Rock)
        elif attack_index == 1:
            self.computer_attack_type = AttackType.Paper
            self.computer_attack_sprite = AttackAnimation(AttackType.Paper)
        elif attack_index == 2:
            self.computer_attack_type = AttackType.Scissors
            self.computer_attack_sprite = AttackAnimation(AttackType.Scissors)

    def draw_scores(self):
        """
       Fonction qui montre les scores du joueur et de l'ordinateur
       """
        
        #Montre le score du joueur
        arcade.draw_text("Votre score est:" + str(self.player_score),
            -220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        #Montre le score de l'ordinateur
        arcade.draw_text("Le score de l'ordinateur est:" + str(self.computer_score),
            220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")

    def draw_instructions(self):
        """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur.
       """
        string = None
        #La varible string est changé selon le gameState et est ensuite transformé en texte
        if self.game_state == GameState.GAME_OVER:
            if self.player_score > self.computer_score: 
                #Si la partie est terminé et le score du joeur est plus grand que celui de l'ordinateur, on affiche ceci
                string = "La partie est terminé, Vous avez gagné la partie ! Appuyer sur espace pour rejouer !"
            else:
                #Sinon, l'ordinateur gagne est on affiche ceci
                string = "La partie est terminé, vous avez perdu la partie. Appuyer sur espace pour rejouer !"

        elif self.game_state == GameState.NOT_STARTED:
            #Si la ronde n'est pas commencé, on affiche ceci
            string = "Appuyer sur espace pour commencer la partie !"
        elif self.game_state == GameState.ROUND_ACTIVE:
            #Si il y a une ronde en cours, on affiche ceci
            string = "Clicker sur une image pour attaquer !"
        elif self.game_state == GameState.ROUND_DONE:
            if self.winState == "Win":
                #Si la ronde est terminé et le joeur a gagné, on affiche ceci
                string = "Vous avez gagné ! Appuyer sur espace pour commencer une nouvelle ronde !"
            elif self.winState == "Loss":
                #Si la ronde est terminé et le joeur a pardu, on affiche ceci
                string = "Vous avez Perdu ! Appuyer sur espace pour commencer une nouvelle ronde !"
            elif self.winState == "Draw":
                #Si il y a une égalité, on affiche ceci
                string = "Égalité ! Appuyer sur espace pour commencer une nouvelle ronde !"
        
        #On dessine les instructions avec la variable string comme texte
        arcade.draw_text(string,
            350,
            300,
            arcade.color.BLACK,
            20,
            width=300,
            align="center",)
        
    def on_draw(self):
        """Fonction qui dessine l'ensemble des visuels chaque frame"""
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.player.draw()
        self.computer.draw()

        self.draw_computer_attack()

        self.draw_instructions()
        self.draw_possible_attack()
        self.draw_scores()

    def on_update(self, delta_time):
        """Fonction qui update les animations et effectue le combat entre l'ordinateur une fois que le joeur a attaqué"""
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update()
            self.paper.on_update()
            self.scissors.on_update()   

            if self.player_attack_chosen:
                self.computer_attack()
                self.validate_victory()

    def on_key_press(self, key, key_modifiers):
        """Fonction qui est activé chaque fois que l'utilisateur appuye sur une touche"""
        if key == 32:
            #Si la touche espace est activé, on change l'état du jeu
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.ROUND_DONE:
                #Lorsqu'on passe de ROUND_DONE a ROUND_ACTIVE, on reset certaines variables pour refaire une ronde 
                self.game_state = GameState.ROUND_ACTIVE
                self.winState = None
                self.computer_attack_type = None
                self.computer_attack_sprite = None
                self.player_attack_chosen = None

            elif self.game_state == GameState.GAME_OVER:
                #Lorsqu'on passe de GAME_OVER a ROUND_ACTIVE, on reset certaines variables pour recommencer une partie
                self.game_state = GameState.ROUND_ACTIVE
                self.player_score = 0
                self.computer_score = 0
                self.computer_attack_type = None
                self.player_attack_chosen = False
                self.draw_round = None

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Fonction qui est activé a chaque fois que l'utilisateur cliquer avec sa souris"""
        if self.game_state == GameState.ROUND_ACTIVE:
            "Si il y a une ronde active et qu'on clique sur un des trois sprites(Roche, papier ou ciseaux), on change l'attaque choisi par le joeur dépendament du sprite cliqué"
            if self.rock.collides_with_point((x,y)):
                self.player_attack_chosen = AttackType.Rock

            elif self.paper.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Paper

            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Scissors

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
