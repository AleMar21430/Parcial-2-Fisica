from qt import *
from math import *
import numpy as np

global charge_Q, charge_q, velocity, vector_x, vector_y, pos_x, pos_y
charge_Q = 1.60217
charge_q = 1.60217
velocity = 100000
vector_x = -1
vector_y = 0
pos_x = 500
pos_y = 0

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
		self.point_charge = Point_Charge()
		self.line_charge = Line_Charge()
		self.plane_charge = Plane_Charge()
		self.particle = Particle()
		self.addItem(self.particle)

class R_Workspace_Image_Canvas(RW_Splitter):
	def __init__(self, Log: RW_Text_Stream):
		super().__init__(False)
		self.Log = Log

		self.Scene = R_Image_Canvas_Scene()
		self.Viewport = R_Image_Canvas_Viewport()
		self.Viewport.setScene(self.Scene)
		self.Tools = R_Toolbar(self)

		self.addWidget(self.Tools)
		self.addWidget(self.Viewport)
		self.setSizes([500,1500])

		self.Tools.updateSimulationValues()
		self.Viewport.update()

class R_Toolbar(RW_Linear_Contents):
	def __init__(self, parent: R_Workspace_Image_Canvas):
		super().__init__(True)
		self.Parent = parent

		self.Particle_velocity = RCW_Float_Input_Slider("Velocidad m/s", 0, 299792458, 1).setValue(velocity)
		self.Particle_charge = RCW_Float_Input_Slider("Carga C x 10⁻¹⁹", 0, 100, 100000).setValue(charge_q)
		self.Particle_x_value = RCW_Float_Input_Slider("X cm", 1, 1000, 10).setValue(pos_x)
		self.Particle_y_value = RCW_Float_Input_Slider("Y cm", -250, 250, 10).setValue(pos_y)
		self.Particle_theta_value = RCW_Float_Input_Slider("θ °", -50, 50, 10)

		self.Use_Point = RW_Button()
		self.Use_Line = RW_Button()
		self.Use_Plane = RW_Button()

		self.Charge_value = RCW_Float_Input_Slider("Densidad / Carga", 0, 100, 100000).setValue(charge_Q)

		self.Restart_Simulation = RW_Button()

		self.Use_Point.setText("Carga Puntual")
		self.Use_Line.setText("Linea Infinita")
		self.Use_Plane.setText("Plano Infinito")

		self.Restart_Simulation.setText("Reiniciar Simulación")

		self.Linear_Layout.addWidget(self.Particle_velocity)
		self.Linear_Layout.addWidget(self.Particle_charge)
		self.Linear_Layout.addWidget(self.Particle_x_value)
		self.Linear_Layout.addWidget(self.Particle_y_value)
		self.Linear_Layout.addWidget(self.Particle_theta_value)

		self.Linear_Layout.addWidget(self.Use_Point)
		self.Linear_Layout.addWidget(self.Use_Line)
		self.Linear_Layout.addWidget(self.Use_Plane)

		self.Linear_Layout.addWidget(self.Charge_value)

		self.Linear_Layout.addWidget(self.Restart_Simulation)

		self.Particle_velocity.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_charge.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_x_value.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_y_value.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_theta_value.Input.valueChanged.connect(self.updateSimulationValues)
		self.Charge_value.Input.valueChanged.connect(self.updateSimulationValues)

		self.Use_Point.clicked.connect(self.usePointCharge)
		self.Use_Line.clicked.connect(self.useLineCharge)
		self.Use_Plane.clicked.connect(self.usePlaneCharge)

	def updateSimulationValues(self):
		global charge_Q, charge_q, velocity, vector_x, vector_y, pos_x, pos_y

		angle_theta = -self.Particle_theta_value.Input.value()/10 + 90
		angle_radians = radians(angle_theta)
		
		charge_Q = self.Charge_value.Input.value() / 100000
		charge_q = self.Particle_charge.Input.value() / 100000
		velocity = self.Particle_velocity.Input.value()
		vector_x = cos(angle_radians)
		vector_y = sin(angle_radians)
		pos_x = self.Particle_x_value.Input.value() / 10
		pos_y = self.Particle_y_value.Input.value() / 10

		self.Parent.Scene.particle.setPos(pos_x, -pos_y)
		self.Parent.Scene.particle.setVector(velocity, angle_theta)
		self.Parent.Viewport.update()

	def usePointCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.point_charge = Point_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.point_charge)
		self.updateSimulationValues()
		
	def useLineCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.line_charge = Line_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.line_charge)
		self.updateSimulationValues()
		
	def usePlaneCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.plane_charge = Plane_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.plane_charge)
		self.updateSimulationValues()


class R_Image_Canvas_Viewport(QGraphicsView):
	BG_Color = QColor(25,25,25)
	Grid_Small = QPen(QColor(50, 50, 50), 0.5)
	Gird_Large = QPen(QColor(75, 75, 75), 0.75)
	Grid_Size = 100
	Grid_Subdivisions = int(Grid_Size / 10)
	item = None

	def __init__(self):
		super().__init__()
		self.Last_Pos_Pan = QPoint(0,0)
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
		if event.button() == Qt.MouseButton.MiddleButton or event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = True
			self.Last_Pos_Pan = event.pos()

	def mouseReleaseEvent(self, event: QMouseEvent):
		if event.button() == Qt.MouseButton.MiddleButton or event.button() == Qt.MouseButton.LeftButton or event.button() == Qt.MouseButton.RightButton:
			self.Panning_View = False

	def mouseMoveEvent(self, event: QMoveEvent):
		if self.Panning_View:
			delta = (event.pos() - self.Last_Pos_Pan)
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
			self.Last_Pos_Pan = event.pos()

		else: super().mouseMoveEvent(event)
		self.scene().update()

class Point_Charge(QGraphicsEllipseItem):
	def __init__(self):
		super().__init__(-4, -4, 8, 8)
		self.setPen(QPen(Qt.GlobalColor.red,3))

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawText(QPointF(self.mapFromScene(0,0).x(), self.mapFromScene(0,0).y()+250), f"Q = {charge_Q} C x 10⁻¹⁹")
		super().paint(painter, option, widget)

class Line_Charge(QGraphicsLineItem):
	def __init__(self):
		super().__init__(0, -300, 0, 300)
		self.setPen(QPen(Qt.GlobalColor.green,3))

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawText(QPointF(self.mapFromScene(0,0).x(), self.mapFromScene(0,0).y()+250), f"Q = {charge_Q} C x 10⁻¹⁹")
		super().paint(painter, option, widget)

class Plane_Charge(QGraphicsLineItem):
	def __init__(self):
		super().__init__(0, -300, 0, 300)
		self.setPen(QPen(Qt.GlobalColor.blue,3))

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawText(QPointF(self.mapFromScene(0,0).x(), self.mapFromScene(0,0).y()+250), f"Q = {charge_Q} C x 10⁻¹⁹")
		super().paint(painter, option, widget)

class Particle(QGraphicsEllipseItem):
	def __init__(self):
		super().__init__(-4, -4, 8, 8)
		self.vector = QLineF(self.pos(), self.pos() + QPointF(50, 0))
		self.angle_degrees = 0.0

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		dot_radius = 2

		x = '{:,}'.format(round(self.pos().x(),1)).replace(',','\'')
		y = '{:,}'.format(-round(self.pos().y(),1)).replace(',','\'')
		theta = -round(self.angle_degrees -90,1)
		c = '{:,}'.format(charge_q).replace(',','\'')
		v = '{:,}'.format(velocity).replace(',','\'')

		painter.drawText(QPointF(self.mapFromScene(self.pos()).x() - 3, self.mapFromScene(self.pos()).y() + 20),
			f"x = {x}m | y = {y}m | θ = {theta}°"
		)
		painter.drawText(QPointF(self.mapFromScene(self.pos()).x() -3, self.mapFromScene(self.pos()).y() + 40),
			f"q = {c} C x 10⁻¹⁹ | v = {v}m/s"
		)

		painter.setPen(QPen(Qt.GlobalColor.magenta, 2))
		painter.drawLine(self.vector.p1(), self.vector.p2())
		painter.drawEllipse(self.mapFromScene(self.pos()) , dot_radius * 2, dot_radius * 2)

		super().paint(painter, option, widget)

	def setVector(self, length, angle_degrees):
		self.vector = QLineF(self.mapFromScene(self.pos()), self.mapFromScene(self.pos()) + QPointF(sqrt(sqrt(velocity)), 0))
		self.vector.setAngle(angle_degrees + 90)
		self.angle_degrees = angle_degrees
		self.update()