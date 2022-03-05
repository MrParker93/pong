import pyxel  # Please refer to the following link for the documentation: https://github.com/kitao/pyxel
import random


# Handles the ball setup and logic
class Ball:
    def __init__(self) -> None:  # '->' The return type to expect from a function
        self.radius = 2  
        self.starting_position()

    # Draws the ball to the screen
    def draw(self) -> None:
        pyxel.circ(x=self.x_position, y=self.y_position, r=self.radius, col=pyxel.COLOR_WHITE)

    # The default settings for the ball
    def starting_position(self) -> None:
        self.x_position = pyxel.width * 0.5
        self.y_position = pyxel.height * 0.5
        self.x_velocity = random.choice([-1, 1])
        self.y_velocity = random.choice([-1, 1])

    # Handles the ball movement 
    def move(self) -> None:
        
        # Adds velocity to the ball position to make the ball move
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity

        # Checks if the ball collides with the top or bottom wall
        # and reverses the velocity (bounces off the wall)
        if self.check_wall_collision(y_position=self.y_position):
            pyxel.play(2, 0)
            self.y_velocity *= -1  # Multiplying by '-1' changes the value from negative to positive an vice versa changing the direction

    def check_wall_collision(self, y_position: int) -> bool:
        if self.radius <= y_position < pyxel.height - self.radius:
            return False
        return True

    # Checks if the ball passes the left or right wall
    def check_if_scored(self, x_position: int) -> bool:
        if 0 < x_position < pyxel.width:
            return False
        return True

    # Checks if the ball collides with player one bat
    def check_player_one_collision(
        self,
        x_position: int,
        y_position: int,
        bat_position_x: int,
        bat_position_y: int,
    ) -> bool:
        if (
            x_position <= bat_position_x 
            and bat_position_y <= y_position <= bat_position_y + 40
        ):
            return True
        return False

    # Checks if the ball collides with player two bat
    def check_player_two_collision(
        self,
        x_position: int,
        y_position: int,
        bat_position_x: int,
        bat_position_y: int,
    ) -> bool:
        if (
            x_position >= bat_position_x
            and bat_position_y <= y_position <= bat_position_y + 40
        ):
            return True
        return False


# Handles the bat setup and logic
class Bat:
    def __init__(self, x: int, y: int) -> None:
        self.height = 20
        self.width = 3
        self.x = x
        self.y = y

    # Draws the bat to the screen
    def draw(self) -> None:
        pyxel.rect(x=self.x, y=self.y, w=self.width, h=self.height, col=pyxel.COLOR_WHITE)

    # Handles the bat movement
    def move(self, key_up: int, key_down: int) -> None:

        # Checks if the button set to key up is pressed and moves the bat up
        if pyxel.btn(key=key_up):
            self.y -= 3
            if not self.valid_position(y=self.y):
                self.y += 3

        # Checks if the button set to key down is pressed and moves the bat down
        if pyxel.btn(key=key_down):
            self.y += 3
            if not self.valid_position(y=self.y):
                self.y -= 3

    # Ensures the bat remains within the game window
    def valid_position(self, y: int) -> bool:
        return 0 < y < pyxel.height - self.height


# Game setup
class Pong:
    def __init__(self) -> None:

        # Setup for the pyxel application
        pyxel.init(width=256, height=int(256 * 0.75), title="Pong", fps=60)

        # Loads the sounds created using 'pyxel edit YOUR_FILENAME.pyxres' in the terminal
        pyxel.load('sounds.pyxres', sound=True)
        self.setup()
        pyxel.run(self.update, self.draw)

    # Initial setup for the game
    def setup(self) -> None:
        self.game_state = "running"
        self.player_one_score = 0
        self.player_two_score = 0
        self.player_one_bat = Bat(x=(pyxel.width * 0.05) - 5, y=(pyxel.height * 0.5) - 20)
        self.player_two_bat = Bat(x=pyxel.width * 0.95, y=(pyxel.height * 0.5) - 20)
        self.ball = Ball()

    # Checks for changes and updates the game every frame
    def update(self) -> None:

        # Quit the application if Q is pressed
        if pyxel.btn(key=pyxel.KEY_Q):
            pyxel.quit()
        
        # Reset the application if R is pressed
        if pyxel.btn(key=pyxel.KEY_R):
            self.setup()

        # Pause the game
        if pyxel.btnr(key=pyxel.KEY_P):
            if self.game_state == "running":
                self.game_state = "paused"
            else:
                self.game_state = "running"

        # Ensures the game state is running (and not paused) to look for updates
        if self.game_state == "running":
            # Set the inputs for the movement of the bat and calls the function
            self.player_one_bat.move(key_up=pyxel.KEY_W, key_down=pyxel.KEY_S)
            self.player_two_bat.move(key_up=pyxel.KEY_UP, key_down=pyxel.KEY_DOWN)

            # Start the movement of the ball
            self.ball.move()

            if self.ball.check_player_one_collision(
                x_position=self.ball.x_position,
                y_position=self.ball.y_position,
                bat_position_x=(self.player_one_bat.x + self.player_one_bat.width),
                bat_position_y=self.player_one_bat.y,
            ):
                # Reverses the velocity of the ball and increases the speed by .1
                # After colliding with the bat
                pyxel.play(1, 1)
                self.ball.x_velocity *= -1
                self.ball.x_velocity *= 1.1
                self.ball.y_velocity *= 1.1

            elif self.ball.check_player_two_collision(
                x_position=self.ball.x_position,
                y_position=self.ball.y_position,
                bat_position_x=(self.player_two_bat.x - self.player_two_bat.width),
                bat_position_y=self.player_two_bat.y,
            ):
                pyxel.play(1, 1)
                self.ball.x_velocity *= -1
                self.ball.x_velocity *= 1.1
                self.ball.y_velocity *= 1.1
        
            if self.ball.check_if_scored(x_position=self.ball.x_position):
                # If player one scores
                if self.ball.x_position > pyxel.width * 0.5:
                    pyxel.play(0, 2)
                    
                    # Add one point to the score
                    self.player_one_score += 1

                    # Set the ball to the default position
                    self.ball.starting_position()
                
                # If player two scores
                else:
                    pyxel.play(0, 2)
                    self.player_two_score += 1
                    self.ball.starting_position()

    # Draws the game
    def draw(self) -> None:
        pyxel.cls(pyxel.COLOR_BLACK)
        self.display_score()
        self.display_pause()
        self.player_one_bat.draw()
        self.player_two_bat.draw()
        self.ball.draw()

    # Displays the current score
    def display_score(self) -> None:
        pyxel.text(
            x=pyxel.width * 0.5 - 10,
            y=pyxel.height * 0.05,
            s=str(self.player_one_score),
            col=pyxel.COLOR_WHITE,
        )
        pyxel.text(
            x=pyxel.width * 0.5 + 10,
            y=pyxel.height * 0.05,
            s=str(self.player_two_score),
            col=pyxel.COLOR_WHITE,
        )

    # Displays 'PAUSE'
    def display_pause(self) -> None:
        if self.game_state == "paused":
            pyxel.text(
                x=pyxel.width * 0.5 - 10,
                y=pyxel.height * 0.5,
                s="PAUSED",
                col=pyxel.COLOR_WHITE
            )

if __name__ == "__main__":
    Pong()


# Ways to make the game more advanced

# TODO: Add a title screen
# TODO: Add game physics to the bat and ball (I recommend using the PyMunk module)
# TODO: Add difficulty settings (think of how you can change specific values to effect this)