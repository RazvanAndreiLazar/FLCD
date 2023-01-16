%{
#include <stdio.h>
#include <stdlib.h>
#define YYDEBUG 1
%}

%token IDENT
%token CONST

%token PLUS
%token MINUS
%token MULTIPLY
%token DIVIDE
%token MOD
%token LESS
%token GREATER
%token LESSEQ
%token ASSIGN
%token EQ
%token GREATEREQ 
%token DIFF
%token AND
%token OR

%token SQOPEN 
%token SQCLOSE
%token BROPEN
%token BRCLOSE
%token SBROPEN
%token SBRCLOSE
%token QUOTE
%token COMMA

%token INT
%token STRING
%token BOOL
%token ARRAY

%token IF
%token ELSE
%token WHILE

%token READ
%token PRINT

%token BEG
%token END
%token STOP

%token ENDLINE

%start program

%%

operator : PLUS { printf("operator -> +\n"); } 
        | MINUS { printf("operator -> -\n"); }  
        | MULTIPLY { printf("operator -> *\n"); } 
        | DIVIDE { printf("operator -> /\n"); } 
        | MOD { printf("operator -> mod\n"); }

relation : LESS { printf ("relation -> <\n"); } 
        | LESSEQ { printf ("relation -> <=\n"); } 
        | DIFF { printf ("relation -> !=\n"); } 
        | GREATEREQ { printf ("relation -> >=\n"); } 
        | GREATER { printf ("relation -> >\n"); }
        | EQ { printf ("relation -> ==\n"); } 
        | AND { printf ("relation -> &&\n"); }
        | OR { printf ("relation -> ||\n"); }

expression : IDENT { printf("expression -> IDENT\n"); }
        | CONST { printf("expression -> CONST\n"); }
        | IDENT operator IDENT { printf("expression -> IDENT OPERATOR IDENT\n"); }
        | IDENT operator CONST { printf("expression -> IDENT OPERATOR CONST\n"); }
        | CONST operator IDENT { printf("expression -> CONST OPERATOR IDENT\n"); }
        | CONST operator CONST { printf("expression -> CONST OPERATOR CONST\n"); }

condition : expression relation expression { printf("condition -> expression relation expression\n"); }

ioStmt : READ expression { printf("ioStmt -> READ expression\n"); }
        | PRINT expression { printf("ioStmt -> PRINT expression\n"); }

assignStmt : IDENT ASSIGN expression { printf("assignStmt -> IDENT = expression\n"); }

simplStmt : ioStmt { printf("simplStmt -> ioStmt\n"); }
        | assignStmt { printf("simplStmt -> assignStmt\n"); }

ifStmt : IF BROPEN condition BRCLOSE ENDLINE cmpdStmt { printf("ifStmt -> if ( condition ) endline cmpdStmt\n"); }
        | IF BROPEN condition BRCLOSE ENDLINE cmpdStmt ELSE ENDLINE cmpdStmt { printf("ifStmt -> if ( condition ) endline cmpdStmt else endline cmpdStmt\n"); }

whileStmt : WHILE BROPEN condition BRCLOSE ENDLINE cmpdStmt { printf("whileStmt -> while ( condition ) endline cmpdStmt\n"); }

structStmt : ifStmt { printf("structStmt -> ifStmt\n"); }
        | cmpdStmt { printf("structStmt -> cmpdStmt\n"); }
        | whileStmt { printf("structStmt -> whileStmt\n"); }

stmt : structStmt { printf("stmt -> structStmt\n"); }
        | simplStmt { printf("stmt -> simplStmt\n"); }
        | STOP { printf("stmt -> STOP\n"); }
        | declaration { printf("stmt -> declaration\n"); }

stmtlist : stmt { printf("stmtlist -> stmt\n"); }
        | stmtlist ENDLINE stmt { printf("stmtlist -> stmtlist endline stmt\n"); }

cmpdStmt : BEG ENDLINE stmtlist ENDLINE END { printf("cmpdStmt -> BEGIN endline stmtlist endline END\n"); }

program : cmpdStmt { printf("program -> cmpdStmt\n"); }
        | cmpdStmt ENDLINE { printf("program -> cmpdStmt endline\n"); }

type : primType { printf("type -> primType\n"); }
        | arrType { printf("type -> arrType\n"); }

primType : INT { printf("primType -> INT\n"); }
        | STRING { printf("primType -> STRING\n"); }
        | BOOL { printf("primType -> BOOL\n"); }

arrType : ARRAY BROPEN primType BRCLOSE SBROPEN CONST SBRCLOSE { printf("arrType -> array ( primType ) [ CONST ]\n"); }

declaration_list : IDENT { printf("declaration_list -> IDENT\n"); }
        | declaration_list COMMA IDENT { printf("declaration_list -> declaration_list , IDENT\n"); }

declaration : type SQOPEN declaration_list SQCLOSE { printf("declaration -> type { declaration_list }\n"); }

%%

void yyerror(char *s)
{
    printf("%s\n", s);
}

extern FILE *yyin;

int main(int argc, char **argv)
{
    if(argc>1) yyin = fopen(argv[1], "r");
    if(!yyparse()) fprintf(stderr,"\tOK\n");

    return 0;
}

