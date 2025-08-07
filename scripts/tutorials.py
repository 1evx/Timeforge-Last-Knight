import pygame
from scripts import Settings

class Tutorial:
    def __init__(self, screen):
        self.screen = screen
        self.current_tutorial = 0
        self.tutorials = [
            {
                "name": "Movement",
                "description": "Use A and D keys to move left and right",
                "keys_to_check": ["A", "D"],
                "completed": False,
                "progress": 0,
                "required_progress": 2
            },
            {
                "name": "Jumping",
                "description": "Press W or SPACE to jump",
                "keys_to_check": ["W", "SPACE"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Crouching",
                "description": "Press S to crouch",
                "keys_to_check": ["S"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Sliding",
                "description": "Press S + D or S + A to slide",
                "keys_to_check": ["S+D", "S+A"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Basic Attack",
                "description": "Press LEFT CLICK to attack",
                "keys_to_check": ["LEFT_CLICK"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Combo Attack",
                "description": "Press LEFT CLICK twice quickly for a combo",
                "keys_to_check": ["COMBO_ATTACK"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Dash Attack",
                "description": "Press RIGHT CLICK for a dash attack",
                "keys_to_check": ["RIGHT_CLICK"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            },
            {
                "name": "Jump Attack",
                "description": "Jump and press RIGHT CLICK in the air for a jump attack",
                "keys_to_check": ["JUMP_ATTACK"],
                "completed": False,
                "progress": 0,
                "required_progress": 1
            }
        ]
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tutorial_complete = False
        self.tutorial_active = True
        
        # Track previous states for detection
        self.prev_keys = {}
        self.prev_mouse_buttons = [False, False, False]
        self.prev_player_state = "idle"
        self.prev_attack_stage = 0
        self.prev_is_attacking = False
        self.prev_is_dashing = False
        self.prev_is_sliding = False
        self.prev_on_ground = True
        self.prev_velocity_y = 0
        
        # Timing for combo detection
        self.last_attack_time = 0
        self.combo_window = 500  # ms to press again for combo

    def update(self, keys, mouse_buttons, player):
        """Update tutorial progress based on player input and state"""
        if not self.tutorial_active or self.tutorial_complete:
            return
            
        current_tutorial = self.tutorials[self.current_tutorial]
        
        # Update previous states
        self.prev_keys = list(keys)
        self.prev_mouse_buttons = list(mouse_buttons)
        self.prev_player_state = player.state
        self.prev_attack_stage = player.attack_stage
        self.prev_is_attacking = player.is_attacking
        self.prev_is_dashing = player.is_dashing
        self.prev_is_sliding = player.is_sliding
        self.prev_on_ground = player.on_ground
        self.prev_velocity_y = player.velocity_y
        
        # Check tutorial completion based on current tutorial
        if current_tutorial["name"] == "Movement":
            self._check_movement_tutorial(keys)
        elif current_tutorial["name"] == "Jumping":
            self._check_jumping_tutorial(keys, player)
        elif current_tutorial["name"] == "Crouching":
            self._check_crouching_tutorial(keys, player)
        elif current_tutorial["name"] == "Sliding":
            self._check_sliding_tutorial(keys, player)
        elif current_tutorial["name"] == "Basic Attack":
            self._check_basic_attack_tutorial(mouse_buttons, player)
        elif current_tutorial["name"] == "Combo Attack":
            self._check_combo_attack_tutorial(mouse_buttons, player)
        elif current_tutorial["name"] == "Dash Attack":
            self._check_dash_attack_tutorial(mouse_buttons, player)
        elif current_tutorial["name"] == "Jump Attack":
            self._check_jump_attack_tutorial(keys, mouse_buttons, player)
        
        # Check if current tutorial is complete
        if current_tutorial["progress"] >= current_tutorial["required_progress"]:
            current_tutorial["completed"] = True
            self._next_tutorial()

    def _check_movement_tutorial(self, keys):
        """Check if player has moved left and right"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if keys[pygame.K_a] and tutorial["progress"] == 0:
            tutorial["progress"] = 1
        elif keys[pygame.K_d] and tutorial["progress"] == 1:
            tutorial["progress"] = 2

    def _check_jumping_tutorial(self, keys, player):
        """Check if player has jumped"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and player.state == "jump" and player.velocity_y < 0:
            tutorial["progress"] = 1

    def _check_crouching_tutorial(self, keys, player):
        """Check if player has crouched"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if keys[pygame.K_s] and player.state == "crouch" and not player.is_sliding:
            tutorial["progress"] = 1

    def _check_sliding_tutorial(self, keys, player):
        """Check if player has slid"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if player.is_sliding and (keys[pygame.K_s] and (keys[pygame.K_d] or keys[pygame.K_a])):
            tutorial["progress"] = 1

    def _check_basic_attack_tutorial(self, mouse_buttons, player):
        """Check if player has performed a basic attack"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if mouse_buttons[0] and player.is_attacking and player.attack_stage == 1:
            tutorial["progress"] = 1

    def _check_combo_attack_tutorial(self, mouse_buttons, player):
        """Check if player has performed a combo attack"""
        tutorial = self.tutorials[self.current_tutorial]
        # Pass the tutorial if the player is in combo attack state
        if player.state == "attack2" or player.attack_stage == 2:
            tutorial["progress"] = 1

    def _check_dash_attack_tutorial(self, mouse_buttons, player):
        """Check if player has performed a dash attack"""
        tutorial = self.tutorials[self.current_tutorial]
        
        if mouse_buttons[2] and player.is_dashing and player.is_attacking and player.attack_stage == 3:
            tutorial["progress"] = 1

    def _check_jump_attack_tutorial(self, keys, mouse_buttons, player):
        """Check if player has performed a jump dash attack (jump attack)"""
        tutorial = self.tutorials[self.current_tutorial]
        if (player.state == "dash_attack" and player.is_dashing and player.is_attacking and not player.on_ground):
            tutorial["progress"] = 1

    def _next_tutorial(self):
        """Move to the next tutorial"""
        self.current_tutorial += 1
        
        if self.current_tutorial >= len(self.tutorials):
            self.tutorial_complete = True
            self.tutorial_active = False

    def draw(self):
        """Draw the current tutorial information"""
        if not self.tutorial_active or self.tutorial_complete:
            return
            
        current_tutorial = self.tutorials[self.current_tutorial]
        
        # Create tutorial box
        box_width = 600
        box_height = 150
        box_x = (Settings.SCREEN_WIDTH - box_width) // 2
        box_y = (Settings.SCREEN_HEIGHT - box_height) // 2
        
        # Draw background box
        bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
        
        # Draw tutorial title
        title_text = self.font.render(f"Tutorial {self.current_tutorial + 1}/{len(self.tutorials)}: {current_tutorial['name']}", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=box_y + 20)
        self.screen.blit(title_text, title_rect)
        
        # Draw tutorial description
        desc_text = self.small_font.render(current_tutorial['description'], True, (255, 255, 255))
        desc_rect = desc_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=box_y + 60)
        self.screen.blit(desc_text, desc_rect)
        
        # Draw progress bar
        progress_width = 400
        progress_height = 20
        progress_x = (Settings.SCREEN_WIDTH - progress_width) // 2
        progress_y = box_y + 100
        
        # Background bar
        bg_progress = pygame.Rect(progress_x, progress_y, progress_width, progress_height)
        pygame.draw.rect(self.screen, (60, 60, 60), bg_progress)
        
        # Progress bar
        progress_ratio = current_tutorial['progress'] / current_tutorial['required_progress']
        progress_fill = pygame.Rect(progress_x, progress_y, int(progress_width * progress_ratio), progress_height)
        pygame.draw.rect(self.screen, (0, 255, 0), progress_fill)
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), bg_progress, 2)
        
        # Progress text
        progress_text = self.small_font.render(f"{current_tutorial['progress']}/{current_tutorial['required_progress']}", True, (255, 255, 255))
        progress_text_rect = progress_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=progress_y + 25)
        self.screen.blit(progress_text, progress_text_rect)

    def draw_completion_screen(self):
        """Draw the tutorial completion screen"""
        if not self.tutorial_complete:
            return
            
        # Create completion box
        box_width = 500
        box_height = 200
        box_x = (Settings.SCREEN_WIDTH - box_width) // 2
        box_y = (Settings.SCREEN_HEIGHT - box_height) // 2
        
        # Draw background box
        bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), bg_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), bg_rect, 3)
        
        # Draw completion text
        title_text = self.font.render("Tutorial Complete!", True, (0, 255, 0))
        title_rect = title_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=box_y + 40)
        self.screen.blit(title_text, title_rect)
        
        desc_text = self.small_font.render("You have learned all the basic controls!", True, (255, 255, 255))
        desc_rect = desc_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=box_y + 80)
        self.screen.blit(desc_text, desc_rect)
        
        continue_text = self.small_font.render("Press any key to continue...", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(centerx=Settings.SCREEN_WIDTH // 2, y=box_y + 120)
        self.screen.blit(continue_text, continue_rect)

    def handle_completion_input(self, event):
        """Handle input for tutorial completion screen"""
        if self.tutorial_complete and event.type == pygame.KEYDOWN:
            return True  # Signal to continue to next level
        return False

    def is_tutorial_complete(self):
        """Check if all tutorials are complete"""
        return self.tutorial_complete

    def get_tutorial_progress(self):
        """Get current tutorial progress"""
        completed = sum(1 for tutorial in self.tutorials if tutorial["completed"])
        return completed, len(self.tutorials)
    
    def reset_tutorial(self):
        """Reset current tutorial progress"""
        if self.current_tutorial < len(self.tutorials):
            self.tutorials[self.current_tutorial]["progress"] = 0
            self.tutorials[self.current_tutorial]["completed"] = False 