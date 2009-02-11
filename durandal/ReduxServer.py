import sys
sys.path.insert(0, "src")

import net
s = net.Server()
s.start(44444)
