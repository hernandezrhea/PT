
import tkinter as tk
from tkinter import ttk, messagebox

BG = "#F3F7FF"
BLUE = "#3B82F6"
DARK_BLUE = "#1E40AF"
LIGHT_BLUE = "#DBEAFE"
PALE_BLUE = "#EFF6FF"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
BORDER = "#CBDCF5"
SELECTED = "#2563EB"


def calculate_movement(path):
    movements = []
    total = 0

    for i in range(1, len(path)):
        movement = abs(path[i] - path[i - 1])
        movements.append(movement)
        total += movement

    return movements, total


def fcfs(head, requests):
    path = [head] + requests
    movements, total = calculate_movement(path)

    return {
        "name": "FCFS",
        "sequence": requests,
        "path": path,
        "movements": movements,
        "total": total
    }


def sstf(head, requests):
    remaining = requests.copy()
    sequence = []
    current = head

    while remaining:
        nearest = min(
            remaining,
            key=lambda request: (abs(request - current), request)
        )

        sequence.append(nearest)
        remaining.remove(nearest)
        current = nearest

    path = [head] + sequence
    movements, total = calculate_movement(path)

    return {
        "name": "SSTF",
        "sequence": sequence,
        "path": path,
        "movements": movements,
        "total": total
    }


# ================= SCAN ALGORITHM =================

def scan(head, requests, minimum, maximum):
    # Fixed direction: UPWARD
    left = sorted(
        [r for r in requests if r < head],
        reverse=True
    )

    right = sorted(
        [r for r in requests if r > head]
    )

    at_head = [r for r in requests if r == head]

    sequence = at_head + right + left
    path = [head] + at_head + right

    # Move to the maximum cylinder before reversing
    # if there are requests on the left side.
    if left:
        if path[-1] != maximum:
            path.append(maximum)

        path += left

    movements, total = calculate_movement(path)

    return {
        "name": "SCAN (Elevator)",
        "sequence": sequence,
        "path": path,
        "movements": movements,
        "total": total
    }


# ================= MAIN GUI =================

class DiskSchedulingGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator")
        self.root.geometry("1100x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)

        self.selected_index = 0

        self.algorithm_names = [
            "FCFS",
            "SSTF",
            "SCAN (Elevator)",
            "COMPARE"
        ]

        self.algorithm_buttons = []

        self.create_widgets()
        self.update_selection()

        # Keyboard navigation across the entire window
        self.root.bind_all("<Up>", self.move_up)
        self.root.bind_all("<Down>", self.move_down)
        self.root.bind_all("<Left>", self.move_left)
        self.root.bind_all("<Right>", self.move_right)
        self.root.bind_all("<Return>", self.select_algorithm)
        self.root.bind_all("<KP_Enter>", self.select_algorithm)

    # ================= CREATE INTERFACE =================

    def create_widgets(self):

        # Header
        header = tk.Frame(self.root, bg=BLUE, height=85)
        header.pack(fill="x", padx=25, pady=(22, 18))
        header.pack_propagate(False)

        tk.Label(
            header,
            text="DISK SCHEDULING",
            bg=BLUE,
            fg=WHITE,
            font=("Segoe UI", 24, "bold")
        ).pack(expand=True)

        # Main content - two-column layout
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # LEFT SIDE
        left_side = tk.Frame(main, bg=BG)
        left_side.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10)
        )

        # Disk Configuration Panel
        config_panel = tk.Frame(
            left_side,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        config_panel.pack(fill="x", pady=(0, 15))

        tk.Label(
            config_panel,
            text="DISK CONFIGURATION",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 12))

        self.head_var = tk.StringVar(value="50")
        self.max_var = tk.StringVar(value="199")
        self.min_var = tk.StringVar(value="0")

        self.queue_var = tk.StringVar(
            value="82, 170, 43, 140, 24, 16, 190"
        )

        self.add_input(
            config_panel,
            "Initial Head Position:",
            self.head_var
        )

        self.add_input(
            config_panel,
            "Maximum Cylinder:",
            self.max_var
        )

        self.add_input(
            config_panel,
            "Minimum Cylinder:",
            self.min_var
        )

        self.add_input(
            config_panel,
            "Request Queue:",
            self.queue_var
        )

        # Bottom spacing for configuration panel
        tk.Frame(
            config_panel,
            bg=WHITE,
            height=15
        ).pack(fill="x")

        # Algorithm Panel
        algo_panel = tk.Frame(
            left_side,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        algo_panel.pack(fill="both", expand=True)

        tk.Label(
            algo_panel,
            text="SELECT ALGORITHM",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 12))

        button_grid = tk.Frame(algo_panel, bg=WHITE)

        button_grid.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        button_grid.grid_columnconfigure(0, weight=1)
        button_grid.grid_columnconfigure(1, weight=1)
        button_grid.grid_rowconfigure(0, weight=1)
        button_grid.grid_rowconfigure(1, weight=1)

        for i, name in enumerate(self.algorithm_names):

            button = tk.Button(
                button_grid,
                text=name,
                command=lambda index=i: self.run_selected(index),
                bg=PALE_BLUE,
                fg=DARK_BLUE,
                activebackground=LIGHT_BLUE,
                activeforeground=DARK_BLUE,
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=10,
                pady=18
            )

            button.grid(
                row=i // 2,
                column=i % 2,
                sticky="nsew",
                padx=6,
                pady=6
            )

            self.algorithm_buttons.append(button)

        # RIGHT SIDE - RESULTS
        results_panel = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        results_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        results_panel.grid_columnconfigure(0, weight=1)
        results_panel.grid_rowconfigure(3, weight=1)

        # Results title
        tk.Label(
            results_panel,
            text="RESULTS",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 17, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(18, 10)
        )

        # Summary area
        summary_frame = tk.Frame(results_panel, bg=WHITE)

        summary_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 12)
        )

        summary_frame.grid_columnconfigure(0, weight=1)

        self.output = tk.Text(
            summary_frame,
            height=9,
            bg=PALE_BLUE,
            fg=TEXT,
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            padx=15,
            pady=12,
            insertbackground=DARK_BLUE
        )

        summary_scrollbar = tk.Scrollbar(
            summary_frame,
            command=self.output.yview
        )

        self.output.configure(
            yscrollcommand=summary_scrollbar.set
        )

        self.output.grid(row=0, column=0, sticky="nsew")
        summary_scrollbar.grid(row=0, column=1, sticky="ns")

        self.output.insert(
            "1.0",
            "Welcome to Disk Scheduling Simulator!\n\n"
            "Enter your disk configuration on the left.\n\n"
            "Select an algorithm to view its results here.\n\n"
            "KEYBOARD CONTROLS\n"
            "↑ ↓ ← →  Navigate algorithms\n"
            "ENTER      Select algorithm\n\n"
            "AVAILABLE ALGORITHMS\n"
            "• FCFS\n"
            "• SSTF\n"
            "• SCAN (Elevator)\n"
            "• Compare All"
        )

        self.output.config(state="disabled")

        # Table title
        tk.Label(
            results_panel,
            text="HEAD MOVEMENT TABLE",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 8)
        )

        # Table
        table_frame = tk.Frame(results_panel, bg=WHITE)

        table_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(
            table_frame,
            columns=("step", "movement", "distance"),
            show="headings",
            height=8
        )

        self.table.heading(
            "step",
            text="STEP",
            anchor="center"
        )

        self.table.heading(
            "movement",
            text="HEAD MOVEMENT",
            anchor="center"
        )

        self.table.heading(
            "distance",
            text="DISTANCE",
            anchor="center"
        )

        self.table.column(
            "step",
            width=65,
            anchor="center"
        )

        self.table.column(
            "movement",
            width=190,
            anchor="center"
        )

        self.table.column(
            "distance",
            width=90,
            anchor="center"
        )

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=table_scrollbar.set
        )

        self.table.grid(row=0, column=0, sticky="nsew")
        table_scrollbar.grid(row=0, column=1, sticky="ns")

        self.table.tag_configure(
            "even",
            background=WHITE
        )

        self.table.tag_configure(
            "odd",
            background=PALE_BLUE
        )

        # Footer
        footer = tk.Frame(self.root, bg=BLUE, height=48)
        footer.pack(fill="x", padx=25, pady=(0, 18))
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="PLATFORM TECHNOLOGY",
            bg=BLUE,
            fg=WHITE,
            font=("Segoe UI", 11, "bold")
        ).pack(expand=True)

    # ================= INPUT FIELDS =================

    def add_input(self, parent, label_text, variable):

        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", padx=20, pady=5)

        tk.Label(
            row,
            text=label_text,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10),
            width=21,
            anchor="w"
        ).pack(side="left")

        entry = tk.Entry(
            row,
            textvariable=variable,
            bg=PALE_BLUE,
            fg=TEXT,
            insertbackground=DARK_BLUE,
            relief="flat",
            font=("Segoe UI", 10),
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE
        )

        entry.pack(
            side="right",
            fill="x",
            expand=True,
            ipady=7
        )

    # ================= KEYBOARD NAVIGATION =================

    def update_selection(self):

        for i, button in enumerate(self.algorithm_buttons):

            if i == self.selected_index:
                button.config(
                    bg=SELECTED,
                    fg=WHITE,
                    activebackground=DARK_BLUE,
                    activeforeground=WHITE
                )

            else:
                button.config(
                    bg=PALE_BLUE,
                    fg=DARK_BLUE,
                    activebackground=LIGHT_BLUE,
                    activeforeground=DARK_BLUE
                )

    def move_up(self, event=None):
        self.selected_index = (self.selected_index - 2) % 4
        self.update_selection()
        return "break"

    def move_down(self, event=None):
        self.selected_index = (self.selected_index + 2) % 4
        self.update_selection()
        return "break"

    def move_left(self, event=None):
        self.selected_index = (self.selected_index - 1) % 4
        self.update_selection()
        return "break"

    def move_right(self, event=None):
        self.selected_index = (self.selected_index + 1) % 4
        self.update_selection()
        return "break"

    def select_algorithm(self, event=None):
        self.run_selected(self.selected_index)
        return "break"

    def run_selected(self, index):

        self.selected_index = index
        self.update_selection()

        if index == 0:
            self.run_algorithm("FCFS")

        elif index == 1:
            self.run_algorithm("SSTF")

        elif index == 2:
            self.run_algorithm("SCAN")

        elif index == 3:
            self.compare_all()

    # ================= GET INPUTS =================

    def get_inputs(self):

        try:
            head = int(self.head_var.get())
            maximum = int(self.max_var.get())
            minimum = int(self.min_var.get())

            requests = [
                int(x.strip())
                for x in self.queue_var.get().split(",")
                if x.strip()
            ]

            if minimum >= maximum:
                raise ValueError(
                    "Minimum cylinder must be less than maximum cylinder."
                )

            if not minimum <= head <= maximum:
                raise ValueError(
                    "Initial head position is outside the disk range."
                )

            if not requests:
                raise ValueError(
                    "Please enter at least one request."
                )

            for request in requests:

                if not minimum <= request <= maximum:
                    raise ValueError(
                        f"Request {request} is outside the disk range."
                    )

            return head, requests, minimum, maximum

        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
            return None

    # ================= DISPLAY HELPERS =================

    def clear_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

    def display_summary(self, content):

        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, content)
        self.output.config(state="disabled")

    def display_movement_table(self, result):

        self.clear_table()

        for i, movement in enumerate(result["movements"]):

            start = result["path"][i]
            end = result["path"][i + 1]

            tag = "even" if i % 2 == 0 else "odd"

            self.table.insert(
                "",
                "end",
                values=(
                    i + 1,
                    f"{start} → {end}",
                    movement
                ),
                tags=(tag,)
            )

        self.set_normal_table_headings()

    def set_normal_table_headings(self):

        self.table.heading(
            "step",
            text="STEP",
            anchor="center"
        )

        self.table.heading(
            "movement",
            text="HEAD MOVEMENT",
            anchor="center"
        )

        self.table.heading(
            "distance",
            text="DISTANCE",
            anchor="center"
        )

    # ================= RUN ALGORITHMS =================

    def run_algorithm(self, algorithm):

        data = self.get_inputs()

        if data is None:
            return

        head, requests, minimum, maximum = data

        if algorithm == "FCFS":
            result = fcfs(head, requests)

        elif algorithm == "SSTF":
            result = sstf(head, requests)

        else:
            result = scan(
                head,
                requests,
                minimum,
                maximum
            )

        self.display_result(result)

    # ================= DISPLAY SINGLE RESULT =================

    def display_result(self, result):

        self.set_normal_table_headings()

        summary = (
            f"{result['name']}\n\n"
            "SERVICE SEQUENCE\n\n"
            f"{' → '.join(map(str, result['sequence']))}\n\n"
            f"TOTAL HEAD MOVEMENT: {result['total']} cylinders\n\n"
            "FULL HEAD PATH\n\n"
            f"{' → '.join(map(str, result['path']))}"
        )

        self.display_summary(summary)
        self.display_movement_table(result)

    # ================= COMPARE ALL =================

    def compare_all(self):

        data = self.get_inputs()

        if data is None:
            return

        head, requests, minimum, maximum = data

        results = [
            fcfs(head, requests),
            sstf(head, requests),
            scan(head, requests, minimum, maximum)
        ]

        lowest = min(
            result["total"] for result in results
        )

        winners = [
            result["name"]
            for result in results
            if result["total"] == lowest
        ]

        summary = "ALGORITHM COMPARISON\n\n"

        summary += (
            f"{'ALGORITHM':<22}"
            f"{'TOTAL MOVEMENT':>16}\n\n"
        )

        for result in results:

            summary += (
                f"{result['name']:<22}"
                f"{result['total']:>16} cylinders\n"
            )

        summary += (
            "\nMOST EFFICIENT ALGORITHM\n\n"
            f"{', '.join(winners)}\n\n"
            f"Lowest Movement: {lowest} cylinders"
        )

        self.display_summary(summary)

        # Comparison table
        self.clear_table()

        self.table.heading(
            "step",
            text="ALGORITHM",
            anchor="center"
        )

        self.table.heading(
            "movement",
            text="HEAD MOVEMENT",
            anchor="center"
        )

        self.table.heading(
            "distance",
            text="DISTANCE",
            anchor="center"
        )

        row_number = 0

        for result in results:

            for i, movement in enumerate(result["movements"]):

                start = result["path"][i]
                end = result["path"][i + 1]

                tag = (
                    "even" if row_number % 2 == 0
                    else "odd"
                )

                self.table.insert(
                    "",
                    "end",
                    values=(
                        result["name"],
                        f"{start} → {end}",
                        movement
                    ),
                    tags=(tag,)
                )

                row_number += 1


# ================= RUN PROGRAM =================

if __name__ == "__main__":

    root = tk.Tk()
    app = DiskSchedulingGUI(root)
    root.mainloop()
