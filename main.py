import cluster_analysis
import cluster_methods
from tkinter import *
import matplotlib.pyplot as plt
from pandastable import Table
from tkinter import filedialog
from tkinter import ttk
import re
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


class App:

    def __init__(self, master):

        self.master = master
        self.master.title("Data Clustering")
        self.master.geometry("600x350")
        self.master.resizable(0, 0)

        self.if_label, self.number = IntVar(), IntVar()
        self.separators = StringVar()
        self.chosen_method, self.chosen_cluster = 0, 0
        self.filename, self.cluster_object = None, None

        self.all_separators = [',', ';', '.', '/']
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
            command=self.show_method
        )

        self.visualize_button = Button(
            master,
            text='Cluster details',
            command=self.visualize,
            state='disabled'
        )

        self.save_to_file_button = Button(
            master,
            text='Save to file',
            command=self.save_to_file,
            state='disabled'
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

    def packed(self):
        self.open_button.place(x=270, y=10)
        self.show_button.place(x=250, y=210)
        self.text_number_of_clusters.place(x=200, y=50)
        self.number_of_clusters.place(x=350, y=50)
        self.check_label.place(x=230, y=80)
        self.text_separator.place(x=250, y=110)
        self.check_separator.place(x=275, y=130)
        self.save_to_file_button.place(x=265, y=300)
        self.visualize_button.place(x=255, y=250)
        self.display_methods_button.place(x=250, y=175)

    def visualize(self):
        self.check_number()
        self.read_cluster_object()
        new_window = Toplevel(self.master)
        frame = Frame(new_window)
        new_window.title("Clustering methods")
        frame.pack(fill='both', expand=True)
        tv = ttk.Treeview(
            frame,
            columns=1,
            show='headings'
        )
        tv.column(1, minwidth=0, width=150, stretch=NO)
        tv.heading(1, text='Number of cluster')
        for i in range(int(self.number)):
            tv.insert(parent='', index=i, iid=i, values=i)
        Button(new_window, text="Choose cluster", command=lambda: [self.choose_cluster(tv), new_window.destroy()]).pack()
        tv.pack()

    @staticmethod
    def generate_plot(dataframe, number):
        dataframe = dataframe.drop(dataframe.columns[[-1]], axis=1)
        details = dataframe.mean(axis=0)
        details.plot(kind='bar')
        plt.title('Cluster no. ' + number)
        plt.xlabel('', fontsize=10)
        plt.show()

    def choose_cluster(self, tv):
        self.chosen_cluster = tv.focus()
        self.plot_chosen_cluster(self.chosen_cluster, self.cluster_object.data_frame)

    def plot_chosen_cluster(self, number_of_cluster, dataframe):
        if self.if_label:
            dataframe = dataframe.drop(dataframe.columns[[0]], axis=1)
        dataframe = dataframe.astype(int)
        dataframe_of_one_cluster = dataframe[dataframe['cluster'] == int(number_of_cluster)]
        self.generate_plot(dataframe_of_one_cluster, number_of_cluster)

    def extract_number(self, text):
        self.chosen_method = re.findall(r'\d+', text)[0]

    def read_cluster_object(self):
        self.check_number()
        self.cluster_object = cluster_analysis.ClusterAnalysis(self.filename, int(self.number),
                                                               cluster_methods.selected_method[int(self.chosen_method)],
                                                               self.if_label.get(), self.separators.get())

    def save_to_file(self):
        self.read_cluster_object()
        filename = filedialog.asksaveasfilename(filetypes=[("CSV", "*.csv")], defaultextension="*.csv")
        if filename:
            with open(filename, "w", -1, "utf-8") as file:
                self.cluster_object.data_frame.to_csv(file, sep=self.separators.get(), index=False)

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
        self.save_to_file_button.config(state="normal")
        self.visualize_button.config(state="normal")

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

    def show_selected(self, tv):
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
            height=9
        )
        tv.heading(1, text='Method')
        tv.heading(2, text='Usecase')
        tv.column(1, minwidth=0, width=150, stretch=NO)
        tv.column(2, minwidth=0, width=900, stretch=YES)

        for i in range(8):
            tv.insert(parent='', index=i, iid=i, values=(cluster_methods.methods_names[i],
                                                     cluster_methods.methods_description[i]))

        Button(new_window, text="Choose method", command=lambda: [self.show_selected(tv), new_window.destroy()]).pack()
        tv.pack()

    def show(self):
        self.check_number()
        self.read_cluster_object()
        self.show_dataframe(self.cluster_object.data_frame)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
