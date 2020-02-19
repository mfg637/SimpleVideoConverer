import tkinter
import tkinter.ttk
import tkinter.filedialog
import converter


class MainWindow:
	def __init__(self, sources_list=None):
		self._root = tkinter.Tk()
		self._list = tkinter.Listbox(self._root, width=50)
		self._add_files(sources_list)
		#self._list.insert(0, sources_list)
		self._list.grid(row=0, column=0, columnspan=3)
		self._addfiles_btn = tkinter.ttk.Button(self._root, text="Add files", command=self._add_files)
		self._addfiles_btn.grid(row=1, column=0, columnspan=3)

		self._mode_selector_header = tkinter.Label(self._root, text="Select convert mode:")
		self._mode_selector_header.grid(row=2, column=0, sticky="w", columnspan=2)
		self._mode = tkinter.IntVar(self._root, 0)
		self._CRF_radio_btn = tkinter.Radiobutton(self._root, text="CRF:", variable=self._mode, value=0)
		self._CRF_radio_btn.grid(row=3,column=0, sticky="w")
		self._CRF_value_field = tkinter.Entry(self._root)
		self._CRF_value_field.insert(0, "18")
		self._CRF_value_field.grid(row=3, column=1, sticky="w")
		self._2pass_radio_btn = tkinter.Radiobutton(
			self._root, text="2 pass bitrate kbps:", variable=self._mode, value=1
		)
		self._2pass_radio_btn.grid(row=4,column=0, sticky="w")
		self._2pass_bitrate = tkinter.Entry(self._root)
		self._2pass_bitrate.insert(0, "5000")
		self._2pass_bitrate.grid(row=4, column=1, sticky="w")

		self._vcodec_label = tkinter.Label(self._root, text="Video codec:")
		self._vcodec_label.grid(row=5, column=0, sticky="w")
		self._vcodec_field = tkinter.ttk.Combobox(self._root, values=['libx264', 'libx265'])
		self._vcodec_field.current(0)
		self._vcodec_field.grid(row=5, column=1, sticky="w")
		
		self._preset_label = tkinter.Label(self._root, text="Quality level (encoding time):")
		self._preset_label.grid(row=6, column=0, sticky="w")
		self._preset_field= tkinter.ttk.Combobox(self._root, values=[
			'ultrafast',
			'superfast',
			'veryfast',
			'faster',
			'fast',
			'medium',
			'slow',
			'slower',
			'veryslow',
			'placebo'
		])
		self._preset_field.current(8)
		self._preset_field.grid(row=6, column=1)
		self._convert_btn = tkinter.ttk.Button(self._root, text="Convert", command=self._start_convert)
		self._convert_btn.grid(row=7, column=0, columnspan=3)
		self._progress=tkinter.ttk.Progressbar(self._root, length=400)
		self._progress.grid(row=8, column=0, columnspan=3)
		self._root.mainloop()

	def _add_files(self, sources_list=None):
		files = None
		if sources_list is None:
			files = tkinter.filedialog.askopenfilenames()
		else:
			files=sources_list
		print(files)
		if (files is None) or (len(files)==0):
			return
		if self._list.get(0)=="":
			self._list.delete(0, tkinter.END)
			for file in files:
				self._list.insert(0, file)
		else:
			for file in files:
				self._list.insert(tkinter.END, file)

	def _callback(self, n=None):
		if n is None:
			self._progress.step()
			self._progress.update_idletasks()
		else:
			self._progress['value']=0
			self._progress['maximum']=n

	def _start_convert(self):
		converter.convert(
                        self._vcodec_field.get(),
			self._list.get(0, tkinter.END),
			self._mode.get(),
			int(self._CRF_value_field.get()),
			int(self._2pass_bitrate.get()),
			self._preset_field.get(),
			self._callback
		)
		self._list.delete(0, tkinter.END)
