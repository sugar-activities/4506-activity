#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Main.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pygame, gc, sys, os, threading, random, gtk, pygtk
from pygame.locals import *

gc.enable()

RESOLUCION = (1200, 900)
BASE= os.path.dirname(__file__)
IMAGENES= os.path.join(BASE, "Imagenes/")
CANTOS= os.path.join(BASE, "Sonidos/")
# Sonidos de Insectos: http://mushinone.cool.ne.jp/English/ENGitiran.htm

import BiblioJAM
from BiblioJAM.JAMButton import JAMButton
from BiblioJAM.JAMLabel import JAMLabel
from BiblioJAM.JAMDialog import JAMDialog
import BiblioJAM.JAMGlobals as JAMG

def Traduce_posiciones(VA, VH):
	eventos= pygame.event.get(pygame.MOUSEBUTTONDOWN)
	for event in eventos:
		x, y = event.pos
		xx= x/VA
		yy= y/VH
		event_pos= (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos= event_pos, button=event.button)
		pygame.event.post(evt)

	eventos= pygame.event.get(pygame.MOUSEMOTION)
	for event in eventos:
		x, y = event.pos
		xx= x/VA
		yy= y/VH
		event_pos= (xx, yy)
	for event in eventos:
		evt = pygame.event.Event(pygame.MOUSEMOTION, pos= event_pos, rel=event.rel, buttons=event.buttons)
		pygame.event.post(evt)

class Main():
# Subprograma independiente Crustaceos
	def __init__(self, res):
		self.resolucionreal= res
		# Variables para JAMatrix
		self.ventana= None
		self.name= "CantaBichos"
		self.estado= False

		# Variables del Juego
		self.fondo= None
		self.reloj= None

		# Escalado
		self.ventana_real= None
		#self.resolucionreal= None
		self.VA= None
		self.VH= None

		self.preset()

		self.Bichos= None
		self.mensaje= None
		self.dialog= None

		self.load()

		self.switch()

	def preset(self):
		pygame.display.set_mode( (0,0), pygame.DOUBLEBUF | pygame.FULLSCREEN, 0)
		A, B= RESOLUCION
		self.ventana= pygame.Surface( (A, B), flags=HWSURFACE )
		self.ventana_real= pygame.display.get_surface()
		#C= pygame.display.Info().current_w
		#D= pygame.display.Info().current_h
		#self.resolucionreal= (C,D)
		C, D= self.resolucionreal
		self.VA= float(C)/float(A)
		self.VH= float(D)/float(B)

	def load(self):
		if not self.ventana: self.ventana = self.menu_principal.ventana
		pygame.event.set_blocked([JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN,
					KEYUP, VIDEORESIZE, VIDEOEXPOSE, USEREVENT, QUIT, ACTIVEEVENT])
		pygame.event.set_allowed([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYDOWN])
		pygame.mouse.set_visible(True)

		if not self.Bichos: self.Bichos= Bichos_Cantores(self)
		if not self.reloj: self.reloj= pygame.time.Clock()
		if not self.fondo: self.fondo= self.get_fondo()

		if not self.dialog:
			self.dialog= JAMDialog()
			self.dialog.set_text(tamanio= 40)

		if not pygame.mixer.get_init():
			pygame.mixer.init(44100, -16, 2, 2048)
		pygame.mixer.music.set_volume(1.0)
		self.estado= True

	def switch(self):
		return self.run()

	def run(self):
		self.ventana.blit(self.fondo, (0,0))
		self.Bichos.draw(self.ventana)
		pygame.display.update()
		while self.estado:
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			Traduce_posiciones(self.VA, self.VH)
			if self.mensaje:
				self.pause_game()
			self.Bichos.clear(self.ventana, self.fondo)
			self.Bichos.update()
			self.handle_event()
			pygame.event.clear()
			self.Bichos.draw(self.ventana)			
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def handle_event(self):
		for event in pygame.event.get(pygame.KEYDOWN):
			tecla= event.key
			if tecla== pygame.K_ESCAPE:
				pygame.event.clear()
				return self.selecciona_mensaje_salir()

	def pause_game(self):
		while self.mensaje.sprites():
			self.reloj.tick(35)
			while gtk.events_pending():
			    	gtk.main_iteration(False)
			Traduce_posiciones(self.VA, self.VH)
			self.Bichos.clear(self.ventana, self.fondo)
			self.mensaje.clear(self.ventana, self.fondo)
			self.mensaje.update()
			self.Bichos.draw(self.ventana)
			self.mensaje.draw(self.ventana)
			self.ventana_real.blit(pygame.transform.scale(self.ventana, self.resolucionreal), (0,0))
			pygame.display.update()

	def deselecciona_mensaje(self, boton):
		self.mensaje= None
		self.mensaje= pygame.sprite.OrderedUpdates()

	def selecciona_mensaje_salir(self):
		self.dialog.set_text(texto= "¿ Salir de CantaBichos ?")
		self.dialog.connect(funcion_ok= self.salir, funcion_cancel= self.deselecciona_mensaje)
		self.mensaje= self.dialog

	def selecciona_mensaje_limite(self):
		self.dialog.set_text(texto= "No puedes Reproducir más de 8 Sonidos a la vez !!")
		self.dialog.connect(funcion_ok= self.deselecciona_mensaje, funcion_cancel= self.deselecciona_mensaje)
		self.mensaje= self.dialog

	def get_fondo(self, color=(100,100,100,1), tamanio=RESOLUCION):
		superficie = pygame.Surface( tamanio, flags=HWSURFACE )
		superficie.fill(color)
		return superficie

	def salir(self, boton):
		sys.exit()
	
class Bichos_Cantores(pygame.sprite.OrderedUpdates):
	def __init__(self, main):
		pygame.sprite.OrderedUpdates.__init__(self)
		self.main = main
		self.botones = {}

		for imagen in os.listdir(IMAGENES):
			sonido= os.path.basename(imagen).split(".")[0]+".ogg"
			imagen= os.path.join(IMAGENES, imagen)
			boton= JAMButton("", imagen)
			boton.set_imagen(origen= imagen) 
			boton.set_tamanios(tamanio= (190, 180), grosorbor= 1, espesor= 1)
			self.add(boton)
			jam_label = JAMLabel("Cantando . . .")
			jam_label.set_text(tamanio= 25, color=(255,0,0,1))
			self.botones[boton] = [sonido, jam_label, False, sonido]
			boton.connect(callback=self.play_canto, sonido_select=None)
		x = 0
		y = 0
		contador = 0
		for boton in self.sprites():
			boton.set_posicion(punto=(x,y))
			x += 200
			contador += 1
			if contador == 6:
				x = 0
				y += boton.get_tamanio()[1]
				contador = 0

	def play_canto(self, boton):
		if self.botones[boton][2] == False:
			if self.verifica_cantos() >= 8:
				self.main.selecciona_mensaje_limite()
				return
			if type(self.botones[boton][0])== str:
				self.botones[boton][0] = pygame.mixer.Sound(os.path.join(CANTOS, self.botones[boton][3]))
				self.botones[boton][0].play(-1)
			posicion = (boton.rect.x+5, boton.rect.y+5)
			self.botones[boton][1].set_posicion(posicion)
			self.add(self.botones[boton][1])
			self.botones[boton][2]= True
			return
		else:
			self.botones[boton][0].stop()
			self.botones[boton][0] = self.botones[boton][3]
			self.botones[boton][1].kill()
			self.botones[boton][2] = False
			return

	'''
	def detiene_cantos(self):
		for boton in self.botones.keys():
			if self.botones[boton][2] == True:
				self.botones[boton][0].stop()
				self.botones[boton][0] = self.botones[boton][3] # descarga el sonido xque la xo no aguanta
				self.botones[boton][1].kill()
				self.botones[boton][2] = False'''

	def verifica_cantos(self):
	# cuenta cuantos sonidos se están reproduciendo porque la xo no soporta mas de 15 simultaneos.
		cantos = 0
		for boton in self.botones.keys():
			if self.botones[boton][2]: cantos += 1
		return cantos

