# Generated from grammar/Python3.g4 by ANTLR 4.9.2
import logging
from antlr4 import *


# Imports for grizzly code evaluation and execution and 
import grizzly
from grizzly.udfcompiler.udfcompiler_exceptions import UDFCompilerException

if __name__ is not None and "." in __name__:
    from .Python3d3Parser import Python3d3Parser
else:
    from Python3d3Parser import Python3d3Parser

# This class defines a complete generic visitor for a parse tree produced by Python3Parser.


class Python3d3Visitor(ParseTreeVisitor):
    def __init__(self, templates, params):
        self.params = params
        self.templates = templates
        # Lists to collect translated statements
        self.pre = []
        self.statements = []
        self.assignments = {}
        self.cursor = []
        self.exceptions = []
        self.to_eval = []
        # List containing specific elements of code to check whether it can be compiled to plain sql easily
        self.contains_stmts =   {'if-stmt': False,
                                'iterative': False,
                                'exception': False,
                                'print': False,
                                'db-reference': False
                                }

        # Parameters of the UDF need to be availiable for compiler to detect datatypes
        for param in params:
            #self.assignments[param.name] = self.templates[param.type]
            self.assignments[param.name] = self.map_type(param.type)

    @staticmethod
    def evaluate(to_eval):
        # Function to evaluate Grizzly statements into SQL Statements
        _var = ''
        _qry = ''
        for i, line in enumerate(to_eval):
            # Check whether statement is saved in a variable or executed directly
            if '=' in line:
                exec(line)
                _var = line.split('=')[0].replace(' ', '')
                # Check if statement is last from list
                if i == len(to_eval)-1:
                    _qry = eval(_var + '.generateQuery()')
            elif '.use' in line:
                exec(line)
            else:
                _qry = eval(line)
        return _qry, _var

    def map_type(self, type):
        return self.templates['types'][type]
    
    def datatype_without_brackets(self, type):
        # Remove parenthesis from datatype
        import re
        remove_brackets_expr = '[\(].*?[\)]'
        removed_brackets_type = re.sub(remove_brackets_expr, '', type)
        return removed_brackets_type

    # Visit a parse tree produced by Python3Parser#file_input.
    def visitFile_input(self, ctx: Python3d3Parser.File_inputContext):
        # First rule of syntax tree
        self.statements.append('BEGIN')
        self.visitChildren(ctx)
        self.statements.append('END;')

    # Visit a parse tree produced by Python3d3Parser#stmt.
    def visitStmt(self, ctx: Python3d3Parser.StmtContext):
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by Python3d3Parser#exception_stmt.
    def visitException_stmt(self, ctx:Python3d3Parser.Exception_stmtContext):
        self.contains_stmts['exception'] = True
        self.statements.append('BEGIN')
        self.visitChildren(ctx.suite()[0])
        self.statements.append('EXCEPTION')

        # Iterate through each exception handling
        for i, exception_stmt in enumerate(ctx.except_stmt()):
            # If an custom exception type is given
            if exception_stmt.expr():
                if type(exception_stmt.expr()) == list:
                    exception_text = exception_stmt.expr()[0].getText()
                else:
                    exception_text = exception_stmt.expr().getText()

                # Try to map error type
                try:
                    exception_text = self.templates['types'][exception_text]
                except (ValueError, KeyError):
                    # Only allow mapped exceptions in postgresql (self-defined not supported)
                    if self.templates.profile == 'postgresql':
                        exception_text = 'OTHERS'

                self.statements.append('WHEN ' + exception_text + ' THEN')
            # If no exception type is defined, grab all
            else:
                self.statements.append('WHEN OTHERS THEN')
            # Visit code in exception clause
            self.visitChildren(ctx.suite()[i+1])

        self.statements.append('END;')

    # Visit a parse tree produced by Python3d3Parser#raise_stmt.
    def visitRaise_stmt(self, ctx:Python3d3Parser.Raise_stmtContext):
        exception_name = ctx.NAME() if ctx.NAME() else 'def'
        # Only add custom exceptions if dbms supports it
        if self.templates.profile == 'oracle':
            # Add excpetion declaration
            self.exceptions.append(f'{exception_name} EXCEPTION;')
            self.statements.append(f'RAISE {exception_name};')
        # Add custom error type as message in postgresql
        elif self.templates.profile == 'postgresql':
            self.statements.append(f"RAISE EXCEPTION '{exception_name}';")
        else:
            logging.info(f'Raising exceptions not possible for {self.templates.profile} DB')

    # Visit a parse tree produced by Python3d3Parser#simple_stmt.
    def visitSimple_stmt(self, ctx: Python3d3Parser.Simple_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#small_stmt.
    def visitSmall_stmt(self, ctx: Python3d3Parser.Small_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#assignment_stmt.
    def visitAssignment_stmt(self, ctx: Python3d3Parser.Assignment_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#initialization.
    def visitInitialization(self, ctx:Python3d3Parser.InitializationContext):
        # Function to visit initialization with datatype
        # i: int = 0
        self.assignments[ctx.NAME().getText()] = self.map_type(ctx.typ().getText())
        #self.templates[ctx.typ().getText()]
        self.statements.append(f'{ctx.NAME().getText()} := {self.visitChildren(ctx)};')

    # Visit a parse tree produced by Python3d3Parser#declaration.
    def visitDeclaration(self, ctx:Python3d3Parser.DeclarationContext):
        # Function to visit declaration of variable with datatype
        # i: int
        self.assignments[ctx.NAME().getText()] = self.map_type(ctx.typ().getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#nontype_initialization.
    def visitNontype_initialization(self, ctx:Python3d3Parser.Nontype_initializationContext):
        # Function to visit initialization without a datatype
        # i = 0 / i = False etc.
        # i = 3 / g_df1 = grizzly.read('table')

        # If initialization is for a grizzly statement
        if ctx.GRZLYNAME():
            self.to_eval.append(ctx.getText())
            return

        # If assignment isn't an grizzly statement
        assignment = self.visit(ctx.expr())
        var = ctx.NAME().getText()

        # Check if variable name is not already in assignments (of types)
        if var not in self.assignments:
            declr_expr = ctx.expr()
            # If expression is typecasted
            if declr_expr.typecast():
                var_type_raw = declr_expr.typecast().typ().getText()
                var_type = self.map_type(var_type_raw)
            # If the expression is a string
            elif declr_expr.STRING():
                var_type = self.map_type('str')
            # If expression is a number try to load mapped datatype
            elif declr_expr.NUMBER():
                var_type = self.map_type('int')
            # If expression is a float try to load mapped datatype
            elif declr_expr.FLOAT():
                var_type = self.map_type('float')
            # If expression is a bool try to load mapped datatype
            elif declr_expr.BOOL():
                var_type = self.map_type('bool')
            # If expression is a list try to load mapped datatype
            elif declr_expr.list_expr():
                list_expr = declr_expr.list_expr()
                var_type = self.map_type('list')
                if list_expr.elems():
                    list_elems = list_expr.elems()
                    first_elem = list_elems.elem()[0]
                    # init list with first element datatype
                    if first_elem.NUMBER():
                        var_type = var_type.replace('$$datatype$$', self.map_type('int'))
                    elif first_elem.STRING():
                        var_type = var_type.replace('$$datatype$$', self.map_type('str'))
                    elif first_elem.FLOAT():
                        var_type = var_type.replace('$$datatype$$', self.map_type('float'))
                    elif first_elem.BOOL():
                        var_type = var_type.replace('$$datatype$$', self.map_type('bool'))
                    else: 
                        raise TypeError(f'Cant handle datatype of "{list_elems}" list')
                else:
                    raise TypeError(f'Please define a datatype for list "{var}"')
            
            # If assignment contains an operation
            elif declr_expr.calc_op():
                if 'CONCAT' in assignment or 'REPEAT' in assignment:
                    var_type = self.map_type('str')
                else:
                    var_type = self.map_type('int')
            elif assignment in self.assignments:
                var_type = self.map_type(self.assignments[assignment])
            
            # If assignment is an list element
            elif declr_expr.list_dec():
                list_decl = declr_expr.list_dec()
                list_var = list_decl.NAME().getText()
                list_type = self.assignments[list_var]
                var_type = list_type[:list_type.rfind('[')]
                #assignment = self.visit(declr_expr.list_dec())
            
            # If datatype could not be found
            else:
                raise TypeError(f'Please define a type for "{assignment}" expression in your UDF')
                var_type = '<UNDEFINED>'
                
            self.assignments[var] = var_type
        
        if ctx.expr().list_expr():
            self.statements.append(f'{var} := array{assignment};')
        else:
            self.statements.append(f'{var} := {assignment};')

    # Visit a parse tree produced by Python3d3Parser#Lst_assignment.
    def visitLst_assignment(self, ctx: Python3d3Parser.Lst_assignmentContext):
        # Function to generate list assignment statement
        index = int(ctx.NUMBER().getText()) + 1
        self.statements.append(f'{ctx.NAME()}[{index}] := {self.visit(ctx.expr())};')

    # Visit a parse tree produced by Python3d3Parser#flow_stmt.
    def visitFlow_stmt(self, ctx: Python3d3Parser.Flow_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#break_stmt.
    def visitBreak_stmt(self, ctx: Python3d3Parser.Break_stmtContext):
        self.statements.append('EXIT;')

    # Visit a parse tree produced by Python3d3Parser#continue_stmt.
    def visitContinue_stmt(self, ctx: Python3d3Parser.Continue_stmtContext):
        self.statements.append('CONTINUE;')

    # Visit a parse tree produced by Python3d3Parser#return_stmt.
    def visitReturn_stmt(self, ctx: Python3d3Parser.Return_stmtContext):
        #returns = ctx.expr().getText().replace('"',"'")
        returns = self.visitChildren(ctx)
        self.statements.append(f'RETURN {returns};')

    # Visit a parse tree produced by Python3d3Parser#except_stmt.
    def visitExcept_stmt(self, ctx:Python3d3Parser.Except_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#compound_stmt.
    def visitCompound_stmt(self, ctx: Python3d3Parser.Compound_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#if_stmt.
    def visitIf_stmt(self, ctx: Python3d3Parser.If_stmtContext):
        self.contains_stmts['if_stmt'] = True
        # Counter to keep track of if and elifs
        test_counter = 0
        # Iterate through all tests and suites
        for i, suite in enumerate(ctx.suite()):
            if i == 0:
                test = self.visit(ctx.ob_test()[test_counter])
                self.statements.append(f'IF {test} THEN')
                test_counter += 1
            elif i == len(ctx.suite())-1 and 'else' in ctx.getText():
                self.statements.append(f'ELSE')
            elif 'elif' in ctx.getText():
                test = self.visit(ctx.ob_test()[test_counter])
                self.statements.append(f'ELSIF {test} THEN')
                test_counter += 1
            self.visitChildren(suite)
        
        self.statements.append('END IF;')

    # Visit a parse tree produced by Python3d3Parser#while_stmt.
    def visitWhile_stmt(self, ctx: Python3d3Parser.While_stmtContext):
        # Function to visit while statement in syntaxtree
        self.contains_stmts['iterative'] = True
        # Get test statement
        test = self.visit(ctx.ob_test())
        # Check if while loop is a while True loop
        if test != 'True':
            self.statements.append(f'WHILE {test}')
        self.statements.append('LOOP')
        self.visit(ctx.suite())
        self.statements.append('END LOOP;')

    # Visit a parse tree produced by Python3d3Parser#for_stmt.
    def visitFor_stmt(self, ctx: Python3d3Parser.For_stmtContext):
        self.contains_stmts['iterative'] = True

        # Get iteration variable
        iteration_var = ctx.NAME().getText()

        # Check if variable for iterating exists or if iteration var is a cursor
        temp_list = []
        for assignm in self.assignments:
            temp_list.append(assignm)
        if iteration_var not in temp_list and not ctx.GRZLYNAME():
            self.assignments[iteration_var] = self.map_type('int')

        # Iteration through range
        if ctx.rang():
            self.statements.append(f'FOR {iteration_var} IN {self.visit(ctx.rang())}')
        
        # Iterating through variables (expr1 = iteration var)
        elif ctx.expr():
            var = self.visit(ctx.expr())
            if self.templates.profile == 'oracle':
                raise UDFCompilerException(f'Iterating with variable "{var}" not possible in oracle')
            self.statements.append(f'FOREACH {iteration_var} IN ARRAY {var}')
        
        # Iteration through grizzly refernce
        elif ctx.GRZLYNAME():
            # evaluate grizzly refernce
            _qry, _var = Python3d3Visitor.evaluate(self.to_eval)
            self.to_eval = []
            # If query isn't a SQL-Query already
            if type(_qry) == grizzly.expression.ColRef:
                _qry = _qry.generateQuery()
            
            # Add cutom cursor for declaration block
            template = self.map_type('cursor')
            self.cursor.append(template.replace('$$var$$', _var).replace('$$qry$$', _qry))

            #self.statements.append(f'OPEN {str(iteration_var};')
            self.statements.append(f'FOR {iteration_var} IN {str(ctx.GRZLYNAME().getText())}')
        
        # Create block for suite in for loop
        self.statements.append('LOOP')
        self.visit(ctx.suite())
        self.statements.append('END LOOP;')

    # Visit a parse tree produced by Python3d3Parser#suite.
    def visitSuite(self, ctx: Python3d3Parser.SuiteContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#Ob_test.
    def visitOb_test(self, ctx:Python3d3Parser.Ob_testContext):
        # Function to visit test statements concatenated with logical operators
        tests = []
        if len(ctx.test()) == 1:
            return self.visit(ctx.test()[0])
        else:
            for _, op in enumerate(ctx.log_op()):
                l = self.visit(ctx.test()[0])
                r = self.visit(ctx.test()[1])
                log_op = self.visit(op)
                tests.append(f'{l} {log_op} {r}')
        return ' '.join(tst for tst in tests)

    # Visit a parse tree produced by Python3d3Parser#test.
    def visitTest(self, ctx:Python3d3Parser.TestContext):
        # Function to visit test statements with comparasion operators
        tsts = []
        if len(ctx.comp_op()) == 0:
            return self.visit(ctx.expr()[0])
        else:
            for i, op in enumerate(ctx.comp_op()):
                comp_op = self.visit(op)
                l = self.visit(ctx.expr()[0])
                r = self.visit(ctx.expr()[1])
                tsts.append(f'{l} {comp_op} {r}')
        
        return ' '.join(tst for tst in tsts)

    # Visit a parse tree produced by Python3d3Parser#print_stmt.
    def visitPrint_stmt(self, ctx: Python3d3Parser.Print_stmtContext):
        self.contains_stmts['print'] = True
        # special treatment for oracle and postgresql DBMS
        if self.templates.profile == 'postgresql':
            # Check whether printed statement contains variables or just a string
            if ctx.expr().STRING():
                template = self.templates['funcs']['print_str']
            else:
                template = self.templates['funcs']['print_var']
        else:
            template = self.templates['funcs']['print']
        
        # Add pre sql for enabling serveroutput on oracle DBMS
        if '/' in template:
            self.pre.append(template.split('/')[0])
            self.statements.append(template.split('/')[1].replace('$$code$$', self.visit(ctx.expr())))
        else:
            self.statements.append(template.replace('$$code$$', self.visit(ctx.expr())))
        
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#range.
    def visitRang(self, ctx: Python3d3Parser.RangContext):
        # Function to visit range statement
        if len(ctx.expr()) == 2:
            # If a special range between two expressions is defined
            l = self.visit(ctx.expr()[0])
            r = self.visit(ctx.expr()[1])
            if r in self.assignments:
                r = f'{r} - 1'
            for_loop = f'{str(l)}..{str(r)}'
        else:
            # If only the upper limit of range statement is defined (range(3))
            for_loop = f'0..{str(self.visit(ctx.expr()[0]))}-1'
        return for_loop

    # Visit a parse tree produced by Python3d3Parser#comp_op.
    def visitComp_op(self, ctx: Python3d3Parser.Comp_opContext):
        # Function to visit comparison operators
        comp_op = ctx.getText()
        if comp_op == '==':
            comp_op = '='
        return comp_op
    
    def visitLog_op(self, ctx: Python3d3Parser.Log_opContext):
        # Function to visit logical operators
        return ctx.getText()

    # Visit a parse tree produced by Python3d3Parser#expr.
    def visitExpr(self, ctx: Python3d3Parser.ExprContext):
        # Function to visit expressions
        if ctx.NAME() or ctx.STRING() or ctx.NUMBER() or ctx.FLOAT() or ctx.BOOL() or ctx.list_expr():
            return ctx.getText().replace('"', "'")
        
        # If expression contains an operation
        if ctx.calc_op():
            # Get left and right side of equasion
            l = ctx.expr()[0]
            r = ctx.expr()[1]

            # Get calculate operator
            calc_op = self.visit(ctx.calc_op())

            l = self.visit(l)
            r = self.visit(r)

            if calc_op == '%':
                return f'MOD({l},{r})'

            # Check for String occasions in left and right side of equasion (n-1) with Tokens and checking in the assignments dict
            left_side_contains_str = (ctx.expr()[0].NAME() and self.assignments.get(str(ctx.expr()[0].NAME())) == self.map_type('str')) or ctx.expr()[0].STRING()
            right_side_contains_str = (ctx.expr()[1].NAME() and self.assignments.get(str(ctx.expr()[1].NAME())) == self.map_type('str')) or ctx.expr()[1].STRING()

            # If left or right side of equasion contains a string
            if left_side_contains_str or right_side_contains_str \
                or ('CONCAT' in l or 'CONCAT' in r) \
                or (('CAST' in l or 'CAST' in r) and self.map_type('str') in l or self.map_type('str') in r):
                # Function for adding strings
                if '+' in calc_op:
                    return (f'CONCAT({l}, {r})') 
                # Function for multiplying strings (reapeating)
                elif '*' in calc_op:
                    if right_side_contains_str:
                        if self.templates.profile == 'oracle':
                            return f'RPAD({r}, LENGTH({r})*{l}, {r})'
                        return (f'REPEAT({r}, {l})')
                    else:
                        if self.templates.profile == 'oracle':
                            return f'RPAD({l}, LENGTH({l})*{r}, {l})'
                        return (f'REPEAT({l}, {r})')
            
            return f'{l} {calc_op} {r}'

        # Add parenthesis if needed
        if ctx.parenthesis_expr():
            return f'({self.visit(ctx.parenthesis_expr().expr())})'
        
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#Calc_op.
    def visitCalc_op(self, ctx:Python3d3Parser.Calc_opContext):
        # Function to visit calculation operator
        calc_op = ctx.getText()
        # special operators for postgresql
        if self.templates.profile == 'postgresql':
            if calc_op == '**':
                calc_op = '^'
            elif calc_op == '^':
                calc_op = '#'
        return calc_op

    # Visit a parse tree produced by Python3d3Parser#func_call.
    def visitFunc_call(self, ctx:Python3d3Parser.Func_callContext):
        funcnames = []
        funcname = ctx.NAME()
        # Get function with modules
        for m in funcname:
            funcnames.append(m.getText())
        funcname = '.'.join(f for f in funcnames)
        # Get parameters of function
        params = ctx.params().getText()
        # Check if the function is mapped in template
        try:
            funccall = self.templates['funcs'][str(funcname)]
            funccall = funccall.replace('$$params$$', params)
        except (ValueError, KeyError):
            # If function is not mapped, just get whole funccall
            funccall = ctx.getText()
        return funccall

    # Visit a parse tree produced by Python3d3Parser#grzly_expr.
    def visitGrzly_expr(self, ctx:Python3d3Parser.Grzly_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by Python3d3Parser#typecast.
    def visitTypecast(self, ctx:Python3d3Parser.TypecastContext):
        # Function to visit typecast
        var_type_sql = self.map_type(ctx.typ().getText())
        if self.templates.profile == 'oracle':
            var_type_sql = self.datatype_without_brackets(var_type_sql)

        return f'CAST({self.visit(ctx.expr())} AS {var_type_sql})'

    # Visit a parse tree produced by Python3d3Parser#List_dec.
    def visitList_dec(self, ctx:Python3d3Parser.List_decContext):
        # Function to visit list operations
        list_decl = ctx
        list_var = list_decl.NAME().getText()
        list_type = self.assignments[list_var]
        var_type = list_type[:list_type.rfind('[')]
        lst_index = int(list_decl.NUMBER().getText()) + 1
        assignment = f'{list_var}[{lst_index}]'
        return assignment

    # Visit a parse tree produced by Python3d3Parser#db_reference.
    def visitDb_reference(self, ctx:Python3d3Parser.Db_referenceContext):
        # Function to visit db-reference
        self.contains_stmts['db_reference'] = True
        return f'{ctx.NAME()[0]}.{ctx.NAME()[1]}'

del Python3d3Parser
