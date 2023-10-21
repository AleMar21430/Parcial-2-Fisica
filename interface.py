from qt import *
from math import *
import time

global charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y
charge_Q = 1.60217    # e-19
charge_q = 1.60217    # e-19
mass     = 9.10938    # e-37
velocity = 299792458/3# m/s
angle = 0             # deg
velocity_x = velocity # m/s
velocity_y = 0        # m/s
pos_x = -500          # nm
pos_y = 0             # nm

class Simulation_Thread(QThread):
	gui_update = Signal(float, float, float, float, float)
	def __init__(self, Q, q, m, px, py, vx, vy, v):
		super().__init__()
		self.simulate = True
		self.step = 0
		self.charge_Q = Q
		self.charge_q = q
		self.mass = m
		self.pos_x = px / 1e9 # nm to m
		self.pos_y = py / 1e9 # nm to m
		self.velocity_x = vx
		self.velocity_y = vy
		self.velocity = v
		self.time_delta = 1e-18

	def stop(self):
		self.simulate = False

	def run(self):
		delta = 15
		while self.simulate:
			start_time = time.time()
			k            = eval(f"8.98755e{9-delta}")            # e 9
			sim_charge_Q = eval(f"{self.charge_Q}e{-19+delta}")  # e-19
			sim_charge_q = eval(f"{self.charge_q}e{-19+delta}")  # e-19
			sim_mass     = eval(f"{mass}e{-37+delta}")           # e-37

			r = sqrt(self.pos_x ** 2 + self.pos_y ** 2)
			F_electric = (k * sim_charge_q * sim_charge_Q) / r**2
			Fx = F_electric * (self.pos_x  / r)
			Fy = F_electric * (self.pos_y / r)
			ax = Fx / sim_mass
			ay = Fy / sim_mass

			self.velocity_x += ax * self.time_delta
			self.velocity_y += ay * self.time_delta

			self.pos_x += self.velocity_x * self.time_delta
			self.pos_y += self.velocity_y * self.time_delta

			self.velocity = sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

			self.step += 1
			if self.step % 30 >= 29:
				self.gui_update.emit(self.pos_x * 1e9, -self.pos_y * 1e9, self.velocity_x, -self.velocity_y, self.velocity)
				end_time = time.time()
				elapsed_time = end_time - start_time
				if elapsed_time < 0.025:
					time.sleep(0.025 - elapsed_time)

class R_Image_Canvas_Scene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		self.point_charge = Point_Charge()
		self.line_charge = Line_Charge()
		self.plane_charge = Plane_Charge()
		self.particle = Particle()
		self.addItem(self.point_charge)
		self.addItem(self.particle)
		self.addRect(QRect(-1000,-400,1500,800))

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

		self.args = [charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y]

	def simulate(self):
		self.simulation_thread = Simulation_Thread(charge_Q, charge_q, mass, pos_x, pos_y, velocity_x, velocity_y, velocity)
		self.simulation_thread.gui_update.connect(self.thread_update)
		self.simulation_thread.start()

	def thread_update(self, px, py, vx, vy, v):
		global pos_x, pos_y, velocity_x, velocity_y, velocity
		pos_x = px
		pos_y = py
		velocity_x = vx
		velocity_y = vy
		velocity = v
		self.Scene.particle.setPos(pos_x, pos_y)
		self.update()

	def restart(self):
		try:
			self.simulation_thread.stop()
			self.simulation_thread.quit()
		except: pass
		global charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y
		time.sleep(0.2)
		charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y = self.args
		self.Tools.Particle_velocity.setValue(velocity)
		self.Tools.Particle_x_pos.setValue(pos_x)
		self.Tools.Particle_y_pos.setValue(pos_y)
		self.Tools.Static_charge.setValue(charge_Q)
		self.Scene.particle.setPos(pos_x, -pos_y)
		self.update()

class R_Toolbar(RW_Linear_Contents):
	def __init__(self, parent: R_Workspace_Image_Canvas):
		super().__init__(True)
		self.Parent = parent

		self.Particle_mass = RCW_Float_Input_Slider("Masa x 10⁻³⁷kg", 0, 1000, 1e5).setValue(mass)
		self.Particle_charge = RCW_Float_Input_Slider("Carga x 10⁻¹⁹C", 0, 100, 1e5).setValue(charge_q)
		self.Particle_velocity = RCW_Float_Input_Slider("Velocidad m/s", 1, 299792458, 1).setValue(velocity)
		self.Particle_x_pos = RCW_Float_Input_Slider("X nm", -1000, -25, 1e4).setValue(pos_x)
		self.Particle_y_pos = RCW_Float_Input_Slider("Y nm", -300, 300, 1e4).setValue(pos_y)
		self.Particle_theta = RCW_Float_Input_Slider("θ °", -45, 45, 10).setValue(angle)

		self.Use_Point = RW_Button()
		self.Use_Line = RW_Button()
		self.Use_Plane = RW_Button()

		self.Static_charge = RCW_Float_Input_Slider("Densidad / Carga", 0, 100, 1e5).setValue(charge_Q)

		self.Start_Simulation = RW_Button()
		self.Restart_Simulation = RW_Button()

		self.Use_Point.setText("Carga Puntual")
		self.Use_Line.setText("Linea Infinita")
		self.Use_Plane.setText("Plano Infinito")

		self.Start_Simulation.setText("Iniciar Simulación")
		self.Restart_Simulation.setText("Reiniciar Simulación")

		self.Linear_Layout.addWidget(self.Particle_charge)
		self.Linear_Layout.addWidget(self.Particle_mass)
		self.Linear_Layout.addWidget(self.Particle_velocity)
		self.Linear_Layout.addWidget(self.Particle_x_pos)
		self.Linear_Layout.addWidget(self.Particle_y_pos)
		self.Linear_Layout.addWidget(self.Particle_theta)

		self.Linear_Layout.addWidget(self.Use_Point)
		self.Linear_Layout.addWidget(self.Use_Line)
		self.Linear_Layout.addWidget(self.Use_Plane)

		self.Linear_Layout.addWidget(self.Static_charge)

		self.Linear_Layout.addWidget(self.Start_Simulation)
		self.Linear_Layout.addWidget(self.Restart_Simulation)

		self.Particle_charge.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_mass.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_velocity.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_x_pos.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_y_pos.Input.valueChanged.connect(self.updateSimulationValues)
		self.Particle_theta.Input.valueChanged.connect(self.updateSimulationValues)
		self.Static_charge.Input.valueChanged.connect(self.updateSimulationValues)

		self.Use_Point.clicked.connect(self.usePointCharge)
		self.Use_Line.clicked.connect(self.useLineCharge)
		self.Use_Plane.clicked.connect(self.usePlaneCharge)

		self.Start_Simulation.clicked.connect(self.simulate)
		self.Restart_Simulation.clicked.connect(self.Parent.restart)

	def simulate(self):
		self.Parent.args = [charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y]
		self.Parent.simulate()

	def updateSimulationValues(self):
		global charge_Q, charge_q, mass, velocity_x, velocity_y, pos_x, pos_y, velocity, angle
		angle = -self.Particle_theta.Input.value()/10
		angle_rad = radians(angle)

		charge_Q = self.Static_charge.Input.value() / 1e5
		charge_q = self.Particle_charge.Input.value() / 1e5
		mass = self.Particle_mass.Input.value() / 1e5
		velocity = self.Particle_velocity.Input.value()
		velocity_x = cos(angle_rad) * velocity
		velocity_y = sin(angle_rad) * velocity
		pos_x = self.Particle_x_pos.Input.value() / 1e4
		pos_y = self.Particle_y_pos.Input.value() / 1e4
		self.Parent.Scene.particle.setPos(pos_x, -pos_y)
		self.Parent.args = [charge_Q, charge_q, mass, velocity, angle, velocity_x, velocity_y, pos_x, pos_y]
		self.Parent.Viewport.update()

	def usePointCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.point_charge = Point_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.point_charge)
		self.Parent.Scene.addRect(QRect(-1000,-400,1500,800))
		self.updateSimulationValues()
		
	def useLineCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.line_charge = Line_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.line_charge)
		self.Parent.Scene.addRect(QRect(-1000,-400,1500,800))
		self.updateSimulationValues()
		
	def usePlaneCharge(self):
		self.Parent.Scene.clear()
		self.Parent.Scene.plane_charge = Plane_Charge()
		self.Parent.Scene.particle = Particle()
		self.Parent.Scene.addItem(self.Parent.Scene.particle)
		self.Parent.Scene.addItem(self.Parent.Scene.plane_charge)
		self.Parent.Scene.addRect(QRect(-1000,-400,1500,800))
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
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() - 20), f"Q = {charge_Q} x 10⁻¹⁹C")
		super().paint(painter, option, widget)

class Line_Charge(QGraphicsLineItem):
	def __init__(self):
		super().__init__(0, -300, 0, 300)
		self.setPen(QPen(Qt.GlobalColor.green,3))

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() - 20), f"Q = {charge_Q} x 10⁻¹⁹C")
		super().paint(painter, option, widget)

class Plane_Charge(QGraphicsLineItem):
	def __init__(self):
		super().__init__(0, -300, 0, 300)
		self.setPen(QPen(Qt.GlobalColor.blue,3))

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() - 20), f"Q = {charge_Q} x 10⁻¹⁹C")
		super().paint(painter, option, widget)

class Particle(QGraphicsEllipseItem):
	def __init__(self):
		super().__init__(-4, -4, 8, 8)

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.GlobalColor.white, 2))
		painter.setBrush(QBrush(Qt.GlobalColor.white))
		dot_radius = 2

		c = '{:,}'.format(charge_q).replace(',','\'')
		x = '{:,}'.format(self.pos().x()).replace(',','\'')
		y = '{:,}'.format(-self.pos().y()).replace(',','\'')
		m = '{:,}'.format(mass).replace(',','\'')
		v = '{:,}'.format(round(velocity)).replace(',','\'')
		vx = '{:,}'.format(round(velocity_x,2)).replace(',','\'')
		vy = '{:,}'.format(round(velocity_y,2)).replace(',','\'')
		theta = round(angle, 2)

		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 40),
			f"[ {x}nm , {y}nm ]"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 60),
			f"θ = {theta}°"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 80),
			f"m = {m} x 10⁻³⁷kg"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 100),
			f"q = {c} x 10⁻¹⁹C"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 120),
			f"[ {vx} | {vy} ]"
		)
		painter.drawText(QPointF(self.mapFromScene(0,0).x() + 20, self.mapFromScene(0,0).y() + 140),
			f"v = {v} m/s"
		)

		vector = QLineF(self.mapFromScene(self.pos()), self.mapFromScene(self.pos()) + QPointF(velocity** 0.3, 0))
		vector.setAngle(degrees(atan2(velocity_y, velocity_x)))
		painter.setPen(QPen(Qt.GlobalColor.magenta, 2))
		painter.drawLine(vector.p1(), vector.p2())
		painter.drawEllipse(self.mapFromScene(self.pos()) , dot_radius * 2, dot_radius * 2)
		super().paint(painter, option, widget)