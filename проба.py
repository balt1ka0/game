"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "OH, PIGEON!"

JUMP_MAX_HEIGHT = 100
PLAYER_JUMP_SPEED = 1

PLAYER_X_SPEED = 6
PLAYER_Y_SPEED = 6

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.00001

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.6
TILE_SCALING = 0.4

class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.player_list = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.LIGHT_STEEL_BLUE)

        # A Camera that can be used for scrolling the screen
        self.camera = None

        self.player_jump = False
        self.player_start = None
        self.camera_max = 0

        self.key_up_pressed = False
        self.key_right_pressed = False
        self.key_left_pressed = False

    def setup(self):
        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/голубь.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 160
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 10000, 64):
            wall = arcade.Sprite("images/земля.png", scale=0.6 )
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate1_list = [[1300, 150], [2000, 150], [2900, 150], [3700, 150], [4900, 150]]

        for coordinate in coordinate1_list:
            # Add a crate on the ground
            wall = arcade.Sprite(
                "images/помойка.png", TILE_SCALING 
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        coordinate2_list = [[700, 300], [1200, 800], [2000, 700], [2400, 400], [2500, 480], [3000, 590]]

        for coordinate in coordinate2_list:
            wall = arcade.Sprite(
                "images/пузыри.png", TILE_SCALING 
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.wall_list
        )

    def on_draw(self):
        self.clear()
        # Code to draw the screen goes here

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()

        # Activate our Camera
        self.camera.use()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_up_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.key_up_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right_pressed = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def player_movement(self):
        if self.key_left_pressed:
            self.player_sprite.center_x -= PLAYER_X_SPEED
        if self.key_right_pressed:
            self.player_sprite.center_x += PLAYER_X_SPEED

        if self.key_up_pressed:
            self.player_sprite.center_y += PLAYER_Y_SPEED
        
        if not self.key_up_pressed:
            self.player_sprite.center_y -= PLAYER_Y_SPEED
            if self.player_sprite.center_y < 160:
                self.player_sprite.center_y = 160

    def on_update(self, delta_time):
        """Movement and game logic"""

        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

        self.player_movement()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
