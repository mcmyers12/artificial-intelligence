import tokenize
import cStringIO


# This uses the above libraries to build a Lisp structure based on atoms. 
    # It is adapted from [simple iterator parser](http://effbot.org/zone/simple-iterator-parser.htm). The first function is the `atom` function.
def atom( next, token):
    if token[ 1] == '(':
        out = []
        token = next()
        while token[ 1] != ')':
            out.append( atom( next, token))
            token = next()
            if token[ 1] == ' ':
                token = next()
        return out
    elif token[ 1] == '?':
        token = next()
        return "?" + token[ 1]
    else:
        return token[ 1]


# The next function is the actual `parse` function:
def parse( exp):
    src = cStringIO.StringIO( exp).readline
    tokens = tokenize.generate_tokens( src)
    return atom( tokens.next, tokens.next())


def is_variable( exp):
    return isinstance( exp, str) and exp[ 0] == "?"


# The second tests to see if an expression is a constant:
def is_constant( exp):
    return isinstance( exp, str) and not is_variable( exp)


def extract_dictionaries(tuple_input, dictionaries):
    for item in tuple_input:
        if type(item) == dict:
            dictionaries.update(item)
        elif type(item) == tuple:
            extract_dictionaries(item, dictionaries)
        
    return dictionaries


def composition_of(result1, result2):
    composed_results = {}
    if type(result1) == tuple:
        dictionaries = extract_dictionaries(result1, {})
        composed_results.update(dictionaries)
    elif type(result1) == dict:
        composed_results.update(result1)
          
    if type(result2) == tuple:
        dictionaries = extract_dictionaries(result2, {})
        composed_results.update(dictionaries)
    elif type(result2) == dict:
        composed_results.update(result2)
        
    return composed_results
        

def apply(result1, list_expression1, list_expression2):
    for variable in result1:
        if (variable in list_expression1):
            replace_index = list_expression1.index(variable)
            list_expression1[replace_index] = result1[variable]
        
        if (variable in list_expression2):
            replace_index = list_expression2.index(variable)
            list_expression2[replace_index] = result1[variable]


def get_first_element(list_expression):
    if list_expression and type(list_expression) == list:
        return list_expression.pop(0)
    else: 
        return list_expression
    
    
#unification can return None (if unification completely fails), 
    #{} (the empty substitution list) 
    #or a substitution list that has variables as keys and substituted values as values, like {"?x": "Fred"}.
def unification(list_expression1, list_expression2):
    if (is_constant(list_expression1) and is_constant(list_expression2)) or (list_expression1 == [] and list_expression2 == []):
        if list_expression1 == list_expression2:
            return {}
        else:
            return None
    
    if is_variable(list_expression1):
        if list_expression1 in list_expression2:
            return None
        else:
            return { list_expression1 : list_expression2 }
            
    if is_variable(list_expression2):
        if list_expression2 in list_expression1:
            return None
        else:
            return { list_expression2 : list_expression1 }
    
    first1 = get_first_element(list_expression1)
    first2 = get_first_element(list_expression2)
        
    result1 = unification(first1, first2)
    if result1 == None:
        return None
        
    apply(result1, list_expression1, list_expression2)
    
    result2 = unification(list_expression1, list_expression2)
    if result2 == None:
        return None

    return composition_of(result1, result2)


def unify( s_expression1, s_expression2):
    return unification( parse( s_expression1), parse( s_expression2))



print
print unify("Fred", "Barney")
print
print unify("Pebbles", "Pebbles")
print
print unify("(quarry_worker Fred)", "(quarry_worker ?x)")
print
print unify("(is_son Barney ?x)", "(is_son ?y Bam_Bam)")
print
print unify("(married ?x ?y)", "(married Barney Wilma)")
print
print unify("(is_son Barney ?x)", "(is_son ?y (son Barney))")
print
print unify("(is_son Barney ?x)", "(is_son ?y (son ?y))")
print
print unify("(is_son Barney Bam_Bam)", "(is_son ?y (son Barney))")
print
print unify("(loves Fred Fred)", "(loves ?x ?x)")
print
print unify("(future George Fred)", "(future ?y ?y)")
print


















