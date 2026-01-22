import tkinter as tk

from tkinter import messagebox, ttk
from app import Event, EventRepository, WeatherService

class EventPlannerGUI:
    def __init__(self, root, repo, weather_svc):
        self.root = root
        self.repo = repo
        self.weather_svc = weather_svc
        self.root.title("Weather-Aware Event Planner")
        self.root.geometry("600x450")

        # --- UI Elements ---
        # Input Section
        tk.Label(root, text="ID:").grid(row=0, column=0, padx=5, pady=5)

        self.ent_id = tk.Entry(root)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Title:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_title = tk.Entry(root)
        self.ent_title.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="City:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_city = tk.Entry(root)
        self.ent_city.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Add Event", command=self.add_event).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_event).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Check Weather", command=self.check_weather).pack(side=tk.LEFT, padx=5)

        # List Display (Treeview)
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "City"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("City", text="City")

        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.refresh_list()

    def add_event(self):
        try:
            eid = int(self.ent_id.get())
            title = self.ent_title.get()
            city = self.ent_city.get()
            
            if self.repo.get_by_id(eid):
                messagebox.showerror("Error", f"Event ID {eid} already exists!")
                return

            self.repo.add_or_update(Event(eid, title, city))
            self.refresh_list()
            self.clear_entries()
        except ValueError:
            messagebox.showwarning("Input Error", "ID must be a number!")

    def delete_event(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select", "Please select an event from the list.")

            return
        

        item_values = self.tree.item(selected_item)['values']
        event_id = item_values[0]
        
        if self.repo.delete_by_id(event_id):
            self.refresh_list()
            messagebox.showinfo("Success", f"Event {event_id} deleted.")

    def check_weather(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select", "Please select an event to check weather.")
            return
        
        city = self.tree.item(selected_item)['values'][2]
        weather = self.weather_svc.get_weather(city)
        messagebox.showinfo("Weather Report", f"Weather in {city}:\n{weather}")


    def refresh_list(self):
        """Update the table with data from the database."""
        for i in self.tree.get_children():

            self.tree.delete(i)
        for event in self.repo.get_all():
            self.tree.insert('', tk.END, values=(event.id, event.title, event.city))

    def clear_entries(self):

        self.ent_id.delete(0, tk.END)
        self.ent_title.delete(0, tk.END)
        self.ent_city.delete(0, tk.END)

if __name__ == "__main__":
    app_repo = EventRepository("events.db")
    app_weather = WeatherService()
    root = tk.Tk()
    gui = EventPlannerGUI(root, app_repo, app_weather)
    root.mainloop()
