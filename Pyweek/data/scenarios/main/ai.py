
class AI(BaseAI):
    def initialize(self):
        pass

    def update(self):
        enemy_list = self.get_enemy_units()
        team_list = self.get_my_units()
        # I think we need an AIHandler
        # This would allow each "ai" class in the scenarios.ai.py to be customized by team
        for u in team_list:
            if u.dead:
                continue
            enemy_list.sort(key=lambda e: self.distance(e.pos,u.pos))
            # AI always moves to the closest enemy.
            while u.cur_ap > 0:
                for a in u.actions:
                    if a.name == 'Move':
                        continue # First try an attacking ability
                    for e in enemy_list:
                        if a.test_acceptable(e.pos):
                            self.do_action(u, a, e.pos)

                # Now we make first attempt at moving.
                if u.cur_ap < 1:
                    break
                
                for a in u.actions:
                    if a.name == 'Move':
                        #if enemy_list and len(enemy_list:
                        p = a.get_path(u.pos, enemy_list[0].pos, a._get_blocked_tiles()[0])
                        # Just move once, because there may be a closer enemy or
                        # an enemy in range if we move.
                        self.do_action(u, a, p[1])
                        break

        self.end_my_turn()   

store.ai = AI
