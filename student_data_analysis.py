import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EducationManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Education Management System")

        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # First Tab
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Student Data")

        # Create GUI Elements in Tab 1
        self.create_tab1_elements()

        # Data storage
        self.data = None
        self.canvas = None

    def create_tab1_elements(self):
        # Button to Load CSV
        self.load_button = tk.Button(self.tab1, text="Load CSV Data", command=self.load_csv)
        self.load_button.pack(pady=10)

        # Label for success message
        self.message_label = tk.Label(self.tab1, text="")
        self.message_label.pack()

        # Dropdown for selecting columns
        self.column_var = tk.StringVar(value="FinalGrade")
        self.column_dropdown = ttk.Combobox(self.tab1, textvariable=self.column_var, state="readonly")
        self.column_dropdown.pack(pady=10)
        self.column_dropdown.set("Select Column to Plot")

        # Button to Plot Graph
        self.plot_button = tk.Button(self.tab1, text="Plot Graph", command=self.plot_graph)
        self.plot_button.pack(pady=10)

        # Frame for displaying the graph
        self.graph_frame = tk.Frame(self.tab1)
        self.graph_frame.pack(fill='both', expand=True, pady=10)

    def load_csv(self):
        # Open File Dialog
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                # Read CSV
                self.data = pd.read_csv(file_path)
                
                # Ensure column names match the expected structure
                expected_columns = ["StudentID", "Name", "Age", "Gender", "Class",
                                    "Math", "English", "Science", "Attendance",
                                    "PreviousGrade", "FinalGrade"]
                if all(column in self.data.columns for column in expected_columns):
                    self.message_label.config(text="CSV loaded successfully!", fg="green")
                    # Update dropdown options
                    self.column_dropdown["values"] = expected_columns[5:]  # Exclude non-numeric columns
                else:
                    self.message_label.config(text="CSV does not have required columns.", fg="red")
                    self.data = None
            except Exception as e:
                self.message_label.config(text=f"Error loading CSV: {e}", fg="red")
        else:
            self.message_label.config(text="No file selected.", fg="orange")

    def plot_graph(self):
        if self.data is not None:
            column_to_plot = self.column_var.get()
            if column_to_plot and column_to_plot != "Select Column to Plot":
                try:
                    # Clear any previous graph
                    for widget in self.graph_frame.winfo_children():
                        widget.destroy()

                    # Create a new figure for the graph
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(self.data['Name'], self.data[column_to_plot], color='blue')
                    ax.set_title(f"Student {column_to_plot}")
                    ax.set_xlabel("Student Name")
                    ax.set_ylabel(column_to_plot)
                    ax.set_xticks(range(len(self.data['Name'])))
                    ax.set_xticklabels(self.data['Name'], rotation=45)
                    fig.tight_layout()

                    # Embed the plot in the Tkinter GUI
                    self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                    self.canvas.draw()
                    self.canvas.get_tk_widget().pack(fill='both', expand=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Error plotting graph: {e}")
            else:
                messagebox.showwarning("Invalid Selection", "Please select a valid column to plot.")
        else:
            messagebox.showwarning("No Data", "Please load CSV data first.")

# Create main application window
root = tk.Tk()
app = EducationManagementGUI(root)
root.mainloop()
