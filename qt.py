from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtOpenGL import *
from PySide6.QtOpenGLWidgets import *

from multipledispatch import dispatch

class RW_Settings(QSettings):
	def __init__(self):
		super().__init__("Raylight")

	def init(self, App: QApplication):
		super().setValue("ResX", App.primaryScreen().size().width())
		super().setValue("ResY", App.primaryScreen().size().height())
		super().setValue("Margin", self.ResYP(0.5))
		super().setValue("Export_Precision", 6)
		super().setValue("Display_Precision", 4)
		return self

	def ResX(self):
		return int(self.value("ResX"))
	def ResY(self):
		return int(self.value("ResY"))
	def ResXP(self, Percent):
		return int(self.value("ResX") / 100 * Percent)
	def ResYP(self, Percent):
		return int(self.value("ResY") / 100 * Percent)

class RW_Application(QApplication):
	def __init__(self, Args):
		super().__init__(Args)

class RW_Dock(QDockWidget):
	def __init__(self, Title = ""):
		super().__init__(Title)
		super().setObjectName("Default_Dock")

	def setWidget(self, Widget):
		super().setWidget(Widget)
		return self

	def setTitleBarWidget(self, Widget):
		super().setTitleBarWidget(Widget)
		return self

class RW_Slider(QSlider):
	def __init__(self, Vertical: bool = False):
		if Vertical:
			super().__init__(Qt.Orientation.Vertical)
		else:
			super().__init__(Qt.Orientation.Horizontal)
		super().setObjectName("Default_Slider")

		super().setContentsMargins(0,0,0,0)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

	def setRange(self, Min: int, Max: int):
		super().setRange(Min, Max)
		return self

	def setValue(self, Value):
		super().setValue(Value)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFixedHeight(self, H: int):
		super().setFixedHeight(H)
		return self

	def setMinimum(self, Value: int = 0):
		super().setMinimum(Value)
		return self

	def setMaximum(self, Value: int = 0):
		super().setMaximum(Value)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

class RW_Button(QPushButton):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Button")
		self.setFixedHeight(25)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

	def setText(self, Text: str):
		super().setText(Text)
		return self

	def setIcon(self, Icon:QIcon):
		super().setIcon(Icon)
		return self

	def setFixedSize(self, Width:int, Height:int):
		super().setFixedSize(Width, Height)
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setLinearMargins(self, Vertical: int, Horizontal: int):
		super().setContentsMargins(Horizontal,Vertical,Horizontal,Vertical)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setFixedHeight(self, H: int):
		super().setFixedHeight(H)
		return self

	def setFixedWidth(self, W: int):
		super().setFixedWidth(W)
		return self

	def hide(self):
		super().hide()
		return self

	def show(self):
		super().show()
		return self

class RW_Spacer(QLabel):
	def __init__(self, Vertical: bool = True, Size: int = 10):
		super().__init__()
		super().setObjectName("Default_Label")

		if Vertical: super().setFixedHeight(Size)
		else: super().setFixedWidth(Size)

class RW_Linear_Contents(QWidget):
	def __init__(self, Vertical: bool = True):
		super().__init__()
		super().setObjectName("Default_Widget")

		super().setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		super().setContentsMargins(0,0,0,0)
		self.Linear_Layout = RW_Linear_Layout(Vertical)
		super().setLayout(self.Linear_Layout)

	def addWidget(self, Widget, Alignment:str = "T B L R CV CH", Stretch:int = 0):
		if Alignment == "T": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignTop)
		elif Alignment == "B": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignBottom)
		elif Alignment == "L": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignLeft)
		elif Alignment == "R": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignRight)
		elif Alignment == "CV": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignVCenter)
		elif Alignment == "CH": self.Linear_Layout.addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignCenter)
		else: self.Linear_Layout.addWidget(Widget, Stretch)
		return self

	def clear(self):
		for i in range(self.Linear_Layout.count()):
			self.Linear_Layout.itemAt(i).widget().hide()
			self.Linear_Layout.itemAt(i).widget().deleteLater()
		return self

	def setSpacing(self, Spacing: int):
		self.Linear_Layout.setSpacing(Spacing)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		self.Linear_Layout.setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setMargins(self, Margins: int):
		self.Linear_Layout.setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

	def setFixedHeight(self, H: int):
		super().setFixedHeight(H)
		return self

	@dispatch(int,int)
	def setStretch(self, Index: int = 0, Stretch: int = 1):
		self.Linear_Layout.setStretch(Index, Stretch)
		return self

	@dispatch(dict)
	def setStretch(self, Dictionary: dict = {}):
		for Key in Dictionary:
			self.Linear_Layout.setStretch(Key,Dictionary[Key])
		return self

	def setWindowTitle(self, Title: str = "Title"):
		super().setWindowTitle(Title)
		return self

	def setWindowIcon(self, Icon: QIcon):
		super().setWindowIcon(Icon)
		return self

	def children(self):
		return self.Linear_Layout.children()

	def hide(self):
		super().hide()
		return self

class RW_Line_Editor(QLineEdit):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_LineEdit")

		super().setContentsMargins(0,0,0,0)

	def setDisabled(self, Status: bool = True):
		super().setDisabled(Status)
		return self

	def setParent(self, Parent):
		super().setParent(Parent)
		return self

	def setText(self, Text: str):
		super().setText(Text)
		return self

	def setHidden(self, Status: bool = True):
		super().setHidden(Status)
		return self

	def setFrame(self, Status: bool):
		super().setFrame(Status)
		return self

	def hide(self):
		super().hide()
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

	def selectAll(self):
		super().selectAll()
		return self

	def setFocus(self):
		super().setFocus()
		return self

	def setCursorPosition(self, Position: int):
		super().setCursorPosition(Position)
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setValidator(self, Validator: QValidator):
		super().setValidator(Validator)
		return self

class RW_Text_Editor(QTextEdit):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_TextEdit")

		super().setContentsMargins(0,0,0,0)
		super().setTabStopDistance(40)

	def setDisabled(self, Status: bool = True):
		super().setDisabled(Status)
		return self

	def setParent(self, Parent):
		super().setParent(Parent)
		return self

	def setText(self, Text: str):
		super().setText(Text)
		return self

	def setHtml(self, Text: str):
		super().setHtml(Text)
		return self

	def setHidden(self, Status: bool = True):
		super().setHidden(Status)
		return self

	def hide(self):
		super().hide()
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

	def selectAll(self):
		super().selectAll()
		return self

	def setFocus(self):
		super().setFocus()
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

class RW_Linear_Layout(QBoxLayout):
	def __init__(self, Vertical: bool = True):
		if Vertical: 
			super().__init__(QBoxLayout.Direction.TopToBottom)
			super().setAlignment(Qt.AlignmentFlag.AlignTop)
		else: 
			super().__init__(QBoxLayout.Direction.LeftToRight)
			super().setAlignment(Qt.AlignmentFlag.AlignLeft)

		super().setSpacing(2)
		super().setContentsMargins(0,0,0,0)

	def addWidget(self, Widget:QWidget, Alignment:str = "T B L R CV CH", Stretch:int = 0):
		if Alignment == "T": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignTop)
		elif Alignment == "B": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignBottom)
		elif Alignment == "L": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignLeft)
		elif Alignment == "R": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignRight)
		elif Alignment == "CV": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignVCenter)
		elif Alignment == "CH": super().addWidget(Widget, Stretch, Qt.AlignmentFlag.AlignCenter)
		else: super().addWidget(Widget, Stretch)
		return self

	def setLinearMargins(self, Vertical: int, Horizontal: int):
		super().setContentsMargins(Horizontal,Vertical,Horizontal,Vertical)
		return self

	def setSpacing(self, Spacing: int):
		super().setSpacing(Spacing)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	@dispatch(int,int)
	def setStretch(self, Index: int = 0, Stretch: int = 1):
		super().setStretch(Index, Stretch)
		return self

	@dispatch(dict)
	def setStretch(self, Dictionary: dict = {}):
		for Key in Dictionary:
			super().setStretch(Key,Dictionary[Key])
		return self

	def clear(self):
		for i in range(self.count()):
			self.itemAt(i).widget().hide()
			self.itemAt(i).widget().deleteLater()
		return self

class RW_Scroll_Area(QScrollArea):
	def __init__(self, Vertical: bool = True):
		super().__init__()
		super().setObjectName("Default_ScrollArea")

		super().setWidgetResizable(True)
		super().setContentsMargins(0,0,0,0)

		if Vertical:
			super().setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		else: 
			super().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

	def setWidget(self, Widget):
		super().setWidget(Widget)
		return self

class RW_File_Explorer(QFileDialog):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_FileBrowser")

	def exec(self):
		super().exec()
		return self

	def setAcceptMode(self, Mode: QFileDialog.AcceptMode):
		super().setAcceptMode(Mode)
		return self

	def setFilter(self, Filters: QDir.Filter):
		super().setFilter(Filters)
		return self

	def setDefaultSuffix(self, Suffix: str):
		super().setDefaultSuffix(Suffix)
		return self

	def setFileMode(self, Mode: QFileDialog.FileMode):
		super().setFileMode(Mode)
		return self

	def __call__(self):
		return self

class RW_Text_Stream(QTextBrowser):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_TextStream")

		super().setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setContentsMargins(self, Left: int, Top: int, Right: int, Bottom: int):
		super().setContentsMargins(Left,Top,Right,Bottom)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setFixedHeight(self, H: int):
		super().setFixedHeight(H)
		return self

	def setFixedWidth(self, W: int):
		super().setFixedWidth(W)
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def setVerticalScrollBar(self, Scrollbar: QScrollBar):
		super().setVerticalScrollBar(Scrollbar)
		return self

	def append(self, Text:str = ""):
		super().append(Text)
		return self

	def concat(self, Text:str = ""):
		super().moveCursor(QTextCursor.MoveOperation.End)
		super().insertPlainText(str(Text))
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

	def setHtml(self, Text: str):
		super().setHtml(Text)
		return self

class RW_Splitter(QSplitter):
	def __init__(self, Vertical: bool = True):
		if Vertical: super().__init__(Qt.Orientation.Vertical)
		else: super().__init__(Qt.Orientation.Horizontal)
		super().setObjectName("Default_Splitter")

		super().setHandleWidth(5)
		super().setContentsMargins(0,0,0,0)

	def addWidget(self, Widget):
		super().addWidget(Widget)
		return self

	def setHandleWidth(self, Width):
		super().setHandleWidth(Width)
		return self

	def setSizes(self, Sizes):
		super().setSizes(Sizes)
		return self

	def setStyleSheet(self, Style):
		super().setStyleSheet(Style)
		return self

class RW_Label(QLabel):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Label")

		super().setContentsMargins(0,0,0,0)
		super().setScaledContents(True)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
	
	def setLayout(self, Layout: QLayout):
		super().setLayout(Layout)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

	def setMinimumSize(self, Width: int, Height: int):
		super().setMinimumSize(Width,Height)
		return self

	def setText(self, Text: str):
		super().setText(Text)
		return self

	def setFont(self, Font: QFont):
		super().setFont(Font)
		return self

	def setLinearMargins(self, Vertical: int, Horizontal: int):
		super().setContentsMargins(Horizontal,Vertical,Horizontal,Vertical)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setFixedWidth(self, Width: int):
		super().setFixedWidth(Width)
		return self

	def setParent(self, Parent):
		super().setParent(Parent)
		return self

class RW_Widget(QWidget):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Widget")

		super().setContentsMargins(0,0,0,0)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

	def setLayout(self, Layout: QLayout):
		super().setLayout(Layout)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFont(self, Font: QFont):
		super().setFont(Font)
		return self

	def setLinearMargins(self, Vertical: int, Horizontal: int):
		super().setContentsMargins(Horizontal,Vertical,Horizontal,Vertical)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setFixedWidth(self, Width: int):
		super().setFixedWidth(Width)
		return self

class RW_Menu(QMenu):
	def __init__(self, Title = "Title"):
		super().__init__(Title)
		super().setObjectName("Default_Menu")
		
		super().setContentsMargins(0,0,0,0)

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def addAction(self, Text:str, Action):
		super().addAction(Text, Action)
		return self

	def setLayout(self, Layout):
		super().setLayout(Layout)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

	def setFixedWidth(self, Width: int):
		super().setFixedWidth(Width)
		return self

	def setFixedSize(self, Width: int, Height: int):
		super().setFixedSize(Width, Height)
		return self

class RW_Window(QMainWindow):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Window")

		super().setDockNestingEnabled(True)

	def setWindowTitle(self, Title: str):
		super().setWindowTitle(Title)
		return self

	def addDockWidget(self, Widget:QDockWidget, Area:Qt.DockWidgetArea):
		super().addDockWidget(Area, Widget)
		return self

	def setWindowIcon(self, Icon: QIcon):
		super().setWindowIcon(Icon)
		return self

	def resizeEvent(self, event):
		return super().resizeEvent(event)

	def setBaseSize(self, Width, Height):
		super().setBaseSize(Width ,Height)
		return self

	def setFixedSize(self, Width, Height):
		super().setFixedSize(Width ,Height)
		return self

	def setMaximumSize(self, Width, Height):
		super().setMaximumSize(Width ,Height)
		return self

	def setMinimumSize(self, Width, Height):
		super().setMinimumSize(Width ,Height)
		return self

	def setSizePolicy(self, Policy):
		super().setSizePolicy(Policy)
		return self

	def setCentralWidget(self, Widget):
		super().setCentralWidget(Widget)
		return self

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def move(self, X, Y):
		super().move(X, Y)
		return self

	def showNormal(self):
		super().showNormal()
		return self

	def showMaximized(self):
		super().showMaximized()
		return self

	def showFullScreen(self):
		super().showFullScreen()
		return self

	def setWindowFlags(self, Flags):
		super().setWindowFlags(Flags)
		return self

class RW_Tree_Widget(QTreeWidget):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Tree")

		super().setHeaderHidden(True)

	def setStyleSheet(self, Style: str):
		super().setStyleSheet(Style)
		return self

	def setContentsMargins(self, L: int, T: int, R: int, B: int):
		super().setContentsMargins(L,T,R,B)
		return self

	def setMargins(self, Margins: int):
		super().setContentsMargins(Margins,Margins,Margins,Margins)
		return self

	def setHeaderHidden(self, Status: bool):
		super().setHeaderHidden(Status)
		return self

	def setFont(self, Font:QFont):
		super().setFont(Font)
		return self

	def setColumnCount(self, Count: int):
		super().setColumnCount(Count)
		return self

	def setVerticalScrollBar(self, Scrollbar: QScrollBar):
		super().setVerticalScrollBar(Scrollbar)
		return self

	def setHorizontalScrollBar(self, Scrollbar: QScrollBar):
		super().setHorizontalScrollBar(Scrollbar)
		return self

	def setVerticalScrollBarPolicy(self, Policy: Qt.ScrollBarPolicy):
		super().setVerticalScrollBarPolicy(Policy)
		return self

	def setHorizontalScrollBarPolicy(self, Policy: Qt.ScrollBarPolicy):
		super().setHorizontalScrollBarPolicy(Policy)
		return self

	def setArea(self, H_V: str, Scrollbar:QScrollBar):
		if H_V == "H":
			super().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
			super().setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
			self.setHorizontalScrollBar(Scrollbar)
		elif H_V == "V":
			super().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
			super().setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
			self.setVerticalScrollBar(Scrollbar)
		return self

	def setLayout(self, Layout):
		super().setLayout(Layout)
		return self

	def setFixedWidth(self, Width: int):
		super().setFixedWidth(Width)
		return self

	def setFixedHeight(self, Height: int):
		super().setFixedHeight(Height)
		return self

class RW_Toolbar(QMenuBar):
	def __init__(self):
		super().__init__()
		super().setObjectName("Default_Toolbar")

		super().setContentsMargins(0,0,0,0)

	def addMenu(self, Menu: QMenu):
		super().addMenu(Menu)
		return self

class RCW_Float_Input_Slider(RW_Linear_Contents):
	def __init__(self, Label = "Value", Min = 0, Max = 10, offset = 10):
		super().__init__(False)
		self.setFixedHeight(25)
		self.Offset = offset

		self.Label = RW_Button().setText(Label)
		self.Input = RCW_Float_Slider(Min, Max, self.Offset)
		self.Line = RW_Line_Editor().setValidator(QDoubleValidator(Min, Max, 5))
		self.Popup_Line = RW_Menu().setLayout(RW_Linear_Layout(False).addWidget(self.Line))

		self.addWidget(self.Label).addWidget(self.Input).setStretch({0:1,1:1})

		self.Label.clicked.connect(self.textEdit)
		self.Line.textChanged.connect(self.updateSlider)
		self.Line.returnPressed.connect(self.updateText)

	def setValue(self, Value = 0):
		self.Input.setValue(float(Value * self.Offset))
		return self

	def updateSlider(self):
		self.Input.setValue(float(self.Line.text()) * self.Offset)

	def textEdit(self):
		self.Line.setText(str(self.Input.value() / self.Offset))
		self.Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Line.selectAll().setFocus()
		self.Popup_Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Popup_Line.exec(self.mapToGlobal(self.Input.pos()))

	def updateText(self):
		self.Popup_Line.close()

class RCW_Float_Slider(RW_Slider):
	def __init__(self, Min = 0, Max = 100, offset = 10):
		super().__init__()
		self.Offset = offset
		self.setRange(Min * self.Offset, Max * self.Offset)

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.LeftButton and not self.isSliderDown():
			Option = QStyleOptionSlider()
			self.initStyleOption(Option)
			Slider_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderHandle, self)
			if event.pos() not in Slider_Size.getCoords():
				Handle_Size = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, Option, QStyle.SubControl.SC_SliderGroove, self)
				Center = Slider_Size.center() - Slider_Size.topLeft()
				Pos = event.pos() - Center
				Length = Slider_Size.width()
				Min = Handle_Size.x()
				Max = Handle_Size.right() - Length + 1
				Pos = Pos.x()
				Value = self.style().sliderValueFromPosition( self.minimum(), self.maximum(), Pos - Min, Max - Min)
				self.setSliderPosition(Value)
		super().mousePressEvent(event)

	def paintEvent(self, event):
		QSlider.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		if self.Offset == 1:
			painterPath.addText(QPointF(self.geometry().width() / 2 - QFontMetrics(self.font()).horizontalAdvance(str(self.value())) / 2, self.geometry().height() * 0.75), self.font() , "{:,}".format(self.value()).replace(',','\''))
		else:
			painterPath.addText(QPointF(self.geometry().width() / 2 - QFontMetrics(self.font()).horizontalAdvance(str(self.value())) / 2, self.geometry().height() * 0.75), self.font() , "{:,}".format(self.value() / self.Offset).replace(',','\''))
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))