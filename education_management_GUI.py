import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Main Application Class
class SimpleEducationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Education Management System")
        self.data = None  # Placeholder for dataset

        # Load Data Section
        self.load_button = tk.Button(root, text="Load CSV Dataset", command=self.load_data)
        self.load_button.pack(pady=10)

        self.data_preview = tk.Text(root, height=10, width=100)
        self.data_preview.pack()

        # Analysis Section
        self.analysis_label = tk.Label(root, text="Data Analysis and Visualizations")
        self.analysis_label.pack(pady=10)

        self.visualize_button = tk.Button(root, text="Visualize Grade Distribution", command=self.visualize_grades)
        self.visualize_button.pack(pady=5)

        self.correlation_button = tk.Button(root, text="Show Correlation Matrix", command=self.correlation_matrix)
        self.correlation_button.pack(pady=5)

        # Machine Learning Section
        self.ml_label = tk.Label(root, text="Machine Learning")
        self.ml_label.pack(pady=10)

        self.train_button = tk.Button(root, text="Train Regression Model", command=self.train_regression)
        self.train_button.pack(pady=5)

    def load_data(self):
        # Open File Dialog to load CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.data_preview.delete("1.0", tk.END)
                self.data_preview.insert(tk.END, self.data.head().to_string())
                messagebox.showinfo("Success", "Dataset loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {e}")

    def visualize_grades(self):
        if self.data is not None:
            plt.figure(figsize=(8, 6))
            sns.histplot(self.data['FinalGrade'], kde=True, bins=10, color='blue')
            plt.title("Grade Distribution")
            plt.xlabel("Final Grade")
            plt.ylabel("Frequency")
            plt.show()
        else:
            messagebox.showerror("Error", "Please load a dataset first!")

    def correlation_matrix(self):
        if self.data is not None:
            try:
                # Select only numeric columns
                numeric_data = self.data.select_dtypes(include=["float64", "int64"])

                if numeric_data.empty:
                    raise ValueError("The dataset does not contain numeric columns for correlation analysis.")

                # Compute and visualize correlation matrix
                plt.figure(figsize=(8, 6))
                corr = numeric_data.corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
                plt.title("Correlation Matrix")
                plt.show()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compute correlation matrix: {e}")
        else:
            messagebox.showerror("Error", "Please load a dataset first!")


    def train_regression(self):
        if self.data is not None:
            try:
                # Features and target
                features = ['Math', 'English', 'Science', 'Attendance']
                target = 'FinalGrade'

                # Check if required columns exist
                if not all(col in self.data.columns for col in features + [target]):
                    raise KeyError(f"Missing required columns: {features + [target]}")

                X = self.data[features]
                y = self.data[target]

                # Split data into train and test sets
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Train regression model
                model = LinearRegression()
                model.fit(X_train, y_train)

                # Predict and display results
                predictions = model.predict(X_test)
                results = pd.DataFrame({"Actual": y_test, "Predicted": predictions})
                messagebox.showinfo("Success", "Regression model trained successfully!")
                plt.figure(figsize=(8, 6))
                sns.scatterplot(x=results["Actual"], y=results["Predicted"], color="green")
                plt.title("Actual vs Predicted Grades")
                plt.xlabel("Actual Grades")
                plt.ylabel("Predicted Grades")
                plt.show()
            except Exception as e:
                messagebox.showerror("Error", f"Model training failed: {e}")
        else:
            messagebox.showerror("Error", "Please load a dataset first!")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleEducationGUI(root)
    root.mainloop()
