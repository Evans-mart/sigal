import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Añadir las carpetas necesarias al path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from laboratory.LaboratorioController import LaboratorioController

class LaboratorioViewFinal:
    def __init__(self, root):
        self.root = root
        self.controller = LaboratorioController()
        
        # Configurar la ventana principal
        self.setup_window()
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear la interfaz
        self.create_interface()
        
        # Variables de estado
        self.selected_lab_id = None
        
        # Cargar datos iniciales
        self.refresh_laboratorios()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("SIGAL - Sistema de Gestion de Acceso a Laboratorios")
        self.root.geometry("1300x750")
        self.root.minsize(1000, 600)
        
        # Centrar la ventana
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configura los estilos personalizados"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Estilos personalizados
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#2c3e50')
        
        # Botones con colores
        style.configure('Success.TButton', font=('Arial', 9, 'bold'), background='#27ae60')
        style.configure('Danger.TButton', font=('Arial', 9, 'bold'), background='#e74c3c')
        style.configure('Warning.TButton', font=('Arial', 9, 'bold'), background='#f39c12')
        style.configure('Primary.TButton', font=('Arial', 9, 'bold'), background='#3498db')
        
        # Treeview personalizado
        style.configure('Custom.Treeview', font=('Arial', 9))
        style.configure('Custom.Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_interface(self):
        """Crea la interfaz principal"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        # Header con título
        self.create_header(main_frame)
        
        # Contenido principal
        self.create_content(main_frame)
        
        # Footer con información
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crea el header de la aplicación"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título principal
        title_label = ttk.Label(header_frame, text="Gestion de Laboratorios y Horarios", 
                               style='Title.TLabel')
        title_label.pack(side="left")
        
        # Información del módulo
        module_label = ttk.Label(header_frame, text="Modulo 3 - Sistema SIGAL", 
                                style='Info.TLabel')
        module_label.pack(side="right")
        
        # Línea separadora
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill="x", pady=(10, 0))
    
    def create_content(self, parent):
        """Crea el contenido principal"""
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Panel izquierdo - Laboratorios
        left_panel = ttk.LabelFrame(content_frame, text=" Laboratorios Disponibles ", 
                                   padding="10")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Panel derecho - Detalles
        right_panel = ttk.LabelFrame(content_frame, text=" Informacion Detallada ", 
                                    padding="10")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Crear contenido de paneles
        self.create_laboratory_panel(left_panel)
        self.create_details_panel(right_panel)
    
    def create_laboratory_panel(self, parent):
        """Panel de laboratorios mejorado"""
        # Frame para controles superiores
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Contador de laboratorios
        self.lab_count_var = tk.StringVar(value="Total: 0 laboratorios")
        count_label = ttk.Label(control_frame, textvariable=self.lab_count_var, 
                               style='Info.TLabel')
        count_label.pack(side="left")
        
        # Filtro de estado
        ttk.Label(control_frame, text="Filtrar:").pack(side="right", padx=(10, 5))
        self.filter_var = tk.StringVar(value="todos")
        filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_var, 
                                   width=12, state="readonly")
        filter_combo["values"] = ("todos", "activo", "inactivo", "mantenimiento")
        filter_combo.pack(side="right")
        filter_combo.bind("<<ComboboxSelected>>", self.filter_laboratories)
        
        # Treeview mejorado
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Nombre", "Ubicacion", "Capacidad", "Estado")
        self.lab_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                                    height=15, style='Custom.Treeview')
        
        # Configurar columnas
        self.lab_tree.heading("ID", text="ID")
        self.lab_tree.heading("Nombre", text="Nombre")
        self.lab_tree.heading("Ubicacion", text="Ubicacion")
        self.lab_tree.heading("Capacidad", text="Capacidad")
        self.lab_tree.heading("Estado", text="Estado")
        
        self.lab_tree.column("ID", width=80, anchor="center")
        self.lab_tree.column("Nombre", width=150)
        self.lab_tree.column("Ubicacion", width=180)
        self.lab_tree.column("Capacidad", width=80, anchor="center")
        self.lab_tree.column("Estado", width=100, anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.lab_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.lab_tree.xview)
        self.lab_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar treeview y scrollbars
        self.lab_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos
        self.lab_tree.bind("<ButtonRelease-1>", self.on_laboratory_select)
        self.lab_tree.bind("<Double-1>", lambda e: self.edit_laboratory())
        
        # Botones - AQUÍ ESTÁ EL ARREGLO PRINCIPAL
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Crear botones individuales para mejor control
        btn_nuevo = tk.Button(button_frame, 
                             text="+ Nuevo Laboratorio",
                             command=self.show_lab_form,
                             bg='#27ae60',
                             fg='white',
                             font=('Arial', 9, 'bold'),
                             relief='raised',
                             bd=2)
        btn_nuevo.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        btn_editar = tk.Button(button_frame, 
                              text="Editar",
                              command=self.edit_laboratory,
                              bg='#3498db',
                              fg='white',
                              font=('Arial', 9, 'bold'),
                              relief='raised',
                              bd=2)
        btn_editar.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        btn_eliminar = tk.Button(button_frame, 
                                text="Eliminar",
                                command=self.delete_laboratory,
                                bg='#e74c3c',
                                fg='white',
                                font=('Arial', 9, 'bold'),
                                relief='raised',
                                bd=2)
        btn_eliminar.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        btn_actualizar = tk.Button(button_frame, 
                                  text="Actualizar",
                                  command=self.refresh_laboratorios,
                                  bg='#f39c12',
                                  fg='white',
                                  font=('Arial', 9, 'bold'),
                                  relief='raised',
                                  bd=2)
        btn_actualizar.pack(side="left", fill="x", expand=True)
    
    def create_details_panel(self, parent):
        """Panel de detalles mejorado"""
        # Información del laboratorio
        info_frame = ttk.LabelFrame(parent, text=" Informacion del Laboratorio ", 
                                   padding="15")
        info_frame.pack(fill="x", pady=(0, 15))
        
        # Variables de información
        self.lab_info = {
            "nombre": tk.StringVar(value="Seleccione un laboratorio"),
            "ubicacion": tk.StringVar(value="-"),
            "capacidad": tk.StringVar(value="-"),
            "equipamiento": tk.StringVar(value="-"),
            "estado": tk.StringVar(value="-")
        }
        
        # Crear campos de información
        info_fields = [
            ("Nombre:", "nombre"),
            ("Ubicacion:", "ubicacion"),
            ("Capacidad:", "capacidad"),
            ("Equipamiento:", "equipamiento"),
            ("Estado:", "estado")
        ]
        
        for i, (label_text, key) in enumerate(info_fields):
            field_frame = ttk.Frame(info_frame)
            field_frame.pack(fill="x", pady=2)
            
            label = ttk.Label(field_frame, text=label_text, style='Subtitle.TLabel', width=15)
            label.pack(side="left", anchor="nw")
            
            if key == "equipamiento":
                value_label = ttk.Label(field_frame, textvariable=self.lab_info[key], 
                                      style='Info.TLabel', wraplength=300)
            else:
                value_label = ttk.Label(field_frame, textvariable=self.lab_info[key], 
                                      style='Info.TLabel')
            value_label.pack(side="left", anchor="nw", fill="x", expand=True)
        
        # Panel de horarios
        schedule_frame = ttk.LabelFrame(parent, text=" Horarios Asignados ", padding="15")
        schedule_frame.pack(fill="both", expand=True)
        
        # Controles de horarios
        schedule_control_frame = ttk.Frame(schedule_frame)
        schedule_control_frame.pack(fill="x", pady=(0, 10))
        
        self.schedule_count_var = tk.StringVar(value="Horarios: 0")
        count_label = ttk.Label(schedule_control_frame, textvariable=self.schedule_count_var, 
                               style='Info.TLabel')
        count_label.pack(side="left")
        
        # Treeview de horarios
        horario_tree_frame = ttk.Frame(schedule_frame)
        horario_tree_frame.pack(fill="both", expand=True)
        
        horario_columns = ("ID", "Dia", "Inicio", "Fin", "Tipo")
        self.horario_tree = ttk.Treeview(horario_tree_frame, columns=horario_columns, 
                                        show="headings", height=8, style='Custom.Treeview')
        
        # Configurar columnas de horarios
        self.horario_tree.heading("ID", text="ID")
        self.horario_tree.heading("Dia", text="Dia")
        self.horario_tree.heading("Inicio", text="Inicio")
        self.horario_tree.heading("Fin", text="Fin")
        self.horario_tree.heading("Tipo", text="Tipo")
        
        self.horario_tree.column("ID", width=70, anchor="center")
        self.horario_tree.column("Dia", width=100, anchor="center")
        self.horario_tree.column("Inicio", width=80, anchor="center")
        self.horario_tree.column("Fin", width=80, anchor="center")
        self.horario_tree.column("Tipo", width=100, anchor="center")
        
        # Scrollbar para horarios
        h_scroll_horario = ttk.Scrollbar(horario_tree_frame, orient="vertical", 
                                        command=self.horario_tree.yview)
        self.horario_tree.configure(yscrollcommand=h_scroll_horario.set)
        
        self.horario_tree.grid(row=0, column=0, sticky="nsew")
        h_scroll_horario.grid(row=0, column=1, sticky="ns")
        
        horario_tree_frame.grid_rowconfigure(0, weight=1)
        horario_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos de horarios
        self.horario_tree.bind("<Double-1>", lambda e: self.edit_horario())
        
        # Botones de horarios
        horario_button_frame = ttk.Frame(schedule_frame)
        horario_button_frame.pack(fill="x", pady=(15, 0))
        
        btn_nuevo_horario = tk.Button(horario_button_frame, 
                                     text="+ Nuevo Horario",
                                     command=self.show_horario_form,
                                     bg='#27ae60',
                                     fg='white',
                                     font=('Arial', 9, 'bold'),
                                     relief='raised',
                                     bd=2)
        btn_nuevo_horario.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        btn_editar_horario = tk.Button(horario_button_frame, 
                                      text="Editar Horario",
                                      command=self.edit_horario,
                                      bg='#3498db',
                                      fg='white',
                                      font=('Arial', 9, 'bold'),
                                      relief='raised',
                                      bd=2)
        btn_editar_horario.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        btn_eliminar_horario = tk.Button(horario_button_frame, 
                                        text="Eliminar Horario",
                                        command=self.delete_horario,
                                        bg='#e74c3c',
                                        fg='white',
                                        font=('Arial', 9, 'bold'),
                                        relief='raised',
                                        bd=2)
        btn_eliminar_horario.pack(side="left", fill="x", expand=True)
    
    def create_footer(self, parent):
        """Crea el footer de la aplicación"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill="x", pady=(20, 0))
        
        # Línea separadora
        separator = ttk.Separator(footer_frame, orient='horizontal')
        separator.pack(fill="x", pady=(0, 10))
        
        # Información del pie
        status_frame = ttk.Frame(footer_frame)
        status_frame.pack(fill="x")
        
        # Estado de conexión
        self.connection_status = tk.StringVar(value="Conectado a MongoDB")
        status_label = ttk.Label(status_frame, textvariable=self.connection_status, 
                                style='Info.TLabel')
        status_label.pack(side="left")
        
        # Información del desarrollador
        dev_label = ttk.Label(status_frame, text="Desarrollado por: [Tu nombre] - Modulo 3", 
                             style='Info.TLabel')
        dev_label.pack(side="right")
    
    def show_lab_form(self, lab_data=None):
        """Muestra el formulario para crear o editar un laboratorio"""
        print("Abriendo formulario de laboratorio...")  # Debug
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Laboratorio" if not lab_data else "Editar Laboratorio")
        dialog.geometry("500x500")  # Aumenté la altura
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar el diálogo
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 50))
        
        # Frame principal con scrollbar por si acaso
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(scrollable_frame, padding="25")
        main_frame.pack(fill="both", expand=True)
        
        title_text = "Crear Nuevo Laboratorio" if not lab_data else f"Editar: {lab_data.get('nombre', 'Laboratorio')}"
        title_label = ttk.Label(main_frame, text=title_text, style='Subtitle.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Variables del formulario
        nombre_var = tk.StringVar(value=lab_data["nombre"] if lab_data else "")
        ubicacion_var = tk.StringVar(value=lab_data["ubicacion"] if lab_data else "")
        capacidad_var = tk.StringVar(value=str(lab_data["capacidad"]) if lab_data else "")
        equipamiento_var = tk.StringVar(value=lab_data["equipamiento"] if lab_data else "")
        estado_var = tk.StringVar(value=lab_data["estado"] if lab_data else "activo")
        
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill="both", expand=True)
        
        # Campo Nombre
        ttk.Label(fields_frame, text="Nombre del Laboratorio:", style='Info.TLabel').pack(anchor="w", pady=(0, 5))
        nombre_entry = ttk.Entry(fields_frame, textvariable=nombre_var, font=('Arial', 10))
        nombre_entry.pack(fill="x", pady=(0, 10))
        
        # Campo Ubicación
        ttk.Label(fields_frame, text="Ubicacion:", style='Info.TLabel').pack(anchor="w", pady=(0, 5))
        ubicacion_entry = ttk.Entry(fields_frame, textvariable=ubicacion_var, font=('Arial', 10))
        ubicacion_entry.pack(fill="x", pady=(0, 10))
        
        # Campo Capacidad
        ttk.Label(fields_frame, text="Capacidad (personas):", style='Info.TLabel').pack(anchor="w", pady=(0, 5))
        capacidad_entry = ttk.Entry(fields_frame, textvariable=capacidad_var, font=('Arial', 10))
        capacidad_entry.pack(fill="x", pady=(0, 10))
        
        # Campo Equipamiento
        ttk.Label(fields_frame, text="Equipamiento:", style='Info.TLabel').pack(anchor="w", pady=(0, 5))
        equipamiento_text = tk.Text(fields_frame, height=3, font=('Arial', 10), wrap=tk.WORD)
        equipamiento_text.insert("1.0", equipamiento_var.get())
        equipamiento_text.pack(fill="x", pady=(0, 10))
        
        # Campo Estado
        ttk.Label(fields_frame, text="Estado:", style='Info.TLabel').pack(anchor="w", pady=(0, 5))
        estado_combo = ttk.Combobox(fields_frame, textvariable=estado_var, state="readonly", font=('Arial', 10))
        estado_combo["values"] = ("activo", "inactivo", "mantenimiento")
        estado_combo.pack(fill="x", pady=(0, 20))  # Más espacio antes de los botones
        
        # Frame de botones
        button_frame = ttk.Frame(fields_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        def save_lab():
            nombre = nombre_var.get().strip()
            ubicacion = ubicacion_var.get().strip()
            capacidad_str = capacidad_var.get().strip()
            equipamiento = equipamiento_text.get("1.0", tk.END).strip()
            estado = estado_var.get()
            
            print(f"Guardando laboratorio: {nombre}, {ubicacion}, {capacidad_str}")  # Debug
            
            if not all([nombre, ubicacion, capacidad_str, equipamiento]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            try:
                capacidad = int(capacidad_str)
                if capacidad <= 0 or capacidad > 200:
                    raise ValueError("La capacidad debe estar entre 1 y 200")
            except ValueError as e:
                messagebox.showerror("Error", f"Capacidad invalida: {str(e)}")
                return
            
            try:
                if lab_data:
                    success = self.controller.update_laboratorio(
                        lab_data["id"], nombre, ubicacion, capacidad, equipamiento, estado
                    )
                    message = "actualizado" if success else "No se pudo actualizar"
                else:
                    lab_id = self.controller.create_laboratorio(
                        nombre, ubicacion, capacidad, equipamiento, estado
                    )
                    success = lab_id is not None
                    message = "creado" if success else "No se pudo crear"
                
                print(f"Resultado: {success}, {message}")  # Debug
                
                if success:
                    messagebox.showinfo("Exito", f"Laboratorio {message} correctamente.")
                    dialog.destroy()
                    self.refresh_laboratorios()
                else:
                    messagebox.showerror("Error", f"{message} el laboratorio.")
            except Exception as e:
                print(f"Error al guardar: {e}")  # Debug
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        
        # Botones más grandes y visibles
        btn_guardar = tk.Button(button_frame, 
                               text="💾 GUARDAR",
                               command=save_lab,
                               bg='#27ae60',
                               fg='white',
                               font=('Arial', 12, 'bold'),
                               height=2,
                               relief='raised',
                               bd=3)
        btn_guardar.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        btn_cancelar = tk.Button(button_frame, 
                                text="❌ CANCELAR",
                                command=dialog.destroy,
                                bg='#e74c3c',
                                fg='white',
                                font=('Arial', 12, 'bold'),
                                height=2,
                                relief='raised',
                                bd=3)
        btn_cancelar.pack(side="left", fill="x", expand=True)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        nombre_entry.focus()
        print("Formulario creado exitosamente")  # Debug
    
    # Resto de métodos - los métodos que faltan los agrego aquí
    def filter_laboratories(self, event=None):
        """Filtra laboratorios por estado"""
        print("Filtrando laboratorios...")  # Debug
        pass  # Implementar según necesites
    
    def refresh_laboratorios(self):
        """Actualiza la lista de laboratorios"""
        print("Actualizando laboratorios...")  # Debug
        try:
            labs = self.controller.get_all_laboratorios()
            print(f"Laboratorios obtenidos: {len(labs)}")  # Debug
            
            # Limpiar treeview
            for item in self.lab_tree.get_children():
                self.lab_tree.delete(item)
            
            # Insertar laboratorios
            for lab in labs:
                self.lab_tree.insert("", tk.END, values=(
                    lab["id"][:8] + "..." if len(lab["id"]) > 8 else lab["id"],
                    lab["nombre"],
                    lab["ubicacion"],
                    f"{lab['capacidad']} pers.",
                    lab["estado"].upper()
                ))
            
            self.lab_count_var.set(f"Total: {len(labs)} laboratorios")
            self.connection_status.set("Conectado a MongoDB")
        except Exception as e:
            print(f"Error al actualizar: {e}")  # Debug
            self.connection_status.set("Error de conexion")
            messagebox.showerror("Error", f"Error al actualizar laboratorios: {e}")
    
    def on_laboratory_select(self, event):
        """Maneja la selección de un laboratorio"""
        print("Laboratorio seleccionado")  # Debug
        pass  # Implementar según necesites
    
    def edit_laboratory(self):
        """Edita el laboratorio seleccionado"""
        print("Editando laboratorio...")  # Debug
        pass  # Implementar según necesites
    
    def delete_laboratory(self):
        """Elimina el laboratorio seleccionado"""
        print("Eliminando laboratorio...")  # Debug
        pass  # Implementar según necesites
    
    def show_horario_form(self, horario_data=None):
        """Muestra el formulario para crear o editar un horario"""
        print("Mostrando formulario de horario...")  # Debug
        pass  # Implementar según necesites
    
    def edit_horario(self):
        """Edita el horario seleccionado"""
        print("Editando horario...")  # Debug
        pass  # Implementar según necesites
    
    def delete_horario(self):
        """Elimina el horario seleccionado"""
        print("Eliminando horario...")  # Debug
        pass  # Implementar según necesites

def main():
    """Función principal para ejecutar la aplicación mejorada"""
    root = tk.Tk()
    app = LaboratorioViewFinal(root)
    
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Esta seguro de que desea salir?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()