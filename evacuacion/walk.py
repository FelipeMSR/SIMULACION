import mesa


class Walk(mesa.Agent):
    grid = None
    x = None
    y = None
    moore = True
    
    def __init__(self, unique_id: int, model, pos, moore = True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    
    def comparar_muerte(self, ola):
        vecinos =  self.model.grid.get_neighbors(self.pos, self.moore, True)
        olas = [obj for obj in vecinos if isinstance(obj, ola)]
        
        for o in olas:
            if self.pos[1] <= o.pos[1]:
                return True
        
        return False
    
    def ola_guia_mov(self, maximo):
        
        if self.pos[1] + 2 < maximo:
            next_move = (self.pos[0],self.pos[1]+1)
            self.model.grid.move_agent(self, next_move)



    def movimiento(self, objetivo,obstaculo,guia):
        # Pick the next cell from the adjacent cells.
        next_moves = []
        vecinos =  self.model.grid.get_neighbors(self.pos, self.moore, True)
        objetivos = [obj for obj in vecinos if isinstance(obj, objetivo)]
        obstaculos = [obj for obj in vecinos if isinstance(obj, obstaculo)]
        guias = [obj for obj in vecinos if isinstance(obj, guia)]
        
        #si hay camino para llegar
        if len(objetivos) > 0:
            flag = 0
            #print("HAY OBJETIVOS")
            for ob in objetivos:
                #si el camino avanza, el proximo mov es por el camino
                if flag == 0 and ob.pos[1] > self.pos[1] :
                    #print("EL OBJETIVO ESTA ARRIBA")
                    next_moves.append(ob.pos)

            if len(next_moves) > 0:
                flag = 1
                next_move = self.random.choice(next_moves)
            if flag == 0:
                #print("Estoy arriba")
                next_move = self.pos
        elif len(guias) > 0:
            for g in guias:
                next_move = g.pos

        #Si no hay camino, pero hay obstaculo
        elif len(obstaculos) > 0:
            #print("HAY OBSTACULOS")
            y0 = self.pos[1]
            y = self.pos[1] + 1
            x0 = self.pos[0]
            x = self.pos[0] + 1
            x1 = self.pos[0] - 1

            next_moves.append((x0,y))
            next_moves.append((x,y))
            next_moves.append((x1,y))
            next_moves.append((x,y0))
            next_moves.append((x1,y0))

            for o in obstaculos:
                
                for n in next_moves:
                    if n != o.pos:
                        next_move = n
                        break
            

        #Si no hay camino, pero tampoco obstaculo se mueve de manera aleatoria
        else:
            y0 = self.pos[1]
            y = self.pos[1] + 1
            x0 = self.pos[0]
            x = self.pos[0] + 1
            x1 = self.pos[0] - 1

            next_moves.append((x0,y))
            next_moves.append((x,y))
            next_moves.append((x1,y))
            next_moves.append((x,y0))
            next_moves.append((x1,y0))

            next_move = self.random.choice(next_moves)
            if next_move[1] >= 100:
                next_move = self.pos
        if next_move [0] < 0:
           y = next_move[1]
           x = 1

           next_move = x,y 
            
        self.model.grid.move_agent(self, next_move)