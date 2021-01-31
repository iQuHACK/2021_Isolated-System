# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:37:27 2021

@author: frede
"""

import numpy as np
from qiskit import *
from qiskit import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

# For qsphere generation
vectorbackend = Aer.get_backend('statevector_simulator')

# For generating circuits
simulator = Aer.get_backend('qasm_simulator')

import matplotlib
matplotlib.use("Agg")
#Using agg, we can make the plots into pygame surfaces
import matplotlib.backends.backend_agg as agg

import pygame, sys
from pygame.locals import *


pygame.init()

infoObject = pygame.display.Info()

screen_width = infoObject.current_w
screen_height = infoObject.current_h

print(screen_width)
print(screen_height)

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Gate/State Memory')

font = pygame.font.SysFont('Constantia', 30)
#define colours
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

class Game():
    
    def __init__(self):
        #goto_introscreen
        self.gate_n = 2
        self.qbts_n = 2
        self.bg_col = (204, 102, 0)
        self.OGcardback = pygame.image.load('Pictures/duck.png').convert()
        self.cardback = None
        self.goto_mainmenu()
    
    #Take username
    def goto_mainmenu(self):
        
        
        again = button(screen_width/10, screen_height/20, 'Play Again?', self)
        quitbut = button(300, 640, 'Quit?', self)
        m_gates = button(200, 460, 'Add gates', self)
        l_gates = button(400, 460, 'Remove gates', self)
        m_qbts = button(200, 550, 'Add qubit', self)
        l_qbts = button(400, 550, 'Remove qubit', self)


        run = True

        while run:
            #get mouse position
            pos = pygame.mouse.get_pos()
            
            screen.fill(self.bg_col)
            if again.draw_button(pos):
                print('PLAY!')
                self.goto_play()
            if quitbut.draw_button(pos):
                print('Quit')
                run = False
            if m_gates.draw_button(pos):
                print("Added qubit")
                self.gate_n += 1
            if l_gates.draw_button(pos):
                if self.gate_n > 2:
                    print('Removed gate')
                    self.gate_n -= 1
                else:
                    print('At least 2 gates required')
            if m_qbts.draw_button(pos):
                if self.qbts_n < 3:
                    print("Added qubit")
                    self.qbts_n += 1
                else:
                    print("At most 3 qubits")
            if l_qbts.draw_button(pos):
                if self.qbts_n > 2:
                    print('Removed qubit')
                    self.qbts_n -= 1
                else:
                    print('At least 2 qubits')
            
            text_img = font.render("Gates: " + str(self.gate_n), True, black)
            text_len = text_img.get_width()
            screen.blit(text_img, (630, 490))
            
            text_img = font.render("Qubits: " + str(self.qbts_n), True, black)
            text_len = text_img.get_width()
            screen.blit(text_img, (630, 580))
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False	
        
        
            pygame.display.update()
        
        self.quit()
    
    def goto_play(self):
        card_x = 4
        card_y = 3
        pairs = [int(i/2) for i in range(card_x*card_y)]
        np.random.shuffle(pairs)
        card_height = int(screen_height/card_y*0.8) 
        card_width = int(screen_width/card_x*0.8)
        buffer_x = int(screen_width/card_x*0.1)
        buffer_y = int(screen_height/card_y*0.1)
        self.cardback = pygame.transform.scale(self.OGcardback, (card_width, card_height))
        
        #Easy mode
        pictures = create_pictures(int(card_x*card_y/2), self.qbts_n, self.gate_n)
        #Harder mode
        #pictures = create_pictures(int(card_x*card_y/2), 3, 5)
        
        cards = []
        no = -1
        for x in np.linspace(0, screen_width, card_x+1)[:-1]:
                for y in np.linspace(0, screen_height, card_y+1)[:-1]:
                    no += 1
                    cards.append(card(x+buffer_x, y+buffer_y, card_height, card_width, "Test", self, pictures[no][1], pictures[no][0]))
        pressed = []
                    
        while cards:
            #get mouse position
            pos = pygame.mouse.get_pos()
            screen.fill(self.bg_col)
            
            closed = False
            if len(pressed)==2:
                closed = True
        
            #removes = []
            for idx in range(len(cards)):
                but = cards[idx]
                if but.draw_card(pos, closed):
                    if but.flipped == 0:
                        pressed.remove(idx)
                    else:
                        print(idx)
                        pressed.append(idx)
                    #removes.append(idx)
            
            #for rem in reversed(removes):
            #    del buttons[rem]
            
            if len(pressed) > 1:
                if cards[pressed[0]].pair == cards[pressed[1]].pair:
                    pressed.sort(reverse=True)
                    for rem in pressed:
                        del cards[rem]
                    pressed = []
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cards = False
                    
            pygame.display.update()
         
        self.goto_mainmenu()
        self.quit()
                    
                
        
    
        
    def quit(self):
        pygame.quit()
        sys.exit()
    
def create_pictures(pair_n, qbt_n, gate_n):
    pics = []
    states = []
    for n in range(pair_n):
        circuit = create_gates(qbt_n, gate_n)
        state = Statevector.from_instruction(circuit)
        #Make sure to only add circuit that map to unique statevectors
        while list(state.data) in states:
            circuit = create_gates(qbt_n, gate_n)
            state = Statevector.from_instruction(circuit)
        
        states.append(list(state.data))
        
        circ_plot = circuit.draw(output="mpl")
        qsphere_plot = plot_state_qsphere(state)
            
        pics.append([circ_plot,n])
        pics.append([qsphere_plot,n])
    np.random.shuffle(pics)
    return pics

def create_gates(qbt_n, gate_n):

    
    qr = QuantumRegister(9)
    cr = ClassicalRegister(9)
    qc = QuantumCircuit(qr, cr)

    #First three qubits decide the gate
    #Can be tuned to have higher probabilities of some gates.
    qc.h(qr[0:3])

    #Next two qubits decide the qubit to apply gate to
    #50/50, 00 and 01 for two qubits:
    if qbt_n == 2:
        qc.h(3)
    #Create 1/3 chance of 00, 01, and 10, respectively.
    elif qbt_n == 3:
        qc.ry(2*np.arcsin(1/np.sqrt(3)), 3)
        qc.x(3)
        qc.ch(3,4)
        qc.x(3)
    #Generate angle (pi/n) in case rotation gate was chosen
    qc.h(qr[5:7])

    #Generate target in case controlled not was chosen.
    if qbt_n == 2:
        qc.x(7)
        qc.cx(3,7)
    if qbt_n == 3:
        qc.x(qr[3:5])
        #If 00
        #q.cch(qr[3,4],7)
        #Instead using identity (up to global phase)
        qc.ry(np.pi/4, 7)
        qc.ccx(3,4,7)
        qc.ry(-np.pi/4, 7)

        qc.ccx(3,4,8)
        qc.mct([qr[i] for i in [3,4,7]],8)
        qc.x(qr[3:5])

        #If 01
        qc.ch(3,8)

        #If 10
        qc.ch(4,7)


    # Map the quantum measurement to the classical bits
    qc.measure(qr, cr)

    # Execute the circuit on the qasm simulator
    job = execute(qc, simulator, shots=gate_n)

    # Grab results from the job
    result = job.result()

    # Returns counts
    counts = result.get_counts(qc)

    state_list = []
    for k in counts.keys():
        for i in range(counts[k]):
            state_list.append(k)

    #Convert to gate format
    gates = []
    for state in state_list:
        gates.append({"gate": int(state[6:9],2), "qubit":int(state[4:6],2), 
                          "rotation":np.pi/4*(int(state[2:4],2)+1), "c_target": int(state[0:2],2)})
        
    return generate_circuit(gates, qbt_n)

def generate_circuit(gates, qbt_n):
    qr = QuantumRegister(qbt_n)
    qc = QuantumCircuit(qr)
    for gate in gates:
        if gate["gate"] == 0:
            qc.h(gate["qubit"])
        elif gate["gate"] == 1:
            qc.x(gate["qubit"])
        elif gate["gate"] == 2:
            qc.y(gate["qubit"])
        elif gate["gate"] == 3:
            qc.z(gate["qubit"])
        elif gate["gate"] == 4:
            qc.rx(gate["rotation"] ,gate["qubit"])
        elif gate["gate"] == 5:
            qc.ry(gate["rotation"] ,gate["qubit"])
        elif gate["gate"] == 6:
            qc.rz(gate["rotation"] ,gate["qubit"])
        elif gate["gate"] == 7:
            qc.cx(gate["qubit"], gate["c_target"])
        else:
            print("Error")
    return qc
    
        
class card():
    #colours for button and text
    button_col = [(0,0,0),(255, 255, 255)]
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    
    def __init__(self, x, y, height, width, text, parent, pair, diagram):
        self.parent = parent
        self.x = x
        self.y = y
        #Gotta get that sweet, sweet, golden ratio
        self.width = width
        self.height = height
    
        canvas = agg.FigureCanvasAgg(diagram)
        canvas.draw()
        self.diagram_size = canvas.get_width_height()
        
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        surf = pygame.image.fromstring(raw_data, self.diagram_size, "RGB")
        
        scaled_dim = (int(self.diagram_size[0]*self.height/self.diagram_size[1]), self.height)
        if scaled_dim[0]>self.width:
            scaled_dim = (self.width, int(self.diagram_size[1]*self.width/self.diagram_size[0]))
            
        
        self.scaled_diagram = pygame.transform.smoothscale(surf, scaled_dim)
        
        self.pair = pair
        self.text = text
        self.flipped = 0
        self.clicked = False
        
    def draw_card(self, pos, closed):
        action = False
        
        #create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)
        
        #add text to button
        if self.flipped:
            pygame.draw.rect(screen, self.button_col[self.flipped], button_rect)
            screen.blit(self.scaled_diagram, (self.x, self.y))
        else:
            screen.blit(self.parent.cardback, (self.x, self.y))
            if closed:
                s = pygame.Surface((self.width,self.height))  # the size of your rect
                s.set_alpha(100)                # alpha level
                s.fill((100,100,100))           # this fills the entire surface
                screen.blit(s, (self.x, self.y)) 
                self.clicked = False
            
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                s = pygame.Surface((self.width,self.height))  # the size of your rect
                s.set_alpha(100)                # alpha level
                s.fill((100,100,100))           # this fills the entire surface
                screen.blit(s, (self.x, self.y)) 
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.flipped = (self.flipped + 1)%2
                action = True
            else:
                s = pygame.Surface((self.width,self.height))  # the size of your rect
                s.set_alpha(50)                # alpha level
                s.fill((255,255,255))           # this fills the entire surface
                screen.blit(s, (self.x, self.y)) 
        else:
            #pygame.draw.rect(screen, self.button_col[self.flipped], button_rect)
            self.clicked = False
		
		#add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
                
        return action
        

class button():
		
    #colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black

    def __init__(self, x, y, text, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = 180
        self.height = 70
        self.text = text
        self.clicked = False
        
        if self.text=='Play Again?':
            self.image = pygame.image.load('Pictures/qSphere.png').convert()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.image = None


    def draw_button(self, pos):
        action = False

        #create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)
		
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)
            self.clicked = False
		
		#add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        #add text to button
        if self.text=='Play Again?':
            screen.blit(self.image, (self.x, self.y))
        else:
            text_img = font.render(self.text, True, self.text_col)
            text_len = text_img.get_width()
            screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action

#Run game
Game()
