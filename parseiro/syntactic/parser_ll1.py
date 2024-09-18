from parseiro.symbols import Epsilon, EndMarker

'''
# Initial Grammar
E -> E + T
E -> T
T -> T * F
T -> F
F -> (E)
F -> n

# LL1 Converted Grammar
E  -> T E1
E1 -> + T E1 | &
T  -> F T1
T1 -> * F T1 | &
F  -> n
F  -> (E)
'''


class ParserLL1:
    def analyze(self, string: str):
        table = {
            ("E", "n"): ("T", "E1"),
            ("E", "("): ("T", "E1"),
            
            ("E1", "+"): ("+", "T", "E1"),
            ("E1", ")"): (Epsilon(),),
            ("E1", EndMarker()): (Epsilon(),),

            ("T", "n"): ("F", "T1"),
            ("T", "("): ("F", "T1"),
            
            ("T1", "+"): (Epsilon(),),
            ("T1", "*"): ("*", "F", "T1"),
            ("T1", ")"): (Epsilon(),),
            ("T1", EndMarker()): (Epsilon(),),

            ("F", "n"): ("n",),
            ("F", "("): ("(", "E", ")"),
        }

        index = 0
        tokens = list("n+n*n")
        tokens.append(EndMarker())

        stack = [Epsilon(), "E"]

        while len(stack) > 1:
            print(stack)
            token = tokens[index]
            node = stack.pop()
            print(node, token)
            print()

            if node == Epsilon():
                continue

            if node == EndMarker():
                print("Syntactical error")
                break

            # Terminal char
            if node in "n+*()":
                index += 1
                continue

            if (node, token) not in table:
                print("Syntactical error")
                break
            
            production = table[node, token]
            stack.extend(reversed(production))

        print(stack)

p = ParserLL1()
p.analyze("")