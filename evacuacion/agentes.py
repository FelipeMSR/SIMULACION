import mesa
from evacuacion.walk import Walk

class Civil(Walk):
    def __init__(self, unique_id: int, posIni: tuple, pos:tuple, posFin, model, edad, evacuado, tiempoEvacuado, conoceRuta, moore):
        super().__init__(unique_id, model, pos, moore = moore)
        self.pos = pos
        self.posIni = posIni
        self.posFin = posFin
        self.edad = edad
        self.evacuado = evacuado
        self.tiempoEvacuado = tiempoEvacuado
        self.conoceRuta = conoceRuta
        self.estado = "Evacuando"
        if self.edad >= 13 and self.edad <45:
            self.rapidez = 5.0
        else:
            self.rapidez = 2.5
        

        
    def step(self):

        if self.comparar_muerte(Ola):
            self.estado = "No evacuado"
            
        if self.estado == "Evacuando" and self.rapidez == 5.0:
            #print("soy el agente: ",self.unique_id, "en la pos: ", self.pos)
            self.movimiento(Camino, Obstaculo, Guia)
            if not(self.edad >= 13 and self.edad <45):
                self.rapidez = 2.5
        elif self.estado == "Evacuando":
            self.rapidez = 5.0
            
        
        if self.pos[0] in self.posFin and self.pos[1] == 99:
            self.evacuado = True
            self.estado = "Evacuado en PE"

        elif self.pos[0] not in self.posFin and self.pos[1] == 99:
            self.evacuado = True
            self.estado = "Evacuado sin PE"    


class Guia(Walk):
    def __init__(self, unique_id: int, model, pos,maximo, moore=True):
        super().__init__(unique_id, model, pos, moore)
        self.pos = pos
        self.tEspera = 0
        self.maximo = maximo

    def step(self):
        if self.tEspera == 60:
            self.ola_guia_mov(self.maximo)     
        else:
            self.tEspera +=1     

class Camino(mesa.Agent):
    def __init__(self, unique_id: int, model, pos:tuple):
        super().__init__(unique_id, model)
        self.pos = pos
    def step(self) -> None:
        return super().step()



class Obstaculo(mesa.Agent):
    def __init__(self, unique_id: int, model, pos:tuple):
        super().__init__(unique_id, model)
        self.pos = pos
    def step(self) -> None:
        return super().step()

class Ola(Walk):
    def __init__(self, unique_id: int, model, pos:tuple, maximo,moore):
        super().__init__(unique_id, model, pos, moore=moore)
        self.pos = pos
        self.maximo = maximo
        self.espera = 0

    def step(self):
        if self.espera == 15:
            self.ola_guia_mov(self.maximo)
        else:
            self.espera += 1

