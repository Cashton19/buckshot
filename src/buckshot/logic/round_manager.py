class RoundManager():
    """Create a New Round After each reload"""
    def __init__(self):
        self.current_round = 1
        
    def next_round(self, turnmanager, shotgun):
        if not shotgun.is_empty():
            return
        else:
            self.current_round += 1
            turnmanager.reset()
            shotgun.load_shells(self.current_round)
            