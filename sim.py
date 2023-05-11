# Импорт всех классов
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.lang import Builder #слайдер
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
from math import cos, sin
# Импорт всех классов
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


from kivy.lang import Builder #слайдер
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy.graphics import (Color, Ellipse, Rectangle, Line)

from math import sin, cos, asin, acos, atan, pi, e, sqrt, radians

# Глобальные настройки
Window.size = (1500, 900)
Window.clearcolor = (255/255, 186/255, 3/255, 1)
Window.title = "Симулятор"
Window.dpi = 254

def gen(sigma, p, fi, n, scale = 50000):
	l = 0.0002
	g = 9.81

	delta = radians(5)

	point_x = [0.0, 0.00001]
	point_y = [0.0, -0.0000001]

	"""start_angle = atan(abs(point_y[0] - point_y[1]) / abs(point_x[1] - point_x[0]))
	for i in range(2, n):
		Ft = sigma
		P = p * g * (abs(point_y[i - 1] - point_y[0]) + 0.0001)
		F = P * l
		teta = atan((point_y[i - 2] - point_y[i - 1]) / (point_x[i - 1] - point_x[i - 2]))
		
		if teta < 0:
			teta = teta + pi
		if teta > 0:
			if fi < pi / 2:
				if fi + delta < teta < fi + delta:
					break
		else:
			teta = teta + pi
			if teta < pi - fi + delta:
				break
		
		#print(teta, F,)
		alpha = asin(min(F / (2 * Ft), 1))
		point_x.append(point_x[i - 1] + l * cos(teta + alpha))
		point_y.append(point_y[i - 1] - l * sin(teta + alpha))"""

	start_angle = atan(abs(point_y[0] - point_y[1]) / abs(point_x[1] - point_x[0]))
	for i in range(2, 10000000):
		Ft = sigma
		P = p * g * (abs(point_y[i - 1] - point_y[0]) + 0.0001)
		F = P * l
		teta = atan((point_y[i - 2] - point_y[i - 1]) / (point_x[i - 1] - point_x[i - 2]))
		if teta < 0:
			if abs(teta) < pi - fi + delta:
				break
			teta = teta + pi
		else:
			if fi < pi / 2:
				if fi - delta < teta < fi + delta:
					break
		alpha = asin(F / (2 * Ft))
		point_x.append(point_x[i - 1] + l * cos(teta + alpha))
		point_y.append(point_y[i - 1] - l * sin(teta + alpha))

		if teta < start_angle:
			break
	
	ans = []
	for i in range(0, len(point_x)):
		ans.append(point_x[i] * scale)
		ans.append((point_y[i] + abs(point_y[0] - point_y[-1])) * scale)
	
	return ans

class PainterWidget(Widget):
	def __init__(self, sigma, p, fi, n, **kwargs):
		super(PainterWidget, self).__init__(**kwargs)

		with self.canvas:
			self.color = Color(0, 0, 1, 1)
			self.line = Line(points=(), width=5, close=False)

		self.sigma = sigma
		self.p = p
		self.fi = fi
		self.n = n
		self.generate()
	
	def generate(self):
		poin = gen(sigma=self.sigma, p=self.p, fi=self.fi, n=self.n)
		self.line.points = poin

		

class MyApp(App):
	
	# Создание всех виджетов (объектов)
	def __init__(self):
		super().__init__()

	# Основной метод для построения программы
	def build(self):
		box = Widget()

		self.input_sigma = TextInput(hint_text='k пов натяжения', multiline=False, pos=(300, 0), size=(200, 100))
		self.input_p = TextInput(hint_text='плотность', multiline=False, pos=(600, 0), size=(200, 100))
		self.input_fi = TextInput(hint_text='fi', multiline=False, pos=(900, 0), size=(200, 100))
		self.input_n = TextInput(hint_text='n', multiline=False, pos=(1200, 0), size=(200, 100))

		self.input_sigma.bind(text=self.on_text_sigma) # Добавляем обработчик события
		self.input_p.bind(text=self.on_text_p) # Добавляем обработчик события
		self.input_fi.bind(text=self.on_text_fi) # Добавляем обработчик события
		self.input_n.bind(text=self.on_text_n) # Добавляем обработчик события

		sigma = 0.073
		p = 1000
		fi = pi
		n = 10000000

		self.sim = PainterWidget(sigma=sigma, p=p, fi=fi, n=n)

		self.input_sigma.text = str(sigma)
		self.input_p.text = str(p)
		self.input_fi.text = str(fi)
		self.input_n.text = str(n)

		box.add_widget(self.input_sigma)
		box.add_widget(self.input_p)
		box.add_widget(self.input_fi)
		box.add_widget(self.input_n)

		box.add_widget(self.sim)
		box.add_widget(Button(text="Очистить", on_press=self.clear_canvas, size=(200, 100)))
		
		return box
	
	# Получаем данные и производит их конвертацию
	def on_text_sigma(self, *args):
		while True:
			try: 
				self.sim.sigma = float(self.input_sigma.text)
				break
			except ...:
				pass
		self.sim.generate()
	
	# Получаем данные и производит их конвертацию
	def on_text_p(self, *args):
		while True:
			try: 
				self.sim.p = float(self.input_p.text)
				break
			except ...:
				pass
		self.sim.generate()
	
	# Получаем данные и производит их конвертацию
	def on_text_fi(self, *args):
		while True:
			try:
				self.sim.fi = float(self.input_fi.text)
				break
			except ...:
				pass
		self.sim.generate()
	
	# Получаем данные и производит их конвертацию
	def on_text_n(self, *args):
		while True:
			try:
				self.sim.n = int(self.input_n.text)
				break
			except ...:
				pass
		self.sim.generate()

	def clear_canvas(self, inst):
		self.sim.line.points = ()
		self.sim.generate()


# Запуск проекта
if __name__ == "__main__":
	MyApp().run()