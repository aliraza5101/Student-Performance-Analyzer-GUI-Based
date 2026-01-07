import customtkinter as ctk
import csv
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =============================================================================
# BACKEND LOGIC (Unchanged)
# =============================================================================
FILE_NAME = "students.csv"
students_list = []

class Student:
    def __init__(self, id, name, midterm, final, assignment):
        self.id = int(id)
        self.name = name
        self.midterm = float(midterm)
        self.final = float(final)
        self.assignment = float(assignment)
        self.final_score = 0.0
        self.grade = ""

    def compute_final(self):
        self.final_score = (0.4 * self.midterm) + (0.5 * self.final) + (0.1 * self.assignment)

    def compute_grade(self):
        if 85 <= self.final_score <= 100: self.grade = "A"
        elif 70 <= self.final_score < 85: self.grade = "B"
        elif 55 <= self.final_score < 70: self.grade = "C"
        elif 40 <= self.final_score < 55: self.grade = "D"
        else: self.grade = "F"

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "midterm": self.midterm,
            "final": self.final, "assignment": self.assignment,
            "final_score": round(self.final_score, 2), "grade": self.grade
        }

def load_data():
    students_list.clear()
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                s = Student(row["id"], row["name"], row["midterm"], row["final"], row["assignment"])
                s.compute_final()
                s.compute_grade()
                students_list.append(s)
    except FileNotFoundError:
        pass

def save_data():
    with open(FILE_NAME, mode='w', newline='') as file:
        fieldnames = ["id", "name", "midterm", "final", "assignment", "final_score", "grade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for s in students_list:
            writer.writerow(s.to_dict())

# =============================================================================
# COMPACT & MODERN GUI
# =============================================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") 

class StudentApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. GEOMETRY
        self.title("Student Perfomance Analyzer")
        self.geometry("950x600") 
        
        load_data()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Sidebar Title
        ctk.CTkLabel(self.sidebar, text="Analyzer Pro", font=("Montserrat", 20, "bold"), text_color="#2ecc71").pack(pady=(30, 5))
        ctk.CTkLabel(self.sidebar, text="v2.1 Compact", font=("Arial", 10), text_color="gray").pack(pady=(0, 20))

        # Compact Buttons
        self.add_sidebar_btn("🏠 Dashboard", self.show_dashboard)
        self.add_sidebar_btn("➕ Add Student", self.show_add_student)
        self.add_sidebar_btn("📂 Records", self.show_view_records)
        self.add_sidebar_btn("📈 Analytics", self.show_visualization)
        
        # Exit
        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#c0392b", hover_color="#e74c3c", height=35, 
                      font=("Arial", 12, "bold"), command=self.exit_app).pack(side="bottom", fill="x", padx=15, pady=20)

        # MAIN AREA
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#181818")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.show_dashboard()

    def add_sidebar_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, height=40, corner_radius=6,
                            fg_color="transparent", hover_color="#333333", anchor="w", font=("Arial", 13))
        btn.pack(pady=3, padx=10, fill="x")

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================
    # DASHBOARD (UPDATED FIX)
    # ==========================
    def show_dashboard(self):
        self.clear_frame()
        
        # 1. Branding Header
        banner = ctk.CTkFrame(self.main_frame, fg_color="#181818")
        banner.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(banner, text="Developed by", font=("Arial", 11), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(banner, text="ALI RAZA QURESHI", font=("Arial", 28 , "bold"), text_color="#3498db").pack(anchor="w")
        
        ctk.CTkLabel(banner, text="Supervised by", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=(5,0))
        ctk.CTkLabel(banner, text="DR. WAJID ARSHAD ABBASI", font=("Arial", 16, "bold"), text_color="#f1c40f").pack(anchor="w")

        ctk.CTkLabel(self.main_frame, text="⎯"*80, text_color="#333").pack()

        # 2. Stats Cards
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)

        total = len(students_list)
        avg = sum(s.final_score for s in students_list)/total if total else 0
        
        self.create_mini_card(stats_frame, "STUDENTS", str(total), "#27ae60")
        self.create_mini_card(stats_frame, "AVERAGE", f"{avg:.1f}", "#8e44ad")
        self.create_mini_card(stats_frame, "STATUS", "Active", "#2c3e50")

        # 3. QUOTE SECTION (Fixed: Only appears ONCE at bottom)
        quote_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        quote_frame.pack(side="bottom", pady=(0, 40), fill="x") 

        ctk.CTkLabel(quote_frame, text='"We want to make a machine that will be proud of us..."', 
                      font=("Arial", 16, "italic"), text_color="#a4b0be").pack()
        ctk.CTkLabel(quote_frame, text="- Danny Hillis", 
                      font=("Arial", 14, "bold"), text_color="#7f8c8d").pack(pady=(5, 0))

    def create_mini_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=color, height=80, corner_radius=10)
        card.pack(side="left", expand=True, fill="both", padx=5)
        
        ctk.CTkLabel(card, text=title, font=("Arial", 10, "bold"), text_color="white").pack(pady=(15,0))
        ctk.CTkLabel(card, text=value, font=("Arial", 20, "bold"), text_color="white").pack(pady=(0,10))

    # ==========================
    # ADD STUDENT
    # ==========================
    def show_add_student(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="ADD NEW RECORD", font=("Impact", 22), text_color="#ecf0f1").pack(pady=(20, 10))

        form = ctk.CTkFrame(self.main_frame, width=400, fg_color="#222")
        form.pack(pady=5, padx=20)

        self.id_entry = self.add_field(form, "Student ID")
        self.name_entry = self.add_field(form, "Full Name")
        self.mid_entry = self.add_field(form, "Midterm (0-100)")
        self.final_entry = self.add_field(form, "Final (0-100)")
        self.assign_entry = self.add_field(form, "Assignment (0-100)")

        ctk.CTkButton(form, text="SAVE", height=35, width=200, fg_color="#2ecc71", hover_color="#27ae60",
                      font=("Arial", 13, "bold"), command=self.save_student).pack(pady=20)

    def add_field(self, parent, placeholder):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300, height=35, font=("Arial", 12))
        entry.pack(pady=5, padx=10)
        return entry

    def save_student(self):
        try:
            sid = int(self.id_entry.get())
            if any(s.id == sid for s in students_list):
                messagebox.showerror("Error", "ID already exists!")
                return
            s = Student(sid, self.name_entry.get(), float(self.mid_entry.get()), float(self.final_entry.get()), float(self.assign_entry.get()))
            s.compute_final()
            s.compute_grade()
            students_list.append(s)
            messagebox.showinfo("Success", "Student Added!")
            self.show_view_records()
        except ValueError:
            messagebox.showerror("Error", "Invalid Input")

    # ==========================
    # VIEW RECORDS
    # ==========================
    def show_view_records(self):
        self.clear_frame()
        
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(20, 10))
        ctk.CTkLabel(top, text="RECORDS", font=("Impact", 22)).pack(side="left")
        ctk.CTkButton(top, text="Sort by Grade", height=25, font=("Arial", 11), command=self.sort_records).pack(side="right")

        scroll_area = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scroll_area.pack(fill="both", expand=True, padx=20, pady=5)

        if not students_list:
            ctk.CTkLabel(scroll_area, text="No Data").pack(pady=20)

        for s in students_list:
            self.create_slim_row(scroll_area, s)

    def create_slim_row(self, parent, student):
        row = ctk.CTkFrame(parent, fg_color="#2d3436", height=45, corner_radius=8)
        row.pack(fill="x", pady=3)
        
        color = "#2ecc71" if student.grade == "A" else ("#e74c3c" if student.grade == "F" else "#f1c40f")
        
        ctk.CTkFrame(row, fg_color=color, width=5, height=30).pack(side="left", padx=(10, 5), pady=5)

        ctk.CTkLabel(row, text=f"{student.name}", font=("Arial", 13, "bold"), width=120, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(row, text=f"ID: {student.id}", font=("Arial", 11), text_color="gray").pack(side="left", padx=5)
        
        ctk.CTkButton(row, text="✖", width=25, height=25, fg_color="transparent", hover_color="#c0392b", text_color="#e74c3c",
                      command=lambda s=student: self.delete_student(s)).pack(side="right", padx=10)
        
        ctk.CTkLabel(row, text=f"{student.grade}", font=("Arial", 14, "bold"), text_color=color).pack(side="right", padx=10)
        ctk.CTkLabel(row, text=f"{student.final_score:.1f}", font=("Arial", 12)).pack(side="right", padx=5)

    def sort_records(self):
        students_list.sort(key=lambda x: x.final_score, reverse=True)
        self.show_view_records()

    def delete_student(self, student):
        if messagebox.askyesno("Delete", f"Remove {student.name}?"):
            students_list.remove(student)
            self.show_view_records()

    # ==========================
    # ANALYTICS
    # ==========================
    def show_visualization(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="ANALYTICS HUB", font=("Impact", 22)).pack(pady=10)

        if not students_list:
            ctk.CTkLabel(self.main_frame, text="No Data").pack()
            return

        tabs = ctk.CTkTabview(self.main_frame)
        tabs.pack(fill="both", expand=True, padx=20, pady=5)

        tab_grade = tabs.add("Grades")
        tab_pass = tabs.add("Pass/Fail")
        tab_avg = tabs.add("Averages")

        # Graph 1
        grades = [s.grade for s in students_list]
        counts = {g: grades.count(g) for g in ["A", "B", "C", "D", "F"]}
        
        fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=80)
        fig1.patch.set_facecolor('#2b2b2b')
        colors = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']
        ax1.pie([counts[k] for k in counts], labels=counts.keys(), colors=colors, autopct='%1.1f%%', textprops={'color':"white"})
        ax1.add_artist(plt.Circle((0,0),0.60,fc='#2b2b2b'))
        self.embed_graph(tab_grade, fig1)

        # Graph 2
        passed = len([s for s in students_list if s.grade != "F"])
        failed = len(students_list) - passed
        
        fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=80)
        fig2.patch.set_facecolor('#2b2b2b')
        ax2.pie([passed, failed], labels=["Pass", "Fail"], colors=['#2ecc71', '#e74c3c'], autopct='%1.1f%%', textprops={'color':"white"})
        self.embed_graph(tab_pass, fig2)

        # Graph 3
        avgs = {
            "Mid": sum(s.midterm for s in students_list)/len(students_list),
            "Final": sum(s.final for s in students_list)/len(students_list),
            "Assgn": sum(s.assignment for s in students_list)/len(students_list)
        }
        fig3, ax3 = plt.subplots(figsize=(4, 3), dpi=80)
        fig3.patch.set_facecolor('#2b2b2b')
        ax3.set_facecolor('#2b2b2b')
        ax3.bar(avgs.keys(), avgs.values(), color="#3498db")
        ax3.tick_params(colors='white')
        self.embed_graph(tab_avg, fig3)

    def embed_graph(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def exit_app(self):
        save_data()
        self.destroy()

if __name__ == "__main__":
    app = StudentApp()
    app.mainloop()