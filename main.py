import cluster_analysis
import cluster_methods
from tkinter import *
from pandastable import Table
from tkinter import filedialog
from tkinter import ttk
import re
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


class App:

    def __init__(self, master):

        self.if_label, self.number = IntVar(), IntVar()
        self.separators = StringVar()
        self.chosen_method = 0

        self.filename = None
        self.master = master
        self.master.title("Data Clustering")
        self.master.geometry("600x300")
        self.master.resizable(0, 0)
        self.all_separators = [',', ';', '.']
        self.separators.set(self.all_separators[0])

        self.text_number_of_clusters = Label(master, text="Number of clusters")
        self.text_separator = Label(master, text="Choose separator")
        self.open_button = Button(
            master,
            text='Open a file',
            command=self.file_select
        )

        self.show_button = Button(
            master,
            text='Show Dataframe',
            state='disabled',
            command=self.show
        )

        self.display_methods_button = Button(
            master,
            text='Choose method',
            command=self.display_methods
        )

        self.save_to_file_button = Button(
            master,
            text='Save to file',
            command=self.save_to_file
        )

        self.check_label = Checkbutton(
            master,
            text="Label on first column",
            onvalue=1,
            offvalue=0,
            variable=self.if_label
        )

        self.number_of_clusters = Entry(
            master,
            width=5)

        self.check_separator = OptionMenu(
            master,
            self.separators,
            *self.all_separators
        )

        self.packed()
        self.master.mainloop()

    def extract_number(self,text):
        self.chosen_method = re.findall(r'\d+', text)[0]

    def save_to_file(self):
        self.check_number()
        cluster_object = cluster_analysis.ClusterAnalysis(self.filename, int(self.number),
                                                          cluster_methods.selected_method[int(self.chosen_method)],
                                                          self.if_label.get(), self.separators.get())
        filename = filedialog.asksaveasfilename(filetypes=[("CSV", "*.csv")], defaultextension="*.csv")
        if filename:
            with open(filename, "w", -1, "utf-8") as file:
                cluster_object.data_frame.to_csv(file, sep=self.separators.get(), index=False)

    def packed(self):
        self.open_button.place(x=270, y=10)
        self.show_button.place(x=250, y=210)
        self.text_number_of_clusters.place(x=200, y=50)
        self.number_of_clusters.place(x=350, y=50)
        self.check_label.place(x=230, y=80)
        self.text_separator.place(x=250, y=110)
        self.check_separator.place(x=275, y=130)
        self.save_to_file_button.place(x=265, y=260)
        self.display_methods_button.place(x=250, y=175)

    def check_number(self):
        if self.number_of_clusters.get().isnumeric():
            self.number = self.number_of_clusters.get()
        else:
            self.number = 2

    def file_select(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select file",
                                                   filetypes=(("CSV files", "*.csv"),
                                                              ("all files", "*.*")))
        self.show_button.config(state="normal")


    def show_dataframe(self, cluster_object):
        new_window = Toplevel(self.master)
        frame = Frame(new_window)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=cluster_object)
        new_window.title("Data")
        new_window.geometry("600x600")
        pt.show()

    def show_methods(self, cluster_object):
        new_window = Toplevel(self.master)
        frame = Frame(new_window)
        frame.pack(fill='both', expand=True)
        pt = Table(frame, dataframe=cluster_object)
        new_window.title("Data")
        new_window.geometry("600x600")
        pt.show()

    def show_selected(self,tv):
        try:
            self.extract_number(str(tv.selection()))
        except IndexError:
            pass

    def show_method(self):
        new_window = Toplevel(self.master)
        frame = Frame(new_window)
        new_window.title("Clustering methods")
        frame.pack(fill='both', expand=True)
        tv = ttk.Treeview(
            frame,
            columns=(1, 2),
            show='headings',
            height=8
        )
        tv.heading(1, text='Method')
        tv.heading(2, text='Usecase')
        tv.column(1, minwidth=0, width=150, stretch=NO)
        tv.column(2, minwidth=0, width=900, stretch=YES)

        tv.insert(parent='', index=0, iid=0, values=(cluster_methods.methods_names[0],
                                                     cluster_methods.methods_description[0]))
        tv.insert(parent='', index=1, iid=1, values=(cluster_methods.methods_names[1],
                                                     cluster_methods.methods_description[1]))
        tv.insert(parent='', index=2, iid=2, values=(cluster_methods.methods_names[2],
                                                     cluster_methods.methods_description[2]))
        tv.insert(parent='', index=3, iid=3, values=(cluster_methods.methods_names[3],
                                                     cluster_methods.methods_description[3])),
        tv.insert(parent='', index=4, iid=4, values=(cluster_methods.methods_names[4],
                                                     cluster_methods.methods_description[4])),
        tv.insert(parent='', index=5, iid=5, values=(cluster_methods.methods_names[5],
                                                     cluster_methods.methods_description[5]))
        tv.insert(parent='', index=6, iid=6, values=(cluster_methods.methods_names[6],
                                                     cluster_methods.methods_description[6]))
        tv.insert(parent='', index=7, iid=7, values=(cluster_methods.methods_names[7],
                                                     cluster_methods.methods_description[7]))


        Button(new_window, text="Choose method", command=lambda:[self.show_selected(tv), new_window.destroy()]).pack()
        tv.pack()

    def display_methods(self):
        self.show_method()

    def show(self):
        self.check_number()
        cluster_object = cluster_analysis.ClusterAnalysis(self.filename, int(self.number), cluster_methods.selected_method[int(self.chosen_method)],
                                                          self.if_label.get(), self.separators.get())
        self.show_dataframe(cluster_object.data_frame)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
