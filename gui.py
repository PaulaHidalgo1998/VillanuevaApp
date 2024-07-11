import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from database import Database
from tksheet import Sheet

class Application(ttk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Personas")
        self.database = Database("personas.db")
        self.root.geometry("1030x600")

        # Estilo
        style = ttk.Style(self.root)
        style.theme_use('clam')  # Puedes cambiar el tema

        # Configuración de estilo
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TCombobox', font=('Helvetica', 12))
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

        self.create_widgets()

        self.tree.bind("<ButtonRelease-1>", self.on_column_click)  # Añadir evento de clic en el encabezado
        self.sort_column = None
        self.sort_ascending = True

    def create_widgets(self):
        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Nombre
        self.label_nombre = ttk.Label(main_frame, text="Nombre:")
        self.label_nombre.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_nombre = ttk.Entry(main_frame)
        self.entry_nombre.grid(row=0, column=1, pady=8)

        # Apellidos
        self.label_apellidos = ttk.Label(main_frame, text="Apellidos:")
        self.label_apellidos.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_apellidos = ttk.Entry(main_frame)
        self.entry_apellidos.grid(row=1, column=1, pady=5)

        # Dinero
        self.label_dinero = ttk.Label(main_frame, text="Dinero:")
        self.label_dinero.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_dinero = ttk.Entry(main_frame)
        self.entry_dinero.grid(row=2, column=1, pady=5)

        # Tipo de Aportación
        self.label_tipo_aportacion = tk.Label(self.root, text="Tipo de Aportación")
        self.label_tipo_aportacion.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_tipo_aportacion  = ttk.Combobox(
            main_frame,
            state="readonly",
            values=["Adulto", "Mayor 67", "Joven", "Aportaciones"]
        )
        self.combo_tipo_aportacion.grid(row=3, column=1, pady=5)

        # Botón para añadir persona
        self.add_button = tk.Button(self.root, text="Añadir Persona", command=self.add_persona)
        self.add_button.grid(row=4, columnspan=2, pady=10)

        # Etiqueta para mostrar el número total de personas
        self.label_total_personas = ttk.Label(main_frame, text=f"Total de personas: {self.database.count_personas()}")
        self.label_total_personas.grid(row=6, columnspan=2, pady=10)

        # Tabla para ver personas
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Apellidos", "Dinero", "Tipo_aportacion"), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Apellidos', text='Apellidos')
        self.tree.heading('Dinero', text='Dinero')
        self.tree.heading('Tipo_aportacion', text='Tipo de Aportación')
        self.tree.grid(row=7, columnspan=2, pady=10)

        self.load_personas()

       # Botón para eliminar persona
        self.delete_button = ttk.Button(main_frame, text="Eliminar Persona", command=self.delete_persona)
        self.delete_button.grid(row=5, columnspan=2, pady=10)
        
        # Botón para Borrar TODO
        #self.delete_all_button = tk.Button(self.root, text="Borrar Todo", command=self.delete_ALL)
        #self.delete_all_button.grid(row=5, columnspan=2, pady=10)

    def add_persona(self):
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        dinero = self.entry_dinero.get()
        tipo_aportacion = self.combo_tipo_aportacion.get()

        if nombre and apellidos and tipo_aportacion:
            try:
                dinero = float(dinero)
                self.database.add_persona(nombre, apellidos, dinero, tipo_aportacion)
                messagebox.showinfo("Éxito", "Persona añadida correctamente")
                self.clear_entries()
            except ValueError:
                messagebox.showerror("Error", "El campo dinero debe ser un número.")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
        self.load_personas()

    def delete_persona(self):
        selected_item = self.tree.selection()
        if selected_item:
            persona = self.tree.item(selected_item)["values"]
            id = persona[0]

            if messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres eliminar a {persona[1]} {persona[2]}?"):
                self.database.delete_persona(id )
                
                self.tree.delete(selected_item)
                messagebox.showinfo("Éxito", "Persona eliminada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una persona para eliminar")


    def delete_ALL(self):
        self.database.delete_all()
        self.load_personas()

    def clear_entries(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_dinero.delete(0, tk.END)
        self.combo_tipo_aportacion.set('')

    def load_personas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        personas = self.database.get_personas()
        for persona in personas:
            self.tree.insert("", "end", values=persona[0:])

    def on_column_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            column = self.tree.identify_column(event.x)
            column_name = column[1:]  # Obtener el número de columna (como cadena)
            if self.sort_column == column_name:
                self.sort_ascending = not self.sort_ascending
            else:
                self.sort_column = column_name
                self.sort_ascending = True
            self.sort_table(self.sort_column, self.sort_ascending)

    def sort_table(self, col, ascending):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        data.sort(reverse=not ascending)
        for index, item in enumerate(data):
            self.tree.move(item[1], "", index)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
