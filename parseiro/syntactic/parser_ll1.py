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
            ("E1", ")"): ("&",),
            ("E1", "$"): ("&",),

            ("T", "n"): ("F", "T1"),
            ("T", "("): ("F", "T1"),
            
            ("T1", "+"): ("&",),
            ("T1", "*"): ("*", "F", "T1"),
            ("T1", ")"): ("&",),
            ("T1", "$"): ("&",),

            ("F", "n"): ("n",),
            ("F", "("): ("(", "E", ")"),
        }

        index = 0
        tokens = "n+n*n$"

        stack = ["$", "E"]

        while len(stack) > 1:
            print(stack)
            token = tokens[index]
            node = stack.pop()
            print(node, token)
            print()

            # & is a epsilon transition
            if node == "&":
                continue

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