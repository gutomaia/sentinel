import ast
import hashlib

class Cerebro(ast.NodeVisitor):
    '''Cerebro is a device to help identify humans and mutants'''

    def __init__(self):
        self.level = 0
        self.genes = []
        self.path = ''


    def visit_FunctionDef(self, node):
        self.level += 1
        self.path = 'def <%s>' % node.name
        self.generic_visit(node)
        #todo remove with substring
        self.level -= 1


    def visit_If(self, node):
        self.level += 1
        self.dna(node, self.path, self.level)
        self.generic_visit(node)
        self.level -= 1

    def dna(self, node, path, level):
        if isinstance(node, ast.If):
            mutations = ['True', 'False']
        for m in mutations:
            description = "'if' clause at line %d, column %d at %s" % (
                node.lineno, node.col_offset, path
            )
            self.genes.append('%s|%s|%s' % (tag(node, path, level), m, description))

def tag(node, path, level):
    if isinstance(node, ast.If):
        test = ast.dump(node.test, True)
        s = 'If: %s, c(%s), ident_level %d' % (path, test, level)
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()
