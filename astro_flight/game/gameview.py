import arcade
import arcade.gui
import random
from game import constants
from game.constructor import Constructor
from game.lives import Lives
from game.pauseview import PauseView
from game.gameover import GameOverView

class GameView(arcade.View):
    """Main Game window
    """
    def __init__(self):
        """Initialize Game window
        """
        
        # Sets size of the window and title
        super().__init__()
        
        # Variable with background image
        self.background = arcade.load_texture(constants.PATH + "/images/background.png")
        
        # Variable with sound
        self.explosion = arcade.load_sound(constants.PATH + "/sounds/explosion.wav")
        self.trophy = arcade.load_sound(constants.PATH + "/sounds/trophy.wav")
        
        # Setup game
    def setup(self):
        """Called when the view is loaded
        """
        
        # Sets up lives
        self.lives = constants.LIVES
        
        # Variable with Score
        self.score = 0
        
        # Mouse visibility
        self.window.set_mouse_visible(False)
        
        self.constructor = Constructor()
    
    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        W/A/S/D: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        
        # Checks for key presses and their consequences
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()
        
        if symbol == arcade.key.P:
            # Pause the game
            # Pauses scheduling of asteroids
            self.constructor.pause()
            pause = PauseView(self)
            self.window.show_view(pause)

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            # Move up
            self.constructor.player.change_y = 8

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            # Move down
            self.constructor.player.change_y = -8

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            # Move left
            self.constructor.player.change_x = -8

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            # Move right
            self.constructor.player.change_x = 8

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        
        # Stops movement when key is released
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.constructor.player.change_y = 0

        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.constructor.player.change_x = 0
    
    def on_update(self, delta_time):
        """Call this to update your game at the end of each frame"""
    
        # Adds score for time passed    
        self.score += 0.05
        
        # Updates all the sprites
        self.constructor.scene.update()

        # Collision detection
        if self.constructor.player.collides_with_list(self.constructor.scene.get_sprite_list("Obstacles")):
            
            # Removes asteroid from near the player to prevent from colliding with it again
            for asteroid in (self.constructor.scene.get_sprite_list("Obstacles")):
                
                if int(asteroid.center_y) < 300:
                    asteroid.remove_from_sprite_lists()
                    
        
        # Checks if player collides with asteroid
            arcade.play_sound(self.explosion, .9)  
            self.lives -= 1
            self.constructor.player.center_x = constants.SCREEN_WIDTH / 2
            self.constructor.player.center_y = constants.SCREEN_HEIGHT / 10
        
        # Checks if player collides with trophy
        if self.constructor.player.collides_with_sprite(self.constructor.trophy):
            arcade.play_sound(self.trophy, 0.5)
            self.score += 5
            self.constructor.trophy.center_x = random.randint(10, constants.SCREEN_WIDTH - 10)
            self.constructor.trophy.center_y = random.randint(10, constants.SCREEN_HEIGHT - 10)
        
        # what to do if player is dead
        if self.lives == 0:
            
            # Pauses scheduling of asteroids
            self.constructor.pause()
            # Opens game over window
            game_over = GameOverView(self, self.score)
            self.window.show_view(game_over)
        
    def on_draw(self):
        """Called whenever you need to draw your window
        """
        # Starts the render
        arcade.start_render()
        
        # Sets background image
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)
        
        # Draw all the sprites
        self.constructor.scene.draw()
        
        score_text = f"Score: {int(self.score)}"
        arcade.draw_text(score_text, 430, 760, arcade.csscolor.WHITE, 18, font_name="Kenney Future")
        
        # Sets up lives
        self.lives_list = arcade.SpriteList()
        for i in range(self.lives):
            life = Lives(constants.PATH + "/images/life.png", constants.LIVES_SCALING)
            life.center_x = constants.LIVES_POSITIONS[i]
            self.lives_list.append(life)
        
        # Draws lives
        self.lives_list.draw()
            

