import random
import tkinter as tk
from tkinter import messagebox, ttk


class ReDayMobileApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Window Setup (Mobile/Tablet Ratio)
        self.title("Re:Day - AI Fitness & Focus")
        self.geometry("400x820")
        self.resizable(False, False)

        # User Profile & App Lock State
        self.user_data = {
            "age": "",
            "weight": "",
            "weight_unit": "kg",
            "height": "",
            "height_unit": "cm",
            "notifications": False,
        }

        # App Blocker List (True = Locked by User)
        self.distracting_apps = {
            "Instagram": tk.BooleanVar(value=True),
            "YouTube": tk.BooleanVar(value=True),
            "TikTok": tk.BooleanVar(value=False),
            "Games": tk.BooleanVar(value=False),
        }

        # Daily Tasks State
        self.daily_tasks = [
            {"title": "💧 Drink 2L Water", "completed": False},
            {"title": "🧘 5-Min Shoulder Stretch", "completed": False},
            {"title": "🚶 10-Min Posture Walk", "completed": False},
            {"title": "📱 Desk Break Pose Scan", "completed": False},
        ]

        # Supported Scans
        self.scans = ["Posture Check", "Push-up Form", "Squat Depth", "Plank Hold"]

        # Weekly Progress Data
        self.weekly_scores = [78, 82, 85, 80, 88, 92, 95]
        self.days = ["M", "T", "W", "T", "F", "S", "S"]

        # Screen Time Earned (Minutes)
        self.screen_time_earned_min = 0.0

        # Theme Colors
        self.bg_color = "#1E1E2E"
        self.card_color = "#2B2B3D"
        self.accent_color = "#74C7EC"
        self.fg_color = "#CDD6F4"
        self.text_dim = "#A6ADC8"
        self.danger_color = "#F38BA8"

        self.configure(bg=self.bg_color)

        # Main Navigation Container
        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        # Start App at Onboarding
        self.show_onboarding_screen()

    # ----------------------------------------------------
    # BLOOP BUTTON ANIMATION HELPER
    # ----------------------------------------------------
    def create_bloop_button(
        self,
        parent,
        text,
        command,
        bg_color=None,
        fg_color=None,
        font=("Helvetica", 10, "bold"),
    ):
        bg = bg_color if bg_color else self.card_color
        fg = fg_color if fg_color else self.fg_color

        container = tk.Frame(parent, bg=self.bg_color)
        container.pack_propagate(False)

        btn = tk.Button(
            container,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            activebackground=self.accent_color,
            activeforeground="#11111B",
            bd=0,
            relief="flat",
        )
        btn.configure(command=lambda: self.animate_bloop(btn, command, step=0))
        btn.pack(fill="both", expand=True)

        return container, btn

    def animate_bloop(self, btn, callback_command, step):
        paddings = [2, 5, 2, 0]
        if step < len(paddings):
            p = paddings[step]
            btn.pack_forget()
            btn.pack(fill="both", expand=True, padx=p, pady=p)
            self.after(25, lambda: self.animate_bloop(btn, callback_command, step + 1))
        else:
            if callback_command:
                callback_command()

    # ----------------------------------------------------
    # SCREEN 1: ONBOARDING SCREEN
    # ----------------------------------------------------
    def show_onboarding_screen(self):
        self.clear_container()

        frame = tk.Frame(self.container, bg=self.bg_color, padx=25, pady=20)
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Re:Day 🔥",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        title.pack(pady=(15, 0))

        tagline = tk.Label(
            frame,
            text="Reset Your Posture • Lock Distractions",
            font=("Helvetica", 10, "italic"),
            bg=self.bg_color,
            fg=self.accent_color,
        )
        tagline.pack(pady=(2, 15))

        sub = tk.Label(
            frame,
            text="Set up your profile to get started",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.text_dim,
        )
        sub.pack(pady=(0, 20))

        # 1. Age Entry
        tk.Label(
            frame,
            text="Age:",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(anchor="w", pady=(10, 2))
        self.age_entry = tk.Entry(
            frame,
            font=("Helvetica", 12),
            bg=self.card_color,
            fg=self.fg_color,
            bd=0,
            insertbackground=self.fg_color,
        )
        self.age_entry.insert(0, "22")
        self.age_entry.pack(fill="x", ipady=8)

        # 2. Weight Entry
        tk.Label(
            frame,
            text="Weight:",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(anchor="w", pady=(15, 2))
        w_frame = tk.Frame(frame, bg=self.bg_color)
        w_frame.pack(fill="x")

        self.weight_entry = tk.Entry(
            w_frame,
            font=("Helvetica", 12),
            bg=self.card_color,
            fg=self.fg_color,
            bd=0,
            insertbackground=self.fg_color,
        )
        self.weight_entry.insert(0, "65")
        self.weight_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.weight_unit_var = tk.StringVar(value="kg")
        w_unit = ttk.Combobox(
            w_frame,
            textvariable=self.weight_unit_var,
            values=["kg", "lbs"],
            width=5,
            state="readonly",
        )
        w_unit.pack(side="right", padx=(10, 0), ipady=5)

        # 3. Height Entry
        tk.Label(
            frame,
            text="Height:",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(anchor="w", pady=(15, 2))
        h_frame = tk.Frame(frame, bg=self.bg_color)
        h_frame.pack(fill="x")

        self.height_entry = tk.Entry(
            h_frame,
            font=("Helvetica", 12),
            bg=self.card_color,
            fg=self.fg_color,
            bd=0,
            insertbackground=self.fg_color,
        )
        self.height_entry.insert(0, "175")
        self.height_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.height_unit_var = tk.StringVar(value="cm")
        h_unit = ttk.Combobox(
            h_frame,
            textvariable=self.height_unit_var,
            values=["cm", "inch"],
            width=5,
            state="readonly",
        )
        h_unit.pack(side="right", padx=(10, 0), ipady=5)

        # Submit Bloop Button
        start_container, _ = self.create_bloop_button(
            frame,
            text="Start Re:Day App 🚀",
            command=self.save_onboarding_and_start,
            bg_color=self.accent_color,
            fg_color="#11111B",
            font=("Helvetica", 12, "bold"),
        )
        start_container.configure(height=45)
        start_container.pack(fill="x", pady=35)

    def save_onboarding_and_start(self):
        self.user_data["age"] = self.age_entry.get()
        self.user_data["weight"] = self.weight_entry.get()
        self.user_data["weight_unit"] = self.weight_unit_var.get()
        self.user_data["height"] = self.height_entry.get()
        self.user_data["height_unit"] = self.height_unit_var.get()

        self.show_home_screen()
        self.after(500, self.prompt_notification_permission)

    def prompt_notification_permission(self):
        response = messagebox.askyesno(
            "Allow Notifications",
            "Re:Day would like to send you notifications for posture breaks and focus alerts.\n\nAllow notifications?",
        )
        self.user_data["notifications"] = response

    # ----------------------------------------------------
    # SCREEN 2: MAIN DASHBOARD
    # ----------------------------------------------------
    def show_home_screen(self):
        self.clear_container()

        frame = tk.Frame(self.container, bg=self.bg_color, padx=15, pady=10)
        frame.pack(fill="both", expand=True)

        # Header Bar
        header = tk.Frame(frame, bg=self.bg_color)
        header.pack(fill="x", pady=(5, 5))

        tk.Label(
            header,
            text="Re:Day Dashboard",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(side="left")

        settings_container, _ = self.create_bloop_button(
            header,
            text="⚙️",
            command=self.show_settings_screen,
            bg_color=self.card_color,
            fg_color=self.fg_color,
            font=("Helvetica", 12),
        )
        settings_container.configure(width=40, height=35)
        settings_container.pack(side="right")

        # 1. Earned Screen Time & App Blocker Status
        time_card = tk.Frame(frame, bg=self.card_color, padx=12, pady=10)
        time_card.pack(fill="x", pady=(5, 8))

        tk.Label(
            time_card,
            text="⏳ Earned Screen Time",
            font=("Helvetica", 11, "bold"),
            bg=self.card_color,
            fg=self.accent_color,
        ).pack(anchor="w")

        self.screen_time_label = tk.Label(
            time_card,
            text=f"{self.screen_time_earned_min:.1f} Mins Available",
            font=("Helvetica", 14, "bold"),
            bg=self.card_color,
            fg=self.fg_color,
        )
        self.screen_time_label.pack(anchor="w", pady=(2, 0))

        tk.Label(
            time_card,
            text="• 1 Push-up/Squat = 1 Min  • 1 Sec Plank = 1 Sec",
            font=("Helvetica", 8),
            bg=self.card_color,
            fg=self.text_dim,
        ).pack(anchor="w")

        # Simulated App Launcher Test
        test_frame = tk.Frame(time_card, bg=self.card_color)
        test_frame.pack(fill="x", pady=(6, 0))

        tk.Label(
            test_frame,
            text="Test App Launch:",
            font=("Helvetica", 8, "bold"),
            bg=self.card_color,
            fg=self.fg_color,
        ).pack(side="left")

        for app_name in ["Instagram", "YouTube"]:
            c, _ = self.create_bloop_button(
                test_frame,
                text=app_name,
                command=lambda a=app_name: self.try_open_app(a),
                bg_color=self.bg_color,
                fg_color=self.fg_color,
                font=("Helvetica", 7, "bold"),
            )
            c.configure(height=24, width=70)
            c.pack(side="left", padx=4)

        # 2. Daily Tasks Checklist
        tk.Label(
            frame,
            text="📋 Daily Tasks",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(5, 2))

        tasks_card = tk.Frame(frame, bg=self.card_color, padx=10, pady=6)
        tasks_card.pack(fill="x")

        for i, task in enumerate(self.daily_tasks):
            var = tk.BooleanVar(value=task["completed"])
            cb = tk.Checkbutton(
                tasks_card,
                text=task["title"],
                variable=var,
                font=("Helvetica", 9),
                bg=self.card_color,
                fg=self.fg_color,
                selectcolor=self.bg_color,
                activebackground=self.card_color,
                command=lambda idx=i, v=var: self.toggle_task(idx, v),
            )
            cb.pack(anchor="w", pady=1)

        # 3. AI Pose Scanner
        tk.Label(
            frame,
            text="🎯 AI Pose & Exercise Scanner",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(8, 2))

        scan_btn_frame = tk.Frame(frame, bg=self.bg_color)
        scan_btn_frame.pack(fill="x")

        for scan_type in self.scans:
            c, _ = self.create_bloop_button(
                scan_btn_frame,
                text=scan_type,
                command=lambda s=scan_type: self.run_scan(s),
                bg_color=self.card_color,
                fg_color=self.fg_color,
                font=("Helvetica", 8, "bold"),
            )
            c.configure(height=32)
            c.pack(side="left", expand=True, fill="x", padx=2)

        self.scan_output = tk.Label(
            frame,
            text="Perform an exercise scan to calculate score & earned time.",
            font=("Helvetica", 9, "italic"),
            bg=self.bg_color,
            fg=self.text_dim,
        )
        self.scan_output.pack(pady=4)

        # 4. Smart Form Advice (Triggers ONLY post-scan)
        tk.Label(
            frame,
            text="💡 Smart Form Advice",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(6, 2))

        self.advice_card = tk.Frame(frame, bg=self.card_color, padx=10, pady=8)
        self.advice_card.pack(fill="x")

        self.advice_label = tk.Label(
            self.advice_card,
            text="Waiting for your first exercise scan...",
            font=("Helvetica", 9),
            bg=self.card_color,
            fg=self.text_dim,
            wraplength=330,
            justify="left",
        )
        self.advice_label.pack(anchor="w")

        # 5. Graph Card
        tk.Label(
            frame,
            text="📊 Weekly Posture Progress",
            font=("Helvetica", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(8, 2))

        graph_card = tk.Frame(frame, bg=self.card_color, padx=10, pady=6)
        graph_card.pack(fill="x", pady=(0, 5))

        self.draw_progress_graph(graph_card)

    def try_open_app(self, app_name):
        """Simulates opening a locked app."""
        is_locked = self.distracting_apps.get(app_name, tk.BooleanVar()).get()

        if is_locked and self.screen_time_earned_min <= 0:
            messagebox.showwarning(
                "App Locked by Re:Day 🔒",
                f"{app_name} is currently locked!\n\nYou have 0 earned screen time. Complete a workout or posture check in Re:Day to unlock access.",
            )
            # Instantly redirect back to Re:Day Dashboard
            self.show_home_screen()
        elif is_locked and self.screen_time_earned_min > 0:
            self.screen_time_earned_min -= 1.0
            if self.screen_time_earned_min < 0:
                self.screen_time_earned_min = 0.0

            messagebox.showinfo(
                f"Opening {app_name}",
                f"Used 1 minute of screen time to open {app_name}.\nRemaining: {self.screen_time_earned_min:.1f} Mins.",
            )
            self.show_home_screen()
        else:
            messagebox.showinfo("Opening App", f"{app_name} is unlocked!")

    def draw_progress_graph(self, parent):
        canvas = tk.Canvas(parent, height=100, bg=self.card_color, highlightthickness=0)
        canvas.pack(fill="x", expand=True)

        bar_width = 22
        gap = 18
        start_x = 25
        max_score = 100

        for i, (day, score) in enumerate(zip(self.days, self.weekly_scores)):
            x0 = start_x + i * (bar_width + gap)
            y0 = 78
            bar_height = (score / max_score) * 58
            y1 = y0 - bar_height
            x1 = x0 + bar_width

            canvas.create_rectangle(x0, y1, x1, y0, fill=self.accent_color, outline="")

            canvas.create_text(
                x0 + bar_width / 2,
                y1 - 7,
                text=str(score),
                fill=self.fg_color,
                font=("Helvetica", 7),
            )

            canvas.create_text(
                x0 + bar_width / 2,
                y0 + 10,
                text=day,
                fill=self.text_dim,
                font=("Helvetica", 8, "bold"),
            )

    def toggle_task(self, index, var):
        self.daily_tasks[index]["completed"] = var.get()

    def run_scan(self, scan_type):
        score = random.randint(82, 98)

        if scan_type == "Push-up Form":
            reps = random.randint(10, 25)
            self.screen_time_earned_min += reps * 1.0
            self.scan_output.configure(
                text=f"Completed {reps} Push-ups! Score: {score}/100 (+{reps} Mins Screen Time)",
                fg=self.accent_color,
            )
            advice_list = [
                "⚡ Smart Advice: Keep elbows tucked at a 45° angle. Excellent depth!",
                "⚡ Smart Advice: Tighten your core to prevent hip sagging on reps 10+.",
            ]

        elif scan_type == "Squat Depth":
            reps = random.randint(12, 30)
            self.screen_time_earned_min += reps * 1.0
            self.scan_output.configure(
                text=f"Completed {reps} Squats! Score: {score}/100 (+{reps} Mins Screen Time)",
                fg=self.accent_color,
            )
            advice_list = [
                "⚡ Smart Advice: Knees tracked properly over toes. Great depth!",
                "⚡ Smart Advice: Push chest up slightly at the bottom of squat.",
            ]

        elif scan_type == "Plank Hold":
            seconds = random.randint(30, 90)
            self.screen_time_earned_min += seconds / 60.0
            self.scan_output.configure(
                text=f"Held Plank for {seconds}s! Score: {score}/100 (+{seconds}s Screen Time)",
                fg=self.accent_color,
            )
            advice_list = [
                "⚡ Smart Advice: Back flat and shoulders aligned perfectly over elbows.",
                "⚡ Smart Advice: Squeeze glutes to keep pelvis in a neutral angle.",
            ]

        else:  # Posture Check
            self.scan_output.configure(
                text=f"Posture Alignment Score: {score}/100 ✅",
                fg=self.accent_color,
            )
            advice_list = [
                "⚡ Smart Advice: Pull your shoulders back 1 inch and tuck chin in.",
                "⚡ Smart Advice: Head position is neutral. Keep earlobes aligned with shoulders!",
            ]

        self.screen_time_label.configure(
            text=f"{self.screen_time_earned_min:.1f} Mins Available"
        )
        self.advice_label.configure(
            text=random.choice(advice_list), fg=self.fg_color
        )

    # ----------------------------------------------------
    # SCREEN 3: SETTINGS & APP BLOCKER MANAGER
    # ----------------------------------------------------
    def show_settings_screen(self):
        self.clear_container()

        frame = tk.Frame(self.container, bg=self.bg_color, padx=20, pady=15)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="⚙️ App Settings",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
        ).pack(anchor="w", pady=(10, 10))

        # Profile Card
        prof_card = tk.Frame(frame, bg=self.card_color, padx=12, pady=10)
        prof_card.pack(fill="x", pady=5)

        tk.Label(
            prof_card,
            text="👤 User Profile",
            font=("Helvetica", 11, "bold"),
            bg=self.card_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(0, 4))

        p_text = f"Age: {self.user_data['age']} yrs | Weight: {self.user_data['weight']} {self.user_data['weight_unit']} | Height: {self.user_data['height']} {self.user_data['height_unit']}"
        tk.Label(
            prof_card,
            text=p_text,
            font=("Helvetica", 9),
            bg=self.card_color,
            fg=self.fg_color,
            justify="left",
        ).pack(anchor="w")

        # Distracting Apps Blocker Selection
        block_card = tk.Frame(frame, bg=self.card_color, padx=12, pady=10)
        block_card.pack(fill="x", pady=10)

        tk.Label(
            block_card,
            text="🔒 Lock Distracting Apps",
            font=("Helvetica", 11, "bold"),
            bg=self.card_color,
            fg=self.accent_color,
        ).pack(anchor="w", pady=(0, 2))

        tk.Label(
            block_card,
            text="Opening checked apps will redirect you back to Re:Day unless you earn screen time.",
            font=("Helvetica", 8),
            bg=self.card_color,
            fg=self.text_dim,
            wraplength=310,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))

        for app_name, var in self.distracting_apps.items():
            cb = tk.Checkbutton(
                block_card,
                text=f"Lock {app_name}",
                variable=var,
                font=("Helvetica", 10),
                bg=self.card_color,
                fg=self.fg_color,
                selectcolor=self.bg_color,
                activebackground=self.card_color,
            )
            cb.pack(anchor="w", pady=2)

        # Notification Setting Toggle
        notif_card = tk.Frame(frame, bg=self.card_color, padx=12, pady=10)
        notif_card.pack(fill="x", pady=5)

        self.notif_var = tk.BooleanVar(value=self.user_data["notifications"])
        cb = tk.Checkbutton(
            notif_card,
            text="🔔 Allow App Notifications",
            variable=self.notif_var,
            font=("Helvetica", 10),
            bg=self.card_color,
            fg=self.fg_color,
            selectcolor=self.bg_color,
            activebackground=self.card_color,
            command=self.toggle_notifications,
        )
        cb.pack(anchor="w")

        # Back to Dashboard Bloop Button
        back_container, _ = self.create_bloop_button(
            frame,
            text="← Back to Dashboard",
            command=self.show_home_screen,
            bg_color=self.card_color,
            fg_color=self.fg_color,
            font=("Helvetica", 11, "bold"),
        )
        back_container.configure(height=40)
        back_container.pack(fill="x", pady=20)

    def toggle_notifications(self):
        self.user_data["notifications"] = self.notif_var.get()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()


# Run Application
if __name__ == "__main__":
    app = ReDayMobileApp()
    app.mainloop()
