
import core

def main():
    fx1 = core.Effect(affect={"cur_hitpoints":-2}, duration=1)
    ability_damage = core.Ability([fx1], cost={"cur_magicpoints":-2},
                                  target="Enemies", range=5, shape="Target")

    ut = core.UnitType()
    u1 = core.Unit(ut, abilities=[ability_damage])
    u2 = core.Unit(ut, 1, abilities=[ability_damage])

    print u1.cur_hitpoints, u1.cur_magicpoints
    print u2.cur_hitpoints, u2.cur_magicpoints
    print

    u1.use_ability(ability_damage, [u1, u2])
    u2.update()

    print u1.cur_hitpoints, u1.cur_magicpoints
    print u2.cur_hitpoints, u2.cur_magicpoints
    print

    u2.update()
    print u1.cur_hitpoints, u1.cur_magicpoints
    print u2.cur_hitpoints, u2.cur_magicpoints
    print

    u2.update()
    print u1.cur_hitpoints, u1.cur_magicpoints
    print u2.cur_hitpoints, u2.cur_magicpoints
main()
