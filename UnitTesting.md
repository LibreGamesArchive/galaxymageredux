# Introduction #

Unit tests help speed up development, allow for more confident refactoring, and provide a method for turning bug reports into debuggable code snippets.

# Unit Testing Axioms #

  * **Avoid multiple asserts in a single unit test** When only one assert statement is used in each test case, all asserts are run.
  * **Put initialization code in the setUp function** When constructor formats and standard initialization code changes mostly just the setUp function needs to be updated.
  * **Use factory methods to create partially used local objects**
  * **Everyone writes unittests** When everyone writes unittests testing is less of a burden because more tests are written and tests naturally have more diversity.
  * **Make test cases and unit tests atomic** Test cases shouldn't depend on each other, and neither should unit tests so that each may be run alone or in any order.  This makes the test cases more durable.
  * **Test early** As soon as you write a test case you can run your code. Test cases allow you to run code without needing to write graphics code or test your graphics code without the needing data structures.  It isolates the modules making every one's life easier.
  * **Test often** The more code you write tests for the more code that is protected from sloppy commits.

# Python module unittest #

One of the built-in Python testing frameworks is the unittest module.  Also known as PyUnit, it follows the same paradigm as the famous jUnit and other xUnit testing frameworks.

## Notes on using unittest ##

  * The test suites contain test case classes that derive from `unittest.TestCase`.
  * Methods that begin with `test` are automatically called by `unittest.main()` in alphabetical order.
  * The `setUp` function is called before each test method and the `tearDown` function is called after each test method.
  * Both `setUp` and `tearDown` can be overloaded.
  * You can use the TestLoader and TestRunner to run a suite and capture the output to a string.
  * **These are just the most basic and common features of unittest**

## Format of a Unit Test Class ##

```
import sys, os
sys.path.append("..")

import ability
import battle
import effect
import unit
import unittest

sys.path.append(os.path.join('..', '..', '..', 'data', 'core', 'abilities'))
import physical_attacks
import attack_spells

b = battle.Battle()

class PunchTestCase(unittest.TestCase):
    def setUp(self):
        self.s = unit.Unit("source", unit.Gender.NEUTER, b)
        self.s.statistics[unit.Statistic.PHYSICAL_ATTACK] = unit.Statistic(10)
        self.s.statistics[unit.Statistic.MAGIC_ATTACK] = unit.Statistic(10)
        self.s.abilities.append(physical_attacks.barehanded_punch)
        self.s.abilities.append(attack_spells.magic_zot)
        self.t = unit.Unit("target", unit.Gender.NEUTER, b)
        self.t.statistics[unit.Statistic.MAX_HP] = unit.Statistic(1000)
        self.t.current_hp = \
            self.t.statistics[unit.Statistic.MAX_HP].get_effective_value()
    def testPunchAttack(self):
        MAX_HP_MINUS_BAREHANDED_PUNCH = 990
        self.s.use_ability(physical_attacks.barehanded_punch, [self.t])
        self.assertEqual(self.t.current_hp, MAX_HP_MINUS_BAREHANDED_PUNCH)
    def testMagicZot(self):
        MAX_HP_MINUS_MAGIC_ZOT = 950
        self.s.use_ability(attack_spells.magic_zot, [self.t])
        self.assertEqual(self.t.current_hp, MAX_HP_MINUS_MAGIC_ZOT)
        
if __name__ == '__main__':
    unittest.main()
```

# Final Comments #

Not everyone likes test driven development.  Sometimes it's easier to just code until it works.  But whether you are doing test driven development or not doesn't matter, unittests are always good.  There is another testing framework built-in to python called doctest where the tests are coded in comments inside the code.  This is more pythonic but creates the war between full testing and readable code.


---

[Write Maintainable Unit Tests That Will Save You Time And Tears by Roy Osherove](http://msdn.microsoft.com/en-us/magazine/cc163665.aspx)

[Python unit testing part 1: the unittest module by Grig Gheorghiu](http://agiletesting.blogspot.com/2005/01/python-unit-testing-part-1-unittest.html)

[Python v2.6.1 Documentation of unnittest -- Unit testing framework](http://docs.python.org/library/unittest.html)

[Comment on unittest vs doctest](http://stackoverflow.com/questions/361675/python-doctest-vs-unittest)