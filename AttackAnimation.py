from enum import Enum

import arcade


class AttackType(Enum):
    """Les types d'attaques disponible dans le jeux"""
    Rock = 0
    Paper = 1
    Scissors = 2

class AttackAnimation(arcade.Sprite):
    """Hérite de la classe sprite d'arcade"""
    Attack_Scale = 0.5
    Animation_Speed = 5

    def __init__(self, attack_type):
        """Détermine les frames/textures possibles dépendament du type d'attaque"""
        super().__init__()
        self.attack_type = attack_type
        self.animation_update_time = 1/AttackAnimation.Animation_Speed
        self.time_since_last_swap = 0

        if self.attack_type == AttackType.Rock:
            self.textures = [
                arcade.load_texture("Assets/srock.png"),
                arcade.load_texture("Assets/srock-attack.png"),
            ]
        elif self.attack_type == AttackType.Paper:
            self.textures = [
                arcade.load_texture("Assets/spaper.png"),
                arcade.load_texture("Assets/spaper-attack.png"),
            ]
        else:
            self.textures = [
                arcade.load_texture("Assets/scissors.png"),
                arcade.load_texture("Assets/scissors-close.png"),
            ]

        self.scale = self.Attack_Scale
        self.current_texture = 0
        self.set_texture(self.current_texture)

    def on_update(self, delta_time: float = 1 / 60):
        """Fonction qui change l'image de l'animation a son prochain frame après un certain nombre de temps"""
        self.time_since_last_swap += delta_time

        if self.time_since_last_swap > self.animation_update_time:
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.current_texture = 0
                self.set_texture(self.current_texture)
            self.time_since_last_swap = 0.0



