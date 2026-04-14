from common.db import getAttacks

attacks = getAttacks()

for row in attacks:
    print(dict(row))