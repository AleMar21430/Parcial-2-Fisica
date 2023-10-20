from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import *

class RUI_Application (QApplication):
	def __init__(self, Args):
		super().__init__(Args)

class RUI_Button (QPushButton):
	def __init__(self, Style: str = "_Default_Button"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

class RUI_Dock (QDockWidget):
	def __init__(self, Style: str = "_Default_Dock"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

class RUI_Floating_Toggle (QPushButton):
	def __init__(self, Style: str = "_Default_Floating_Toggle"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint| Qt.WindowType.WindowStaysOnTopHint)

		self.setCheckable(True)
		self.setChecked(False)
		self.Drag_Pos = QPoint(0,0)

	def mousePressEvent(self, Event: QMouseEvent):
		if Event.button() == Qt.MouseButton.RightButton:
			self.Drag_Pos = Event.pos()
		super().mousePressEvent(Event)

	def mouseMoveEvent(self, Event: QMouseEvent): 
		if Event.buttons() & Qt.MouseButton.RightButton:
			self.move(self.mapToParent(Event.pos() - self.Drag_Pos))
		super().mouseMoveEvent(Event)

class RUI_File_Browser (QFileDialog):
	def __init__(self, Style: str = "_Default_File_Browser"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

class RUI_Grid_Layout (QGridLayout):
	def __init__(self, Style: str = "_Default_Grid_Layout"):
		super().__init__()
		self.setObjectName(Style)
		self.setContentsMargins(1,1,1,1)
		self.setSpacing(1)

class RUI_Image (QPixmap):
	def __init__(self, File = None):
		Reader = QImageReader(File)
		Reader.setAllocationLimit(1024)
		super().__init__(QPixmap.fromImageReader(Reader))

class RUI_Label (QLabel):
	def __init__(self, Style: str = "_Default_Label"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setScaledContents(True)

class RUI_Linear_Layout (QBoxLayout):
	def __init__(self, Vertical: bool = True, Margins: int = 1):
		if Vertical:
			super().__init__(QBoxLayout.Direction.TopToBottom)
			self.setAlignment(Qt.AlignmentFlag.AlignTop)
		else:
			super().__init__(QBoxLayout.Direction.LeftToRight)
			self.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.setContentsMargins(Margins,Margins,Margins,Margins)
		self.setSpacing(1)

	def clear(self):
		for i in range(self.count()):
			self.itemAt(i).widget().hide()
			self.itemAt(i).widget().deleteLater()
		return self

class RUI_Linear_Contents (QWidget):
	def __init__(self, Style: str = "_Default_Linear_Contents", Vertical: bool = True, Margins: int = 1):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setAttribute(Qt.WidgetAttribute.WA_StyleSheetTarget)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

		self.Layout = RUI_Linear_Layout(Vertical, Margins)
		self.setLayout(self.Layout)

class RUI_List (QListWidget):
	def __init__(self, Style: str = "_Default_List"):
		super().__init__()

		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setAttribute(Qt.WidgetAttribute.WA_StyleSheetTarget)
		self.setObjectName(Style)
		self.verticalScrollBar().setSingleStep(10)
		self.setSpacing(1)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

class RUI_Main_Window (QMainWindow):
	def __init__(self, Style: str = "_Default_Main_Window"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)

		self.setDockNestingEnabled(True)
		self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.West)
		self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

class RUI_Menu (QMenu):
	def __init__(self, Style: str = "_Default_Menu", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.Layout = RUI_Linear_Layout(Vertical)
		self.setLayout(self.Layout)

class RUI_Option (QComboBox):
	def __init__(self, Style: str = "_Default_Option"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class RUI_Progress (QProgressBar):
	def __init__(self, Style: str = "_Default_Progress", Vertical: bool = False):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setTextVisible(False)
		if Vertical:
			self.setOrientation(Qt.Orientation.Vertical)
			self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
		else:
			self.setOrientation(Qt.Orientation.Horizontal)
			self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

	def paintEvent(self, event):
		QProgressBar.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		if self.value() != -1:
			painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , f"{self.value()}%")
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

class RUI_Scroll_Area (QScrollArea):
	def __init__(self, Style: str = "_Default_Scorll_Area", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		self.setWidgetResizable(True)

		self.Contents = RUI_Linear_Contents()
		self.setWidget(self.Contents)

class RUI_Slider (QSlider):
	def __init__(self, Style: str = "_Default_Slider", Vertical: bool = False):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		if Vertical: self.setOrientation(Qt.Orientation.Vertical)
		else: self.setOrientation(Qt.Orientation.Horizontal)

class RUI_Splitter (QSplitter):
	def __init__(self, Style: str = "_Default_Splitter", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		if Vertical: self.setOrientation(Qt.Orientation.Vertical)
		else: self.setOrientation(Qt.Orientation.Horizontal)

class RUI_Spreadsheet (QTableWidget):
	def __init__(self, Style: str = "_Default_Spreadsheet"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.horizontalHeader().setObjectName("_Horizontal")
		self.verticalHeader().setObjectName("_Vertical")

class RUI_Spreadsheet_Item (QTableWidgetItem):
	def __init__(self, Text: str = "Item"):
		super().__init__()

class RUI_Text_Stream (QTextBrowser):
	def __init__(self, Style: str = "_Default_Text_Stream"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

	def append(self, Text: str, Color: str = "255,255,255"):
		print(Text)
		super().append(f'<p style="color:rgb({Color})">{str(Text)}</p>')
		super().verticalScrollBar().setValue(super().verticalScrollBar().maximum())

	def appendPlain(self, Text: str):
		super().insertPlainText(Text)
		super().verticalScrollBar().setValue(super().verticalScrollBar().maximum())

class RUI_Tree (QTreeWidget):
	def __init__(self, Style: str = "_Default_Tree"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

		self.setHeaderHidden(True)

class RUI_Tree_Item (QTreeWidgetItem):
	def __init__(self, Parent: QTreeWidget | QTreeWidgetItem, Text: str = "Item"):
		super().__init__(Parent)
		self.setText(0, Text)

class RUI_Tab_Widget (QTabWidget):
	def __init__(self, Style: str = "_Default_Tab_Widget", Vertical: bool = True):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		if Vertical:
			self.setTabPosition(QTabWidget.TabPosition.North)
		else:
			self.setTabPosition(QTabWidget.TabPosition.West)

class RUI_Text_Input (QPlainTextEdit):
	def __init__(self, Style: str = "_Default_Text_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setTabStopDistance(40)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

class RUI_HTML_Input (QTextEdit):
	def __init__(self, Style: str = "_Default_Text_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

class RUI_Toggle (RUI_Button):
	def __init__(self, Style: str = "_Default_Button"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.setCheckable(True)
		self.setChecked(False)

class RUI_ToolBar (QToolBar):
	def __init__(self, Style: str = "_Default_Toolbar"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

		self.layout().setContentsMargins(1,1,1,1)
		self.layout().setSpacing(1)

		self.setFloatable(False)
		self.setMovable(False)
		self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
		self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

class RUI_Value_Input (QLineEdit):
	def __init__(self, Type: str = "str", Style: str = "_Default_Value_Input"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

		if Type == "int":
			self.Validator = QIntValidator()
			self.setValidator(self.Validator)
		elif Type == "float":
			self.Validator = QDoubleValidator()
			self.setValidator(self.Validator)

class RUI_Web_Viewer(QWebEngineView):
	def __init__(self, Style: str = "_Default_Webview"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class RUI_Widget (QWidget):
	def __init__(self, Style: str = "_Default_Widget"):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setObjectName(Style)
		self.setContentsMargins(0,0,0,0)
		self.setAcceptDrops(True)
		self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

class RUI_Toast(RUI_Menu):
	def __init__(self, Message = "Message", Position = "Center", color = "250,50,50"):
		super().__init__()
		Layout = RUI_Linear_Layout()
		Label = RUI_Label()
		Label.setText(Message)
		Layout.addWidget(Label)
		self.setLayout(Layout)
		self.setWindowTitle(Message)
		self.setStyleSheet(f"color:rgb({color}); font-size:26px; padding: 5px 10px 5px 10px;")
		self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.Popup)
		self.setFixedSize(Label.sizeHint())

		if type(Position) == str:
			Position = QPoint(960 - (Label.sizeHint().width()/2),1080 - (Label.sizeHint().height()*4))

		timer = QTimer()
		timer.timeout.connect(self.close)
		timer.start(1500)
		self.exec(Position)

class RUI_Graphics_Viewport (QGraphicsView):
	def __init__(self):
		super().__init__()
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
		self.setContentsMargins(0,0,0,0)
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

		self.setRenderHint(QPainter.RenderHint.Antialiasing)
		self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
		self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
		self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setMouseTracking(True)
		self.Panning_View = False
		self.currentScale = 1

	def wheelEvent(self, event: QWheelEvent):
		zoomFactor = 1.25
		
		oldPos = self.mapToScene(event.position().toPoint())
		if event.angleDelta().y() > 0:
			self.scale(zoomFactor, zoomFactor)
			self.currentScale *= zoomFactor
		elif self.currentScale > 0.1:
			self.scale(1/zoomFactor, 1/zoomFactor)
			self.currentScale /= zoomFactor
		
		newPos = self.mapToScene(event.position().toPoint())
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = True
			self.lastPos = event.pos()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = False

	def mouseMoveEvent(self, event: QMoveEvent):
		if self.Panning_View:
			delta = (event.pos() - self.lastPos)
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
			self.lastPos = event.pos()
		else: super().mouseMoveEvent(event)

class RUI_Pair(RUI_Linear_Contents):
	def __init__(self, First: RUI_Widget, Second: RUI_Widget, Vertical: bool = False):
		super().__init__(Vertical = Vertical, Margins = 0)
		self.Layout.addWidget(First)
		self.Layout.addWidget(Second)
		self.Layout.setStretch(0,1)
		self.Layout.setStretch(1,1)

class RUI_Drop_Down(RUI_Linear_Contents):
	def __init__(self):
		super().__init__()
		Toggle = RUI_Toggle()
		self.Contents = RUI_Linear_Contents()
		self.Layout.addWidget(Toggle)
		self.Layout.addWidget(self.Contents)
		self.Contents.setFixedHeight(0)
		Toggle.clicked.connect(lambda Checked: self.expandCollapse(Checked))

	def expandCollapse(self, Checked):
		if (Checked):
			self.Contents.setFixedHeight(self.Contents.sizeHint().height())
		else:
			self.Contents.setFixedHeight(0)

class RUI_Input(RUI_Linear_Contents):
	def __init__(self, Widget: RUI_Widget, Title: str = "Value"):
		super().__init__(Vertical = True, Margins = 0)

		self.Label = RUI_Label("Label")
		self.Label.setText(Title)
		self.Layout.addWidget(self.Label)
		self.Layout.addWidget(Widget)

class RUI_Input_Slider(RUI_Linear_Contents):
	def __init__(self, Type = "int", Min = 0, Max = 10, Float_Decimals = 2):
		super().__init__(Vertical = True, Margins = 0)
		self.Type = Type

		Layout = RUI_Linear_Layout(False, 0)
		self.Popup_Line = RUI_Menu()
		self.Popup_Line.setLayout(Layout)

		if Type == "int":
			self.Line = RUI_Value_Input("int")
			self.Input = RUI_Int_Slider(self, Min, Max)
			self.Layout.addWidget(self.Input)
		else:
			self.Line = RUI_Value_Input("float")
			self.Input = RUI_Float_Slider(self, Float_Decimals, Min, Max)
			self.Layout.addWidget(self.Input)

		Layout.addWidget(self.Line)
		self.Line.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
		self.Line.textChanged.connect(self.updateSlider)
		self.Line.returnPressed.connect(self.updateText)

	def setValue(self, Value = 0):
		if self.Type == "int":
			self.Input.setValue(int(Value))
		else:
			self.Input.setValue(str(round(Value,2)))
		return self

	def updateSlider(self):
		if self.Type == "int":
			self.Input.setValue(int(self.Line.text()))
		else:
			self.Input.setValue(self.Line.text())

	def textEdit(self):
		if self.Type == "int":
			self.Line.setText(str(self.Input.value()))
		else:
			self.Line.setText(str(round(self.Input.value()/10**self.Input.Decimals,self.Input.Decimals)))
		self.Line.selectAll()
		self.Line.setFocus()
		self.Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Popup_Line.setFixedSize(self.Input.width(), self.Input.height())
		self.Popup_Line.exec(self.mapToGlobal(QPoint(self.Input.pos().x()-1,self.Input.pos().y()-1)))

	def updateText(self):
		self.Popup_Line.close()

	def value(self):
		if self.Type == "int":
			return self.Input.value()
		else:
			return round(self.Input.value()/10**self.Input.Decimals,self.Input.Decimals)

class RUI_Int_Slider(RUI_Slider):
	def __init__(self, Parent: RUI_Input_Slider, Min = 0, Max = 100):
		super().__init__()
		self.Parent = Parent
		self.setRange(Min,Max)

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.LeftButton:
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
		elif event.button() == Qt.MouseButton.RightButton and not self.isSliderDown():
			self.Parent.textEdit()

	def paintEvent(self, event):
		QSlider.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , str(self.value()))
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

	def wheelEvent(self, event: QWheelEvent):
		pass

class RUI_Float_Slider(RUI_Slider):
	def __init__(self, Parent: RUI_Input_Slider, Decimals = 2, Min = 0, Max = 10):
		super().__init__()
		self.Parent = Parent
		self.Decimals = Decimals
		self.Min = Min
		self.Max = Max

		self.setRange(Min*10**Decimals,Max*10**Decimals)

	def setValue(self, value):
		super().setValue(int(float(value)*10**self.Decimals))

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.LeftButton:
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
		elif event.button() == Qt.MouseButton.RightButton and not self.isSliderDown():
			self.Parent.textEdit()

	def paintEvent(self, event):
		QSlider.paintEvent(self, event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painterPath = QPainterPath()
		painterPath.addText(QPointF(13, self.geometry().height()/2 + QFontMetrics(self.font()).height()/2 - 3), self.font() , str(round(self.value()/10**self.Decimals, self.Decimals)))
		painter.strokePath(painterPath, QPen(QColor(0,0,0), 2.5))
		painter.fillPath(painterPath, QColor(250,250,250))

	def wheelEvent(self, event: QWheelEvent):
		pass