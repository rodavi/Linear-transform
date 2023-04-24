import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class sUI:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Linear Transformation Interface")

        self.theme = ttk.Style()
        #print(self.theme.theme_names())
        self.theme.theme_use("winnative")
        self.__add_menus()
        self.__add_workspace()
        self.__add_treeview()
        self.__add_statebar()

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=10)
        self.root.grid_rowconfigure(0, weight=10)
        self.root.grid_rowconfigure(1, weight=0)
    
    def run(self):
        self.root.mainloop()

    def __add_menus(self):
        self.main_menu = sMenu(self.root)
        m_file = self.main_menu.create_tab("File")
        m_edit = self.main_menu.create_tab("Edit")
        m_help = self.main_menu.create_tab("Help")

        self.main_menu.add_command(m_file, "New", shortcut="Ctrl+N")
        self.main_menu.add_separator(m_file)
        self.main_menu.add_command(m_file, "Exit", command= lambda : self.root.destroy())
        self.main_menu.add_command(m_help, "Info", shortcut="Ctrl+I")

    def __add_workspace(self):
        Workspace(self.root, 1, 0)

    def __add_treeview(self):
        HierarchyTree(self.root, 0, 0)

    def __add_statebar(self):
        StateBar(self.root, 0, 1)

class sMenu(tk.Frame):

    def __init__(self, master) -> None:
        self.root = master
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu=self.main_menu)
    
    def create_tab(self, name):
        self.new_menu = tk.Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(menu=self.new_menu, label=name)

        self.root.config(menu=self.main_menu)
        return self.new_menu
    
    def add_command(self, tab, name, command=lambda : "", shortcut=""):
        tab.add_command(
            label=name,
            accelerator=shortcut,
            command=command
        )
    
    def add_separator(self, tab):
        tab.add_separator()


class Workspace():

    def __init__(self, master, x, y) -> None:
        self.root = master
        self.f_workspace = tk.Frame(self.root, relief=tk.SUNKEN)
        self.f_workspace.grid(column=x, row=y, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1)
        self.c_workspace = tk.Canvas(self.f_workspace, bg="lightgrey", width=600, height=500)
        self.c_workspace.grid(column=0, row=1, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1)
        self.count_particles = 0
        self.count_rot_col = 0
        self.block_count = 0

        # Buttons frame
        self.f_workspace.grid_columnconfigure(0, weight=1)
        self.f_workspace.grid_rowconfigure(0, weight=0)
        self.__create_buttons_bar()

        # Canvas
        self.f_workspace.grid_columnconfigure(0, weight=1)
        self.f_workspace.grid_rowconfigure(1, weight=1)

        self.c_workspace.grid_columnconfigure(0, weight=0)

    def __create_buttons_bar(self):
        self.f_buttons = tk.Frame(self.f_workspace)
        self.f_buttons.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1)

        def particle_block():
            BlockInCanvas(self.c_workspace, (0, self.block_count), "Particle "+str(self.count_particles))
            self.count_particles = self.count_particles+1
            self.block_count = self.block_count+1

        b_particle = CustomButton(self.f_buttons, "Particle", particle_block, (0, 0))

        def rx_block():
            BlockInCanvas(self.c_workspace, (self.block_count, 0), "Rx "+str(self.count_rot_col))
            self.count_rot_col = self.count_rot_col+1
            self.block_count = self.block_count+1

        b_rz = CustomButton(self.f_buttons, "Rx", rx_block, (1, 0))

        def ry_block():
            BlockInCanvas(self.c_workspace, (self.block_count, 0), "Ry "+str(self.count_rot_col))
            self.count_rot_col = self.count_rot_col+1
            self.block_count = self.block_count+1

        b_ry = CustomButton(self.f_buttons, "Ry", ry_block, (2, 0))

        def rz_block():
            BlockInCanvas(self.c_workspace, (self.block_count, 0), "Rz "+str(self.count_rot_col))
            self.count_rot_col = self.count_rot_col+1
            self.block_count = self.block_count+1

        b_rz = CustomButton(self.f_buttons, "Rz", rz_block, (3, 0))
    

class CustomButton(tk.Button):

    def __init__(self, parent, name="Button", command="Empty", position=(0, 0)):
        self.root = parent
        self.name = name
        self.command = command
        self.position = position
        self.b_new = tk.Button(self.root, text=self.name, command=self.command, width=10, height=2)
        self.b_new.grid(column=position[0], row=position[1], padx=1, pady=1, sticky=tk.W)

    def set_command(self, com):
        self.b_new.config(command=com)

    def get_button(self):
        return self.b_new

class HierarchyTree(tk.Frame):

    def __init__(self, master, x, y) -> None:
        self.root = master
        self.f_hierarchy_tree = tk.Frame(self.root)
        self.f_hierarchy_tree.grid_rowconfigure(0, weight=1)
        self.f_hierarchy_tree.grid(column=x, row=y, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1)
        self.t_hierarchy = ttk.Treeview(self.f_hierarchy_tree)
        self.t_hierarchy.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1)

        self.s_vertical = tk.Scrollbar(self.f_hierarchy_tree, orient="vertical")
        self.s_vertical.grid(column=1, row=0, sticky=tk.N+tk.S+tk.W+tk.E)

        self.t_hierarchy.config(yscrollcommand=self.s_vertical.set)

        self.s_horizontal = tk.Scrollbar(self.f_hierarchy_tree, orient="horizontal")
        self.s_horizontal.grid(column=0, row=1, sticky=tk.N+tk.S+tk.W+tk.E)

        self.t_hierarchy.config(xscrollcommand=self.s_horizontal.set)

class StateBar(tk.Frame):

    def __init__(self, master, x, y) -> None:
        self.root = master
        self.f_statebar = tk.LabelFrame(self.root, text="")
        self.f_statebar.grid_columnconfigure(0, weight=1)
        self.f_statebar.grid(column=x, row=y, sticky=tk.N+tk.S+tk.W+tk.E, padx=1, pady=1, columnspan=2)
        self.v_state = tk.StringVar()
        self.e_state = tk.Entry(self.f_statebar, state="readonly", textvariable=self.v_state)
        self.e_state.grid(column=0, row=0, sticky=tk.N+tk.S+tk.W+tk.E)
        self.e_state.grid_columnconfigure(0, weight=1)
        self.e_state.grid_rowconfigure(0, weight=2)

    def set_state(self, state):
        self.v_state.set(state)

    def get_state(self):
        return self.v_state.get()
    
class BlockInCanvas(tk.Canvas):

    def __init__(self, root, pos, name):
        self.root = root
        self.x0= pos[0]
        self.y0 = pos[1]

        self.bg_color = "#f5e49a"
        self.block = tk.Canvas(self.root, width=50, height=50, bg=self.bg_color, relief="solid")
        self.block.grid(column=self.x0, row=self.y0, padx=5, pady=5)

        self.block.grid_columnconfigure(0, weight=0)
        self.block.grid_rowconfigure(0, weight=0)

        self.xpad = 2
        self.ypad = 2

        self.l_block = tk.Label(self.block, text=name, bg=self.bg_color, font=('Helvatical bold',10, 'bold'))
        self.l_block.grid(column =0, row=0, padx=3, pady=3, sticky=tk.W)

        self.b_delete = tk.Button(self.block, text="D", command= lambda: self.block.destroy())
        self.b_delete.grid(column=1, row=0, sticky=tk.E, padx=self.xpad, pady=self.ypad)

        self.l_block_name = tk.Label(self.block, text="Name:", bg=self.bg_color)
        self.l_block_name.grid(column =0, row=1, pady=2, padx=self.xpad, sticky=tk.E)

        self.v_name = tk.StringVar()
        self.e_block_name = tk.Entry(self.block, textvariable=self.v_name)
        self.e_block_name.grid(column=1, row=1, padx=self.xpad, pady=self.ypad)

        """self.l_ini_pos = tk.Label(self.block, text="Initial Position:", bg=self.bg_color)
        self.l_ini_pos.grid(column =0, row=2, pady=ypad, padx=xpad, sticky=tk.E)

        self.v_ini_pos = tk.StringVar()
        self.e_pos = tk.Entry(self.block, textvariable=self.v_ini_pos)
        self.e_pos.grid(column=1, row=2, padx=xpad, pady=ypad)"""
    
    class BlockParticle(BlockInCanvas):

        def __init__(self, root, pos, name):
            super().__init__(self)
            self.l_ini_pos = tk.Label(self.block, text="Initial Position:", bg=self.bg_color)
            self.l_ini_pos.grid(column =0, row=2, pady=self.ypad, padx=self.xpad, sticky=tk.E)

            self.v_ini_pos = tk.StringVar()
            self.e_pos = tk.Entry(self.block, textvariable=self.v_ini_pos)
            self.e_pos.grid(column=1, row=2, padx=self.xpad, pady=self.ypad)