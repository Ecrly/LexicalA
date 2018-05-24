KEYWORDS_GO = [
'break',	'default', 'func', 'interface', 'select',
'case',	 'defer', 'go' ,'map',	'struct',
'chan',	'else', 'goto', 'package',	'switch',
'const',	'fall','through',	'if',	'range',	'type',
'continue','for',	'import',	'return',	'var']

KEYWORDS = [
'and',	'exec',	'not',
'assert',	'finally',	'or',
'break',	'for',	'pass',
'class',	'from', 'print',
'continue',	'global',	'raise',
'def',	'if',	'return',
'del',	'import',	'try',
'elif',	'in',	'while',
'else',	'is',	'with',
'except',	'lambda',	'yield',
]

KEYWORDS_C = [
    'auto','double','int','struct','break','else','long','switch','case','enum','register','typedef',
    'char','extern','return','union','const','float','short','unsigned','continue',
    'for','signed','void','default','goto','sizeof','volatile','do','if','while','static',
]

KEYWORDS_C_MAP ={
    'auto': 'AUTO',
     'double': 'DOUBLE',
     'int': 'INT',
     'struct': 'STRUCT',
     'break': 'BREAK',
     'else': 'ELSE',
     'long': 'LONG',
     'char': 'CHAR',
     'return': 'RETURN',
     'float': 'FLOAT',
     'for': 'FOR',
     'void': 'VOID',
     'if': 'IF',
     'while': 'WHILE'
}

DELIMITER = ['(', ')', '[', ']', '{', '}']

PUNCTUNTION = ['.', ',', ':', ';']

OPERATOR = ['+', '-', '*', '/', '%', '>', '<', '=', '|', '&']

FILE = 'code_c.txt'


