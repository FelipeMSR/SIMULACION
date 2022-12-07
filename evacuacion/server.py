import mesa
from evacuacion.agentes import Civil, Camino, Obstaculo, Ola, Guia
from evacuacion.model import Simulacion

COLORS = {"Evacuado en PE": "#00AA00", "No evacuado": "#880000", "Evacuando": "#FFFF00","Evacuado sin PE": "#B2FFFF"}
COLORS_2 = {"Joven": "#00AA00",  "Adulto": "#FFFF00","Mayor": "#B2FFFF"}
COLORS_3 = {"Joven evacuado": "#00AA00",  "Adulto evacuado": "#FFFF00","Mayor evacuado": "#B2FFFF"}


def simulacion_representacion(agent):
    if agent is None:
        return
    
    
    portrayal = {}

    
        
    if type(agent) is Camino:
        portrayal["Shape"] = "evacuacion/camino.png"
        portrayal["scale"] =0.9
        portrayal["Layer"] = 1
        
    elif type(agent) is Civil:
        
        if agent.estado == "Evacuando" or agent.estado == "Evacuado en PE" or agent.estado == "Evacuado sin PE" :
            portrayal["Shape"] = "evacuacion/persona.png"
            portrayal["scale"] =0.9
            portrayal["Layer"] = 0
        elif agent.estado == "No evacuado":
            portrayal["Shape"] = "evacuacion/tumba.png"
            portrayal["scale"] =0.9
            portrayal["Layer"] = 4
            
    elif type(agent) is Obstaculo:
        portrayal["Shape"] = "evacuacion/casa.png"
        portrayal["scale"] =0.9
        portrayal["Layer"] = 2

    elif type(agent) is Ola:
        portrayal["Shape"] = "evacuacion/ola.png"
        portrayal["scale"] =0.9
        portrayal["Layer"] = 3
    
    elif type(agent) is Guia:
        portrayal["Shape"] = "evacuacion/guia.png"
        portrayal["scale"] =0.9
        portrayal["Layer"] = 5
    
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(simulacion_representacion, 100, 100, 1500, 1500)
chart_element = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

edad_bar= mesa.visualization.BarChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_2.items()]
)

edad_e_bar= mesa.visualization.BarChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_3.items()]
)



server = mesa.visualization.ModularServer(
    Simulacion, [canvas_element, chart_element, pie_chart, edad_bar, edad_e_bar], "Evacuacion de tsunami"
)

server.port = 8521