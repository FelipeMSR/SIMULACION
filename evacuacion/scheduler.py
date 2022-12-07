from typing import Type, Callable
from evacuacion.agentes import Civil
import mesa


class RandomActivationByTypeFiltered(mesa.time.RandomActivationByType):
    """
    A scheduler that overrides the get_type_count method to allow for filtering
    of agents by a function before counting.

    Example:
    >>> scheduler = RandomActivationByTypeFiltered(model)
    >>> scheduler.get_type_count(AgentA, lambda agent: agent.some_attribute > 10)
    """
    
    def get_type_count(
        self,
        salvado,
        t_edad,
        estado,
        type_class: Type[mesa.Agent],
        filter_func: Callable[[mesa.Agent], bool] = None,
    ) -> int:
        """
        Returns the current number of agents of certain type in the queue that satisfy the filter function.
        """
        count = 0
        civil_count = 0
        edad = 0
        e_salvado = 0    
        distancia = 0
   
        for agent in self.agents_by_type[type_class].values():
            if type(agent) is Civil:
                """
                if dist == 1 and agent.estado == "No evacuado":
                    distancia = abs(agent.posFin[1] - agent.pos[1])
                    print("EL PE ES: ",agent.posFin[1], "MI DISTANCIA ES: ", agent.pos[1], "Y LA DISTANCIA ES: ",distancia)
                    return distancia
                """
                if t_edad == 1:
                    if agent.edad <= 25:
                        edad += 1
                        if salvado == 1 and agent.evacuado:
                            e_salvado +=1
                elif t_edad == 2:
                    if agent.edad > 25 and agent.edad <= 45:
                        edad +=1
                        if salvado == 1 and agent.evacuado:
                            e_salvado +=1
                elif t_edad == 3:
                    if agent.edad > 45:
                        edad +=1
                        if salvado == 1 and agent.evacuado:
                            e_salvado +=1
                if agent.estado == estado:
                    civil_count +=1
            elif filter_func is None or filter_func(agent):
                count += 1
        
        if distancia > 0:
            return distancia
        elif civil_count > 0:
            return civil_count
        elif e_salvado > 0:
            return e_salvado
        elif edad > 0:
            return edad
        
        return count
