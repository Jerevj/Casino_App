from vistas.vista_almuerzo import mostrar_vista_almuerzo
from vistas.admin.mantenedor_excel import mostrar_mantenedor_excel
#from vistas.admin.mantenedor_personas import mostrar_mantenedor_personas

def ir_a_vista_almuerzo(main_frame, volver_callback):
    mostrar_vista_almuerzo(main_frame, volver_callback)

def ir_a_mantenedor_excel():
    mostrar_mantenedor_excel()

#def ir_a_mantenedor_personas():
 #   mostrar_mantenedor_personas()
