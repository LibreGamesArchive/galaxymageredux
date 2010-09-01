
class AI(BaseAI):
    def initialize(self):
        pass

    def get_target(self, unit, enemy_list):
        ''' 'goodguys' target jail cell (14,16), then target map exit (0,0)
            'badguys' target closest 'goodguy', and ignore the prisoner until
            he is free.
        '''
        goal = None
        if self.team == 'goodguys':
            if self.scenario.mod.prisoner_free:
                goal = (0,0)
            else:
                goal = (16,14)
        elif self.team == 'badguys':
            for i in enemy_list:
                if i.type == 'prisoner' and not self.scenario.mod.prisoner_free:
                    continue
                if i.dead:
                    continue
                goal = i.pos
                break
        else:
            print('ai.py: team not in scenario')
        return goal 

    def update(self):
        enemy_list = self.get_enemy_units()
        team_list = self.get_my_units()
        if not (enemy_list or team_list):
            self.end_my_turn()
        for u in team_list:
            if u.dead:
                continue
            enemy_list.sort(key=lambda e: self.distance(e.pos,u.pos))
            # AI always moves to the closest enemy.
            while u.cur_ap > 0:
                target = self.get_target(u, enemy_list)
                if u.name == 'Guard':
                    if self.distance(target, u.pos) > 4:
                        break
                for a in u.actions:
                    if a.name == 'Move':
                        continue # First try an attacking ability
                    for e in enemy_list:
                        if a.test_acceptable(e.pos):
                            self.do_action(u, a, e.pos)

                # Now we make first attempt at moving.
                if u.cur_ap < 1:
                    break
                
                #Refresh target, incase we killed some one.
                target = self.get_target(u, enemy_list)
                if not target:
                    break
                for a in u.actions:
                    if a.name == 'Move':
                        bt,pt = a._get_blocked_tiles()
                        p = a.get_path(u.pos, target, bt+pt)
                        tar = None
                        if p:
                            for i in p:
                                if a.test_acceptable(i):
                                    tar = i
                                    break
                        if tar:
                            self.do_action(u, a, i)
                        else:
                            u.cur_ap = 0
                        break
        self.end_my_turn() 

store.ai = AI
