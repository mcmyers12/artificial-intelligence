'''Propositional logic recursive descent parser
   Authors: Miranda Myers, Sarah Prata, Alec Jacuzzi'''

import collections
from operator import and_, or_

Token = collections.namedtuple('Token', ['name', 'value'])
RuleMatch = collections.namedtuple('RuleMatch', ['name', 'matched'])

TOKENMAP = {'&':'AND', '<=>': 'BIC', '=>': 'IMP', '|':'OR', '~': 'NEG', '(':'LPAR', ')':'RPAR'}
RULEMAP = {
    'biconditional' : ['implication BIC biconditional', 'implication'],
    'implication' : ['or IMP implication', 'or'],
    'or' : ['and OR or', 'and'],
    'and' : ['atom AND and', 'atom'],
    'atom': ['LOGIC', 'LPAR or RPAR', 'negate'],
    'negate' : ['NEG atom'],
}
FIXASSOCRULES = 'or', 'and', 'biconditional', 'implication'

def implication_function(left, right):
    '''Define implication.'''
    if (left == True) and right == False:
        return False
    else:
        return True

def biconditional_function(left, right):
    '''Define biconditional.'''
    if left == True and right == True:
        return True
    if left == False and right == False:
        return True
    else:
        return False

def not_function(term):
    '''Define not.'''
    return not term[1]

def fix_string(input_string, size):
    '''Format the string.'''
    i = 0
    fix_stream = []
    while i < (size - 1):
        current_char = input_string[i]
        if current_char == '~':
            fix_stream.append("~")

        elif current_char == '&':
            fix_stream.append("&")

        elif current_char == '|':
            fix_stream.append("|")

        elif current_char == '=':
            fix_stream.append("=>")
            i += 2

        elif current_char == '<':
            fix_stream.append("<=>")
            i += 3

        elif current_char == '(':
            fix_stream.append("(")

        elif current_char == ')':
            fix_stream.append(")")

        elif current_char == 't':
            fix_stream.append("TRUE")
            i += 4

        elif current_char == 'f':
            fix_stream.append("FALSE")
            i += 5

        elif current_char == ' ':
            i = i

        else:
            fix_stream.append("INVALID")

        i += 1

    return fix_stream

BINCALCMAP = {'&':and_, '|':or_, '<=>':biconditional_function, '=>':implication_function}

def calc_binary(term_list):
    '''Maps values to their binary calc functions.'''
    while len(term_list) > 1:
        term_list[:3] = [BINCALCMAP[term_list[1]](term_list[0], term_list[2])]
    return term_list[0]

def to_bool(term):
    '''Define bool.'''
    if term.lower() == 'true':
        return True
    if term.lower() == 'false':
        return False

CALCMAP = {
    'LOGIC': lambda x: to_bool(x),
    'atom': lambda x: x[len(x) != 1],
    'negate': lambda x: not_function(x),
    'and': calc_binary,
    'or': calc_binary,
    'implication': calc_binary,
    'biconditional': calc_binary,
}

def match(rule_name, tokens):
    '''Build the tree using recursion.'''
    if tokens and rule_name == tokens[0].name:      # Match a token?
        return tokens[0], tokens[1:]
    for expansion in RULEMAP.get(rule_name, ()):   # Match a rule?
        remaining_tokens = tokens
        matched_subrules = []
        for subrule in expansion.split():
            matched, remaining_tokens = match(subrule, remaining_tokens)
            if not matched:
                break   # no such luck. next expansion!
            matched_subrules.append(matched)
        else:
            return RuleMatch(rule_name, matched_subrules), remaining_tokens
    return None, None   # match not found

def _recurse_tree(tree, func):
    '''Descend the tree.'''
    return map(func, tree.matched) if tree.name in RULEMAP else tree[1]

def flatten_right_associativity(tree):
    '''Flatten the tree.'''
    new = _recurse_tree(tree, flatten_right_associativity)
    if tree.name in FIXASSOCRULES and len(new) == 3 and new[2].name == tree.name:
        new[-1:] = new[-1].matched
    return RuleMatch(tree.name, new)

def evaluate(tree):
    '''Evaluate the tree.'''
    solutions = _recurse_tree(tree, evaluate)
    return CALCMAP.get(tree.name, lambda x: x)(solutions)

def calc(expr):
    '''Build and evaluate the tree.'''
    if expr is None or expr == '':
        return
    #split_expr = re.findall('true|false|[%s]' % ''.join(TOKENMAP), expr, re.I)
    split_expr = fix_string(expr, len(expr))
    tokens = [Token(TOKENMAP.get(x, 'LOGIC'), x) for x in split_expr]
    tree = match('biconditional', tokens)[0]
    tree = flatten_right_associativity(tree)
    return evaluate(tree)

def main():
    '''Run the recursive descent parser on the given test file.'''
    test_parse = open("TestParse.txt", 'r')
    for line in test_parse:
        value = calc(line)
        if not line.endswith('\n'):
            print line + '\n', value
        else:
            print line, value
        print " "

if __name__ == '__main__':
    main()
