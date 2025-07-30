global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
	# Generate tokens
	Lexer = lexer.Lex(fn, text)
	tokens, error = Lexer.make_tokens()
	if error: return None, error
	
	# Generate AST
	parser_ = parser.Parser(tokens)
	ast = parser_.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error

while True:
	text = input('basic > ')
	result, error = run('<stdin>', text)

	if error: print(error.as_string())
	else: print(result)