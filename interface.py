from qt import *
from math import *
import numpy as np
def electric_potential(x, y, x1, y1, x2, y2, Q):
	k = 8.9875e9  # Coulomb's constant in N m²/C²

	def integrand(t):
		dx = x2 - x1
		dy = y2 - y1
		r = np.sqrt((x - (x1 + dx * t))**2 + (y - (y1 + dy * t))**2)
		return Q / r

	# Numerical integration using the trapezoidal rule
	segments = 1000  # Increase this for higher accuracy
	t_values = np.linspace(0, 1, segments)
	dt = 1 / segments
	integral = np.sum(integrand(t_values[:-1]) + integrand(t_values[1:])) * 0.5 * dt

	return k * integral

def electric_field_direction_at_point(x1, y1, x, y):
	dx = x1 - x
	dy = y1 - y
	length = sqrt(dx**2 + dy**2)
	if length == 0: length = 0.000001
	return (dx/length), (dy/length)

def electric_field_direction(x1, y1, x2, y2, x, y):
	e1_x, e1_y, = electric_field_direction_at_point(x1, y1, x, y)
	e2_x, e2_y, = electric_field_direction_at_point(x2, y2, x, y)
	mix1, mix2 = (e1_x + e2_x) / 2, (e1_y + e2_y) / 2
	length = sqrt(mix1**2 + mix2**2)
	if length == 0: length = 0.000001
	mix1 = (mix1/length)
	mix2 = (mix2/length)
	return mix1, mix2

class R_Image_Canvas_Scene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		
		self.point1 = MovablePoint(0, 0, 0)
		self.point2 = MovablePoint(0, 0, 0)
		self.line_charge = Line_Charge(0,0,0,0)

		self.addItem(self.line_charge)
		self.addItem(self.point1)
		self.addItem(self.point2)
		
		measure_item = Measure(0,0)
		self.addItem(measure_item)

class R_Workspace_Image_Canvas (RUI_Linear_Contents):
	def __init__(self, Log: RUI_Text_Stream):
		super().__init__("_Container",True)
		self.Log = Log

		global Q
		Q, ok = QInputDialog.getDouble(self, "Carga Q", "Carga Q:", 0.000001, decimals=10)

		self.Scene = R_Image_Canvas_Scene()
		self.Viewport = R_Image_Canvas_Viewport()
		self.Viewport.setScene(self.Scene)

		self.Layout.addWidget(self.Viewport)

class R_Image_Canvas_Viewport(RUI_Graphics_Viewport):
	BG_Color = QColor(25,25,25)
	Grid_Small = QPen(QColor(50, 50, 50), 0.5)
	Gird_Large = QPen(QColor(75, 75, 75), 0.75)
	Grid_Size = 100
	Grid_Subdivisions = int(Grid_Size / 10)
	item = None

	def __init__(self):
		super().__init__()
		self.Last_Pos_Pan = QPoint(0,0)
		self.Last_Pos_Move = QPoint(0,0)
		self.Moving_Item = False
		self.Selecting_Item = False
		self.Panning_View = False

	def drawBackground(self, painter, rect):
		painter.fillRect(rect, self.BG_Color)

		left = int(rect.left()) - (int(rect.left()) % self.Grid_Subdivisions)
		top = int(rect.top()) - (int(rect.top()) % self.Grid_Subdivisions)

		gridLines = []
		painter.setPen(self.Grid_Small)
		y = float(top)
		while y < float(rect.bottom()):
			gridLines.append(QLineF(rect.left(), y, rect.right(), y))
			y += self.Grid_Subdivisions
		painter.drawLines(gridLines)

		gridLines = []
		painter.setPen(self.Grid_Small)
		x = float(left)
		while x < float(rect.right()):
			gridLines.append(QLineF(x, rect.top(), x, rect.bottom()))
			x += self.Grid_Subdivisions
		painter.drawLines(gridLines)

		left = int(rect.left()) - (int(rect.left()) % self.Grid_Size)
		top = int(rect.top()) - (int(rect.top()) % self.Grid_Size)

		gridLines = []
		painter.setPen(self.Gird_Large)
		x = left
		while x < rect.right():
			gridLines.append(QLineF(x, rect.top(), x, rect.bottom()))
			x += self.Grid_Size
		painter.drawLines(gridLines)

		gridLines = []
		painter.setPen(self.Gird_Large)
		y = top
		while y < rect.bottom():
			gridLines.append(QLineF(rect.left(), y, rect.right(), y))
			y += self.Grid_Size
		painter.drawLines(gridLines)

		return super().drawBackground(painter, rect)

	def wheelEvent(self, event: QWheelEvent):
		zoomInFactor = 1.25
		zoomOutFactor = 1 / zoomInFactor
		oldPos = self.mapToScene(event.position().toPoint())
		if event.angleDelta().y() > 0:
			zoomFactor = zoomInFactor
		else:
			zoomFactor = zoomOutFactor

		currentScale = self.transform().m11()
		if zoomFactor * currentScale > 100.0:
			zoomFactor = 100.0 / currentScale
		elif zoomFactor * currentScale < 0.005:
			zoomFactor = 0.005 / currentScale

		self.scale(zoomFactor, zoomFactor)
		newPos = self.mapToScene(event.position().toPoint())
		delta = newPos - oldPos
		self.translate(delta.x(), delta.y())

	def mousePressEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.MiddleButton or event.button() == Qt.MouseButton.MiddleButton:
			self.Panning_View = True
			self.Last_Pos_Pan = event.pos()
		elif event.button() == Qt.MouseButton.LeftButton:
			self.Moving_Item = True
			self.item = self.itemAt(event.pos())
			self.Last_Pos_Move = event.pos()
		elif event.button() == Qt.MouseButton.RightButton:
			self.Moving_Item = True
			measure_item = Measure(0,0)
			self.scene().addItem(measure_item)

			self.item = measure_item
			self.Last_Pos_Move = event.pos()


	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.MiddleButton or event.button() == Qt.MouseButton.MiddleButton:
			self.Panning_View = False
		elif event.button() == Qt.MouseButton.LeftButton:
			self.Moving_Item = False
		elif event.button() == Qt.MouseButton.RightButton:
			self.Moving_Item = False

	def mouseMoveEvent(self, event: QMoveEvent):
		if self.Moving_Item and (type(self.item) == MovablePoint or type(self.item) == Measure):
			delta = (event.pos() - self.Last_Pos_Move) / self.transform().m11()
			self.item.setPos(self.item.pos().toPoint() + delta)
			self.Last_Pos_Move = event.pos()
			self.scene().line_charge.setLine(QLineF(self.scene().point1.pos().x(), self.scene().point1.pos().y(), self.scene().point2.pos().x(), self.scene().point2.pos().y()))

			for item in self.scene().items():
				if type(item) == Measure:
					x, y = electric_field_direction(
						self.scene().point1.pos().x(),
						self.scene().point1.pos().y(),
						self.scene().point2.pos().x(),
						self.scene().point2.pos().y(),
						item.pos().x(),
						item.pos().y()
					)
					angle_degrees = degrees(atan2(x, y))
					potential = electric_potential(
						item.pos().x(),
						item.pos().y(),
						self.scene().point1.pos().x(),
						self.scene().point1.pos().y(),
						self.scene().point2.pos().x(),
						self.scene().point2.pos().y(),
						Q
					)
					item.setVector(potential, angle_degrees)

		elif self.Panning_View:
			delta = (event.pos() - self.Last_Pos_Pan)
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
			self.Last_Pos_Pan = event.pos()

		else: super().mouseMoveEvent(event)
		self.scene().update()

class MovablePoint(QGraphicsEllipseItem):
	def __init__(self, x, y, yoffset):
		super().__init__(x - 4, y - 4, 8, 8)
		self.offset = yoffset
		self.setBrush(Qt.GlobalColor.blue)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))

		painter.drawText(QPointF(self.mapFromScene(self.pos()).x() + 10, self.mapFromScene(self.pos()).y() + 10 + self.offset), f"{round(self.pos().x(),2)}x {round(self.pos().y(),2)}y")

		super().paint(painter, option, widget)


class Line_Charge(QGraphicsLineItem):
	def __init__(self, x1, y1, x2, y2):
		super().__init__(x1, y1, x2, y2)
		self.setPen(QPen(Qt.GlobalColor.green,3))

class Measure(QGraphicsEllipseItem):
	def __init__(self, x, y):
		super().__init__(x - 4, y - 4, 8, 8)
		self.vector = QLineF(self.pos(), self.pos() + QPointF(50, 0))
		self.angle_degrees = 0.0
		self.length = 1.0

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		dot_radius = 2

		painter.drawText(QPointF(self.mapFromScene(self.pos()).x() + 10, self.mapFromScene(self.pos()).y() + 10), f"{round(self.pos().x(),2)}x {round(self.pos().y(),2)}y   {round(self.angle_degrees,2)}deg. {round(self.length,5)}V")

		painter.setPen(QPen(Qt.GlobalColor.red, 2))
		painter.drawLine(self.vector.p1(), self.vector.p2())
		painter.drawEllipse(self.mapFromScene(self.pos()) , dot_radius * 2, dot_radius * 2)

		super().paint(painter, option, widget)

	def setVector(self, length, angle_degrees):
		self.vector = QLineF(self.mapFromScene(self.pos()), self.mapFromScene(self.pos()) + QPointF(length, 0))
		self.vector.setAngle(angle_degrees + 90)
		self.length = length
		self.angle_degrees = angle_degrees
		self.update()