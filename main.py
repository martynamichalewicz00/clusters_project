import cluster_analysis
from tkinter import *
from tkinter import filedialog



class App:

    def __init__(self, master):
        self.if_label, self.number = IntVar(), IntVar()
        self.separators = StringVar()
        self.filename = None
        self.master = master
        self.master.title("Data Clustering")
        self.master.geometry("600x300")
        self.master.resizable(0, 0)
        self.all_separators = [',',';','.']
        self.separators.set(self.all_separators[0])

        self.text_number_of_clusters = Label(master, text="Number of clusters")
        self.text_separator = Label(master, text="Choose separator")
        self.open_button = Button(
            master,
            text='Open a File',
            command=self.file_select
        )

        self.show_button = Button(
            master,
            text='show all',
            command=self.show
        )

        self.check_label = Checkbutton(
            master,
            text = "Label on first column",
            onvalue = 1,
            offvalue = 0,
            variable = self.if_label
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
        self.show_button.place(x=270,y=250)
        self.text_number_of_clusters.place(x=200, y=50)
        self.number_of_clusters.place(x=350,y=50)
        self.check_label.place(x=230,y=80)
        self.text_separator.place(x=250, y=110)
        self.check_separator.place(x=275, y=130)

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

    def show(self):
        self.check_number()
        c = cluster_analysis.ClusterAnalysis(self.filename, int(self.number),"kmeans",self.if_label.get(),self.separators.get())
        print(c.data_frame)




if __name__ == "__main__":
    root = Tk()
    app = App(root)
