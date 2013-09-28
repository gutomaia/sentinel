import ast

from cerebro import tag


class Mutator(ast.NodeTransformer):

    def __init__(self, gene_mutation):
        self.level = 0
        self.function_def = None
        if gene_mutation:
            self.gene = gene_mutation.split('|')[0]
            self.mutation = gene_mutation.split('|')[1]
        else:
            self.gene = False
            self.mutation = False
        self.path = ''

    def visit_FunctionDef(self, node):
        self.level += 1
        self.path += 'def <%s>' % node.name
        self.generic_visit(node)
        self.level -= 1
        return node

    def visit_If(self, node):
        self.level += 1
        self.generic_visit(node)
        gene = tag(node, self.path, self.level)
        if gene == self.gene:
            condition = ast.Name(self.mutation, ast.Load())
            return ast.If(condition, node.body, node.orelse)
        self.level -= 1
        return node
