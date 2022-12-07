import mesa
import random

from evacuacion.agentes import Civil, Camino, Obstaculo, Ola, Guia
from evacuacion.scheduler import RandomActivationByTypeFiltered


class Simulacion(mesa.Model):

    ancho = 100
    alto = 100

    cant_civiles = 500
    cant_caminos = 200
    cant_obstaculos = 100

    puntos_encuentro = 5

    verbose = False #print 
    def __init__(
        self,
        ancho = 100,
        alto = 100,
        cant_civiles = 500,
        cant_caminos = 200,
        cant_obstaculos = 100,
        puntos_encuentro = 5,

        ):
        super().__init__()
        self.ancho = ancho
        self.alto = alto
        self.cant_civiles = cant_civiles
        self.cant_caminos = cant_caminos
        self.cant_obstaculos = cant_obstaculos
        self.puntos_encuentro = puntos_encuentro

        self.schedule = RandomActivationByTypeFiltered(self)
        #self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.ancho,self.alto,True)
        self.run = 0
        

        self.datacollector = mesa.DataCollector(
            {
                "Evacuando": lambda m: m.schedule.get_type_count(0,0,"Evacuando",Civil),
                "No evacuado": lambda m: m.schedule.get_type_count(0,0,"No evacuado",Civil),
                "Evacuado en PE": lambda m: m.schedule.get_type_count(0,0,"Evacuado en PE",Civil),
                "Evacuado sin PE": lambda m: m.schedule.get_type_count(0,0,"Evacuado sin PE",Civil),
                "Joven": lambda m: m.schedule.get_type_count(0,1,"",Civil),
                "Adulto": lambda m: m.schedule.get_type_count(0,2,"",Civil),
                "Mayor": lambda m: m.schedule.get_type_count(0,3,"",Civil),
                "Joven evacuado": lambda m: m.schedule.get_type_count(1,1,"",Civil),
                "Adulto evacuado": lambda m: m.schedule.get_type_count(1,2,"",Civil),
                "Mayor evacuado": lambda m: m.schedule.get_type_count(1,3,"",Civil),

            }
        )


        
        #crear caminos
        puntos = []
        i = 0
        while i < self.puntos_encuentro:
            x = self.random.randrange(self.ancho)
            if x+1 < self.ancho and x+2 < self.ancho and x not in puntos and (x + 1) not in puntos and (x + 2) not in puntos:
                puntos.append(x)
                puntos.append(x+1)
                puntos.append(x+2)
                i+=1
        
        
        cantidad_altura = self.cant_caminos/self.puntos_encuentro
        altura_minima = self.alto - cantidad_altura
        puntos_caminos = [[]]
        for x in puntos:
            altura_maxima = self.alto -1
            while altura_maxima >= altura_minima:
                pos ={x,altura_maxima}
                camino = Camino(self.next_id(),self,pos)
                self.grid.place_agent(camino, (x,altura_maxima))
                self.schedule.add(camino)
                puntos_caminos.append((x,altura_maxima))
                altura_maxima = altura_maxima - 1

        #Crear guias
        for x in puntos:
            guia = Guia(self.next_id(),self,(x,int(altura_minima)-1),self.alto+1,False)
            self.grid.place_agent(guia,(x,int(altura_minima)-1))
            self.schedule.add(guia)

        
        #crear obstaculos
        #X,Y random
        i = 0
        while i < self.cant_obstaculos:
            
            x = self.random.randrange(self.ancho)
            y = self.random.randrange(self.alto-1)
            if (x,y) not in puntos_caminos:
                obstaculo = Obstaculo(self.next_id(),self,(x,y))
                self.grid.place_agent(obstaculo, (x, y))
                self.schedule.add(obstaculo) 
                i+= 1   
            

        #crear olas
        for i in range(self.ancho):
            ola = Ola(self.next_id(),self,(i,0),self.alto,False)
            self.grid.place_agent(ola, (i,0))
            self.schedule.add(ola)

        #crear civiles
        #X,Y random, se setean edades y atributos con valores random basados en distintas probabilidades
        #unique_id: int, posIni, pos, posFin, model, edad, evacuado, tiempoEvacuado, conoceRuta, puntoEncuentro, moore
        
        for i in range(self.cant_civiles):
            x = self.random.randrange(self.ancho)
            y = self.random.randrange(1,self.alto)
            """minimo = -1
            for punto in puntos:
                dif = abs(x-punto)
                if minimo == -1 or dif<minimo:
                    minimo = dif
                    xfin = punto
            """
            edad = random.randint(13,70)
            evacuado = False
            t_evacuado = 0
            conocer = random.randint(1,100)
            if conocer < 70:
                conoce = True
                
                x = self.random.choice(puntos)
            else:
                conoce = False
            moore = True
            civil = Civil(self.next_id(),(x,y),(x,y),puntos,self,edad,evacuado,t_evacuado,conoce,moore)
            self.grid.place_agent(civil, (x, y))
            self.schedule.add(civil)

        self.running = True      
        self.datacollector.collect(self)
       
    def step(self):
        if self.run == 113:
            self.running = False
        self.schedule.step()
        self.run +=1
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [ 
                    self.schedule.time,
                    self.schedule.get_type_count(Civil),
                    self.schedule.get_type_count(Camino),
                    self.schedule.get_type_count(Obstaculo),
                    self.schedule.get_type_count(Ola)
                ]
            )
    
    