
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
                if self.distance(u.pos, enemy_list[0].pos) < 2:
                    print("Attack not designed or implemented")
                    break
                else:
                    t = u.actions[0].get_select()
                    if len(t):
                        t.sort(key=lambda v: self.distance(enemy_list[0].pos,v))
                        self.do_action(u, u.actions[0], t[0])
                    else:
                        break
        self.end_my_turn()   

store.ai = AI
