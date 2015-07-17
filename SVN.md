# Guidelines #

## Think twice before committing ##

Committing something to svn has serious consequences. All other developers will get your changes once they are in svn, and if they break something, they will break it for everybody.

## Double check what you commit ##

Do a svn update and a svn diff before committing. Take messages from svn about conflicts, unknown files, etc. seriously. svn diff will tell you exactly what you will be committing. Check if that's really what you intended to commit.

## Always add descriptive log messages ##

Log messages should be understandable to someone who sees only the log. They shouldn't depend on information outside the context of the commit. It is important to communicate exactly what the important changes are so that everyone else can easily understand.

## Take responsibility for your commits ##

If your commit breaks something or has side effects on other code, take the responsibility to fix or help fix the problems.

## Consult PEP 8 ##
Before you commit, please be sure that your code follows the guidelines laid out in [PEP 8](http://www.python.org/dev/peps/pep-0008/).  Making your code as clean and readable as possible goes a long way when 15 other people will need to understand it.

## Use issue tracking id numbers ##

If you fix bugs reported on the issue tracking system, add the issue id to the log message. In order to keep the issue tracking system in sync with svn, you should reference the issue report in your commits, and close the fixed bugs in the issue tracking system.

## Make "atomic" commits ##

svn has the ability to commit more than one file at a time. Therefore, please commit all related changes in multiple files, even if they span over multiple directories at the same time in the same commit. This way, you ensure that svn stays in a working state before and after the commit.