from lark import Lark, Transformer, Tree

# Load your grammar from the file
with open('mygrammar.lark') as file:
    grammar = file.read()



script = """int t = preach("hello world");"""
# Create a Lark parser with your grammar
parser = Lark(grammar, start='start', parser='earley')
parsed_tree = parser.parse(script)
print(parsed_tree.pretty())


