def string_with_arrows(text,pos_start,pos_end):
    result=''
	
    idx_start=max(text.rfind('\n',0,pos_start.idx),0)
    idx_end=text.find('\n',idx_start+1)

    if idx_end <0 :idx_end=len(text)

    line_count=pos_end.ln - pos_start.ln +1
    for i in range(line_count):
        line=text[idx_start:idx_end]
        col_start=pos_start.col if i==0 else 0
        col_end=pos_end.col if i==line_count-1 else len(line)-1

        result+=line+'\n'
        result+=' '*col_start+'^'*(col_end-col_start)

        idx_start=idx_end
        idx_end=text.find('\n',idx_start+1)
        if idx_end<0 :idx_end=len(text)

    return result.replace('\t','')





class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details
	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result