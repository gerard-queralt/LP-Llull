grammar llull;

root : fun+ EOF ;

fun : funtype SYMBOL '(' (SYMBOL (',' SYMBOL)*)? ')' block
    ;

statement : SYMBOL (ariop)? '=' expr #assig
    | 'array' '(' SYMBOL ',' expr ')' #array
    | 'set' '(' SYMBOL ',' expr ',' expr ')' #set
    | 'write' '(' (expr | STRING) (',' (expr | STRING))* ')' #write
    | 'read' '(' SYMBOL (',' SYMBOL)* ')' #read
    | 'if' '(' expr ')' (statement | block) ('else' (statement | block))? #if
    | 'while' '(' expr ')' (statement | block) #while
    | 'for' '(' SYMBOL '=' expr ';' expr ';' SYMBOL '=' expr ')' (statement | block) #for
    | SYMBOL '(' (expr (',' expr)*)? ')' #call
    ;
    
block : '{' statement+ '}'
    ;
    
expr : '(' expr ')' #parenthesis
    | <assoc=right> expr '^' expr #pow
    | expr ('*'|'/'|'%') expr #multDivMod
    | expr ('+'|'-') expr #sumSub
    | expr BOOLOP expr #boolExpr
    | '!' expr #notExpr
    | 'get' '(' SYMBOL ',' expr ')' #get
    | (NUM | SYMBOL) #value
    ;

ariop : '^' | '*' | '/' | '%' | '+' | '-' ;

funtype : 'void' ;
    
NUM : [0-9]+ ;
SYMBOL : [a-zA-Z] [a-zA-Z0-9]* ;
BOOLOP : '==' | '<>' | '<' | '>' | '<=' | '>=' | '&&' | '||' ;
STRING : ('"' [\u0020-\u0021\u0024-\u007E\u0080-\u00FF]* '"') ;
COMMENT : '#' ~[\r\n]* -> skip;
WS : [ \n]+ -> skip ; 
