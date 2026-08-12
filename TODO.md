# Buckshot Implementation TODO

This list outlines the necessary steps and file structure to implement the game logic.

## 1. Core Logic Components (New Files)
- [ ] **`src/buckshot/logic/shotgun.py`**:
    - [ ] Create `Shotgun` class.
    - [ ] Logic for random shell generation (live/blank).
    - [ ] `shuffle()` method.
    - [ ] `fire()` method to return the next shell and update counts.
- [ ] **`src/buckshot/logic/turn_manager.py`**:
    - [ ] Implement a State Machine for game phases: `SETUP`, `PLAYER_TURN`, `ACTION_RESOLUTION`, `ROUND_END`, `GAME_OVER`.
    - [ ] Handle turn transitions and "skip turn" (Handcuffs) logic.
- [ ] **`src/buckshot/logic/items.py`**:
    - [ ] Define `Item` base class and subclasses for: `Magnifying Glass`, `Cigarette`, `Handcuffs`, `Saw`.
    - [ ] Logic for applying effects to the game state.

## 2. Refactor Existing Components
- [ ] **`src/buckshot/scenes/player.py` & `enemy.py`**:
    - [ ] Add `health` (HP) and `max_health` attributes.
    - [ ] Add `inventory` (list of Items).
    - [ ] Add methods for `take_damage()`, `heal()`, `use_item()`.
- [ ] **`src/buckshot/scenes/game_environment.py`**:
    - [ ] Integrate `Shotgun` and `TurnManager`.
    - [ ] Handle user input for shooting (Self/Opponent) and Item selection.
    - [ ] Implement animations/delays for "Action Resolution" phase.
- [ ] **`src/buckshot/__main__.py`**:
    - [ ] Fix the crash-prone loop.
    - [ ] Create a persistent `Game` object that manages scene transitions without re-initializing/quitting Pygame repeatedly.

## 3. Game Mechanics Implementation
- [ ] **Shotgun State Management**:
    - [ ] Track total, live, and blank shells.
    - [ ] Hidden shell sequence logic.
- [ ] **Turn Sequence**:
    - [ ] Player chooses action -> Resolve -> Update state -> Check for end of round/game.
- [ ] **Shooting Logic**:
    - [ ] Shooting Opponent: Live = Damage + Turn Pass; Blank = No Damage + Turn Pass.
    - [ ] Shooting Self: Live = Damage + Turn Pass; Blank = No Damage + **Keep Turn**.
- [ ] **Item Effects**:
    - [ ] Magnifying Glass: Peek at next shell.
    - [ ] Cigarette: Restore 1 HP.
    - [ ] Handcuffs: Skip opponent's next turn.
    - [ ] Saw: Double damage for the next live shell.

## 4. Win/Loss & Rounds
- [ ] **Round System**: Reset shotgun when empty, regenerate shells.
- [ ] **Win Condition**: Check HP after every damage event.
- [ ] **Game Over Screen**: Transition to a screen showing the winner and options to Play Again or Menu.
- [] Create shotgun.py 
- [] add health, max health to player.py
- [] create turn_manager.py
- []
- []
- []
- []
