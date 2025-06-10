import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class AppIdeasViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("App Ideas Viewer")
        self.root.geometry("1000x700")
        
        # Data storage
        self.ideas = []
        self.current_index = 0
        self.filtered_ideas = []
        
        # Create the GUI
        self.create_widgets()
        
        # Try to load the JSON file automatically if it exists
        if os.path.exists("LLM_Friendly_App_Ideas.json"):
            self.load_json_file("LLM_Friendly_App_Ideas.json")
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # File loading frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Load JSON File", command=self.load_file).pack(side=tk.LEFT)
        self.file_label = ttk.Label(file_frame, text="No file loaded")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Goals frame
        goals_frame = ttk.LabelFrame(main_frame, text="Goals & Requirements", padding="10")
        goals_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        goals_frame.columnconfigure(0, weight=1)
        
        goals_text = tk.Text(goals_frame, height=8, wrap=tk.WORD, font=('Arial', 10, 'bold'), 
                            bg='#f0f8ff', fg='#2c3e50', relief='sunken', bd=1, 
                            state='disabled', padx=10, pady=5)
        goals_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure goals text formatting
        goals_text.tag_configure("goal_title", font=('Arial', 11, 'bold'), foreground='#e74c3c')
        goals_text.tag_configure("section_header", font=('Arial', 10, 'bold'), foreground='#3498db')
        goals_text.tag_configure("bullet", font=('Arial', 10), foreground='#2c3e50')
        
        # Load and display goals
        self.load_goals(goals_text)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(row=0, column=2)
        
        # Left panel - Ideas list
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        ttk.Label(left_frame, text="Ideas List:").grid(row=0, column=0, sticky=tk.W)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.ideas_listbox = tk.Listbox(listbox_frame, width=40)
        self.ideas_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.ideas_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        
        listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.ideas_listbox.yview)
        listbox_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.ideas_listbox.configure(yscrollcommand=listbox_scrollbar.set)
        
        # Right panel - Idea details
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Navigation frame
        nav_frame = ttk.Frame(right_frame)
        nav_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(nav_frame, text="Previous", command=self.previous_idea).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Next", command=self.next_idea).pack(side=tk.LEFT, padx=(5, 0))
        
        self.counter_label = ttk.Label(nav_frame, text="0 / 0")
        self.counter_label.pack(side=tk.RIGHT)
        
        # Details display
        details_frame = ttk.Frame(right_frame)
        details_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, font=('Arial', 10))
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        details_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        # Configure text tags for formatting
        self.details_text.tag_configure("title", font=('Arial', 14, 'bold'), foreground='blue')
        self.details_text.tag_configure("field", font=('Arial', 10, 'bold'), foreground='darkgreen')
        self.details_text.tag_configure("content", font=('Arial', 10))
    
    def load_goals(self, goals_text_widget):
        """Load and display goals from goals.md file with formatting"""
        try:
            goals_text_widget.config(state='normal')
            goals_text_widget.delete(1.0, tk.END)
            
            if os.path.exists("goals.md"):
                with open("goals.md", 'r', encoding='utf-8') as f:
                    goals_content = f.read()
                
                # Parse and format the content
                lines = goals_content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('Goal:'):
                        goals_text_widget.insert(tk.END, line + '\n\n', "goal_title")
                    elif line.startswith('Apps must have'):
                        goals_text_widget.insert(tk.END, line + '\n', "section_header")
                    elif line.startswith('Technical goals'):
                        goals_text_widget.insert(tk.END, '\n' + line + '\n', "section_header")
                    elif line.startswith(('1.', '2.', '3.', '-')):
                        goals_text_widget.insert(tk.END, line + '\n', "bullet")
                    elif line:
                        goals_text_widget.insert(tk.END, line + '\n', "bullet")
                    else:
                        goals_text_widget.insert(tk.END, '\n')
            else:
                # Default formatted goals
                goals_text_widget.insert(tk.END, "Goal: $800 AUD/week as soon as possible.\n\n", "goal_title")
                goals_text_widget.insert(tk.END, "Apps must have a trifecta:\n", "section_header")
                goals_text_widget.insert(tk.END, "1. Good marketing (Short Form Videos following Desmond's rules)\n", "bullet")
                goals_text_widget.insert(tk.END, "2. Good monetisation model\n", "bullet")
                goals_text_widget.insert(tk.END, "3. Good retention technique\n\n", "bullet")
                goals_text_widget.insert(tk.END, "Technical goals:\n", "section_header")
                goals_text_widget.insert(tk.END, "Context7, TaskMaster, Expo dev build, Mermaid diagrams, scalable stack, social login, OTA, Expo web, GitHub deployment, GPS", "bullet")
                
            goals_text_widget.config(state='disabled')
                
        except Exception as e:
            # Fallback in case of error
            goals_text_widget.config(state='normal')
            goals_text_widget.delete(1.0, tk.END)
            goals_text_widget.insert(1.0, f"Error loading goals: {str(e)}")
            goals_text_widget.config(state='disabled')
    
    def load_file(self):
        """Load JSON file through file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.load_json_file(file_path)
    
    def load_json_file(self, file_path):
        """Load and parse JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.ideas = json.load(f)
            
            self.filtered_ideas = self.ideas.copy()
            self.current_index = 0
            
            # Update file label
            self.file_label.config(text=f"Loaded: {os.path.basename(file_path)} ({len(self.ideas)} ideas)")
            
            # Populate listbox
            self.update_listbox()
            
            # Display first idea
            if self.ideas:
                self.display_idea(0)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def update_listbox(self):
        """Update the ideas listbox with current filtered ideas"""
        self.ideas_listbox.delete(0, tk.END)
        
        for i, idea in enumerate(self.filtered_ideas):
            order = idea.get('Order', 'N/A')
            name = idea.get('Name', 'Unnamed')
            display_text = f"{order}. {name}" if order != 'N/A' and order is not None else f"   {name}"
            self.ideas_listbox.insert(tk.END, display_text)
        
        # Update counter
        total = len(self.filtered_ideas)
        current = self.current_index + 1 if total > 0 else 0
        self.counter_label.config(text=f"{current} / {total}")
    
    def on_listbox_select(self, event):
        """Handle listbox selection"""
        selection = self.ideas_listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.display_idea(self.current_index)
    
    def display_idea(self, index):
        """Display idea details in the text widget"""
        if not self.filtered_ideas or index < 0 or index >= len(self.filtered_ideas):
            self.details_text.delete(1.0, tk.END)
            return
        
        idea = self.filtered_ideas[index]
        
        # Clear previous content
        self.details_text.delete(1.0, tk.END)
        
        # Title
        name = idea.get('Name', 'Unnamed Idea')
        order = idea.get('Order', 'N/A')
        title = f"{order}. {name}" if order != 'N/A' and order is not None else name
        self.details_text.insert(tk.END, title + "\n\n", "title")
        
        # Display all fields
        fields = [
            ('Origin', 'Origin'),
            ('Keywords', 'Keywords'),
            ('Marketing', 'Marketing'),
            ('Functionality', 'Functionality'),
            ('Skills to Learn', 'SkillsToLearn'),
            ('Tech Stack', 'TechStack'),
            ('Desire', 'desire'),
            ('Retention', 'retention')
        ]
        
        for display_name, field_key in fields:
            value = idea.get(field_key, '')
            if value:  # Only show fields with content
                self.details_text.insert(tk.END, f"{display_name}:\n", "field")
                self.details_text.insert(tk.END, f"{value}\n\n", "content")
        
        # Highlight current item in listbox
        self.ideas_listbox.selection_clear(0, tk.END)
        self.ideas_listbox.selection_set(index)
        self.ideas_listbox.see(index)
        
        # Update counter
        total = len(self.filtered_ideas)
        current = index + 1 if total > 0 else 0
        self.counter_label.config(text=f"{current} / {total}")
    
    def previous_idea(self):
        """Navigate to previous idea"""
        if self.filtered_ideas and self.current_index > 0:
            self.current_index -= 1
            self.display_idea(self.current_index)
    
    def next_idea(self):
        """Navigate to next idea"""
        if self.filtered_ideas and self.current_index < len(self.filtered_ideas) - 1:
            self.current_index += 1
            self.display_idea(self.current_index)
    
    def on_search_change(self, *args):
        """Handle search text changes"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.filtered_ideas = self.ideas.copy()
        else:
            self.filtered_ideas = []
            for idea in self.ideas:
                # Search in multiple fields
                searchable_text = ' '.join([
                    str(idea.get('Name', '')),
                    str(idea.get('Keywords', '')),
                    str(idea.get('Functionality', '')),
                    str(idea.get('Marketing', '')),
                    str(idea.get('SkillsToLearn', '')),
                    str(idea.get('TechStack', ''))
                ]).lower()
                
                if search_term in searchable_text:
                    self.filtered_ideas.append(idea)
        
        self.current_index = 0
        self.update_listbox()
        
        if self.filtered_ideas:
            self.display_idea(0)
        else:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "No ideas found matching your search.", "content")
    
    def clear_search(self):
        """Clear search and show all ideas"""
        self.search_var.set('')

def main():
    root = tk.Tk()
    app = AppIdeasViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 