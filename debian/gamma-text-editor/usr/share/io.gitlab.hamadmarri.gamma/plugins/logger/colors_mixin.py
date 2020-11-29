

class ColorsMixin(object):
	
	def colorize_terminal(self, text):
		ctext = str(text).replace("<WARNING>", "<\33[33mWARNING\033[0m>")
		ctext = ctext.replace("<ERROR>", "<\33[1m\33[31mERROR\033[0m>")
		return ctext
		
		
	def colorize_textview(self, text):
		if not self.warning_color or not self.error_color:
			self.get_theme_colors()
	
		ctext = str(text).replace("<", "&lt;")
		ctext = ctext.replace(">", "&gt;")
		ctext = ctext.replace("&lt;WARNING&gt;", f'&lt;<span color="{self.warning_color}">WARNING</span>&gt;')
		ctext = ctext.replace("&lt;ERROR&gt;", f'&lt;<b><span color="{self.error_color}">ERROR</span></b>&gt;')
		
		# TODO DEBUG print(ctext)
		return ctext
		
			
	def get_theme_colors(self):	
		filename = self.app.config["style-path"]
		
		try:
			# open the file in reading mode
			f = open(filename, "r")
		except OSError as err:
			self.signal_handler.emit("log-error", self, f'Could not open {filename}: {err}')
			# default colors, in case no theme colors
			self.warning_color = "orange"
			self.error_color = "red"
			return
		except PermissionError as err:
			self.signal_handler.emit("log-error", self, f'Could not open {filename}: {err}')
			# default colors, in case no theme colors
			self.warning_color = "orange"
			self.error_color = "red"
			return
			
		# when successfully opened and read the file
		else:
			# looking for:
			# 	@define-color gamma_warning_color #FCE94F;
			# 	@define-color gamma_error_color #FF749B;
			warning_text = "@define-color gamma_warning_color"
			error_text = "@define-color gamma_error_color"
			
			for line in f:				
				if not self.warning_color:
					i = line.find(warning_text)
					if i != -1:
						pos = i + len(warning_text) + 1
						self.warning_color = line[pos:pos + 7]

				if not self.error_color:
					j = line.find(error_text)
					if j != -1:
						pos = j + len(error_text) + 1
						self.error_color = line[pos:pos + 7]
				
				if self.warning_color and self.error_color:
					break
				
			
			f.close()
			
			# default colors, in case no theme colors
			if not self.warning_color:
				self.warning_color = "orange"
				
			if not self.error_color:
				self.error_color = "red"
		
