from interface import *
import sys

class Window (RUI_Main_Window):
	def __init__(self, App: RUI_Application):
		super().__init__()
		self.setWindowTitle("Parcial 2")
		self.showMaximized()

Application = RUI_Application(sys.argv)
Log = RUI_Text_Stream()
Main_Window = Window(Application)
Main_Window.setCentralWidget(R_Workspace_Image_Canvas(Log))
Application.exec()