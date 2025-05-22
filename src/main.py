import sys
import os
import tkinter as tk
from tkinter import messagebox

# Configurar codificación para Windows
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'C')

# Añadir las carpetas necesarias al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.dirname(__file__))

def mostrar_menu_principal():
    """Crea y muestra el menú principal del sistema SIGAL"""
    def ejecutar_modulo_usuarios():
        """Ejecuta el módulo de usuarios"""
        try:
            menu_root.destroy()  # Cerrar menú
            from views.user_gui import UserGUI
            app = UserGUI()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar módulo de usuarios: {e}")
            mostrar_menu_principal()  # Volver al menú

    def ejecutar_modulo_laboratorios():
        """Ejecuta el módulo de laboratorios"""
        try:
            menu_root.destroy()  # Cerrar menú
            
          
            print("SIGAL - Modulo 3: Gestion de Laboratorios y Horarios")
            print("=" * 60)
            
            from laboratory.LaboratorioViewFinal import LaboratorioViewFinal
            
            # Crear la ventana principal
            root = tk.Tk()
            
            # Crear la aplicación
            app = LaboratorioViewFinal(root)
            
            print("Interfaz grafica cargada exitosamente!")
            
            # Ejecutar la aplicación
            root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar módulo de laboratorios: {e}")
            import traceback
            traceback.print_exc()
            mostrar_menu_principal()  # Volver al menú

    def salir_aplicacion():
        """Cierra la aplicación"""
        menu_root.destroy()

    # Crear ventana del menú principal
    menu_root = tk.Tk()
    menu_root.title("SIGAL - Sistema Integral de Gestion Academica")
    menu_root.geometry("500x400")
    menu_root.configure(bg='#f0f0f0')
    
    # Centrar ventana
    menu_root.eval('tk::PlaceWindow . center')
    
    # Título principal
    title_frame = tk.Frame(menu_root, bg='#2c3e50', height=80)
    title_frame.pack(fill='x', pady=(0, 20))
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(title_frame, 
                          text="SIGAL", 
                          font=('Arial', 24, 'bold'), 
                          fg='white', 
                          bg='#2c3e50')
    title_label.pack(expand=True)
    
    subtitle_label = tk.Label(title_frame, 
                             text="Sistema Integral de Gestion Academica", 
                             font=('Arial', 12), 
                             fg='#ecf0f1', 
                             bg='#2c3e50')
    subtitle_label.pack()
    
    # Marco para botones
    button_frame = tk.Frame(menu_root, bg='#f0f0f0')
    button_frame.pack(expand=True, padx=50, pady=20)
    
    # Estilo de botones
    button_style = {
        'font': ('Arial', 14, 'bold'),
        'width': 25,
        'height': 2,
        'relief': 'raised',
        'bd': 3
    }
    
    # Botón módulo usuarios
    btn_usuarios = tk.Button(button_frame, 
                            text="Modulo de Usuarios",
                            bg='#3498db',
                            fg='white',
                            command=ejecutar_modulo_usuarios,
                            **button_style)
    btn_usuarios.pack(pady=10)
    
    # Botón módulo laboratorios
    btn_laboratorios = tk.Button(button_frame, 
                                text="Modulo de Laboratorios",
                                bg='#27ae60',
                                fg='white',
                                command=ejecutar_modulo_laboratorios,
                                **button_style)
    btn_laboratorios.pack(pady=10)
    
    # Botón salir
    btn_salir = tk.Button(button_frame, 
                         text="Salir",
                         bg='#e74c3c',
                         fg='white',
                         command=salir_aplicacion,
                         **button_style)
    btn_salir.pack(pady=20)
    
    # Información adicional
    info_label = tk.Label(menu_root, 
                         text="Selecciona el modulo que deseas utilizar",
                         font=('Arial', 10),
                         fg='#7f8c8d',
                         bg='#f0f0f0')
    info_label.pack(side='bottom', pady=10)
    
    menu_root.mainloop()

if __name__ == "__main__":
    mostrar_menu_principal()