from random import choices

population = [n for n in range(6)]
peso = [0.5, 0.2, 0.1, 0.05, 0.05, 0.1]

chances = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
}

for _ in range(10000):
    chances[choices(population, peso)[0]] += 1

print(chances)

"ai.html": 0.1829
"algorithms.html": 0.1073
"c.html": 0.1298
"inference.html": 0.1271
"logic.html": 0.0276
"programming.html": 0.2319
"python.html": 0.1217
"recursion.html": 0.0717