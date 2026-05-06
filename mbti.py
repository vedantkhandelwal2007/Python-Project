import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
from pathlib import Path

# ================= QUESTIONS =================
QUESTIONS = [
    ("You feel energized after spending time with a large group of people.", "E", "I"),
    ("You usually think out loud rather than keeping thoughts to yourself.", "E", "I"),
    ("You often start conversations instead of waiting for others.", "E", "I"),
    ("You prefer quiet time alone after a busy day.", "I", "E"),
    ("You reflect deeply before speaking in important situations.", "I", "E"),
    ("You feel more comfortable with a few close friends than with many acquaintances.", "I", "E"),

    ("You trust practical experience more than abstract ideas.", "S", "N"),
    ("You focus on facts before exploring possibilities.", "S", "N"),
    ("You prefer clear details over broad concepts.", "S", "N"),
    ("You enjoy imagining future possibilities more than reviewing present facts.", "N", "S"),
    ("You often connect patterns and hidden meanings in information.", "N", "S"),
    ("You are drawn to innovation and new interpretations.", "N", "S"),

    ("When making decisions, logic matters more than emotions.", "T", "F"),
    ("You value fairness through consistency and principles.", "T", "F"),
    ("You are comfortable giving direct criticism when necessary.", "T", "F"),
    ("You usually consider personal feelings before making a decision.", "F", "T"),
    ("You naturally empathize with how others may react.", "F", "T"),
    ("Maintaining harmony is often more important than winning an argument.", "F", "T"),

    ("You like planning tasks well in advance.", "J", "P"),
    ("You feel better when decisions are settled early.", "J", "P"),
    ("You prefer structure and routines over sudden changes.", "J", "P"),
    ("You like keeping options open until the last moment.", "P", "J"),
    ("You adapt easily when plans change unexpectedly.", "P", "J"),
    ("You enjoy spontaneity more than fixed schedules.", "P", "J"),

    ("You stay calm under pressure.", "A", "T_id"),
    ("You recover quickly from setbacks.", "A", "T_id"),
    ("You feel confident in your decisions.", "A", "T_id"),
    ("You often overthink decisions.", "T_id", "A"),
    ("Stress affects you strongly.", "T_id", "A"),
    ("You worry about your choices.", "T_id", "A"),
]

# ================= DESCRIPTIONS =================
TYPE_DESCRIPTIONS = {
    "INTJ": "Strategic, independent, and future-focused.",
    "INTP": "Analytical and idea-driven.",
    "ENTJ": "Bold and goal-oriented.",
    "ENTP": "Creative and energetic.",
    "INFJ": "Insightful and purposeful.",
    "INFP": "Empathetic and thoughtful.",
    "ENFJ": "People-centered leader.",
    "ENFP": "Enthusiastic and creative.",
    "ISTJ": "Reliable and structured.",
    "ISFJ": "Supportive and careful.",
    "ESTJ": "Efficient and organized.",
    "ESFJ": "Warm and social.",
    "ISTP": "Practical and adaptable.",
    "ISFP": "Creative and flexible.",
    "ESTP": "Bold and action-oriented.",
    "ESFP": "Fun-loving and energetic.",
}

# ================= CAREERS =================
CAREERS = {
    "INTJ": ["Cybersecurity Analyst", "Software Engineer", "Data Scientist"],
    "INTP": ["AI Developer", "Programmer", "Researcher"],
    "ENTJ": ["Entrepreneur", "Manager"],
    "ENTP": ["Startup Founder", "Marketing Strategist"],
    "INFJ": ["Psychologist", "Writer"],
    "INFP": ["Designer", "Content Creator"],
    "ENFJ": ["Teacher", "HR Manager"],
    "ENFP": ["Journalist", "Creative Director"],
    "ISTJ": ["Banker", "Government Officer"],
    "ISFJ": ["Nurse", "Teacher"],
    "ESTJ": ["Administrator", "Police"],
    "ESFJ": ["Event Manager", "HR"],
    "ISTP": ["Engineer", "Game Developer"],
    "ISFP": ["Photographer", "Designer"],
    "ESTP": ["Sales", "Entrepreneur"],
    "ESFP": ["Actor", "Influencer"]
}

# ================= GLOBAL =================
scores = {k: 0 for k in ["E","I","S","N","T","F","J","P","A","T_id"]}
current_q = 0
selected = None

# ================= FUNCTIONS =================
def reset():
    global current_q
    current_q = 0
    for k in scores:
        scores[k] = 0

def get_result():
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    suffix = "-A" if scores["A"] >= scores["T_id"] else "-T"
    return mbti + suffix, mbti

def save_result(res):
    path = Path("results.csv")
    new = not path.exists()
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time","result"])
        w.writerow([datetime.now(), res])

def show_q():
    global selected
    q, _, _ = QUESTIONS[current_q]
    selected = tk.IntVar(value=999)  # FIXED

    label_q.config(text=f"Statement {current_q+1} of {len(QUESTIONS)}")
    label_stmt.config(text=q)
    progress_label.config(text=f"Progress: {current_q+1}/{len(QUESTIONS)}")
    progress_fill.config(width=int((current_q+1)/len(QUESTIONS)*500))

    for w in frame_opts.winfo_children():
        w.destroy()

    for text, val in [
        ("Strongly Agree",2),
        ("Agree",1),
        ("Neutral",0),
        ("Disagree",-1),
        ("Strongly Disagree",-2)
    ]:
        tk.Radiobutton(
            frame_opts,
            text=text,
            variable=selected,
            value=val,
            font=("Arial", 13),
            bg="#ffffff",
            anchor="w",
            padx=15,
            pady=12
        ).pack(fill="x", padx=20, pady=6)

def next_q():
    global current_q
    val = selected.get()

    if val == 999:
        messagebox.showwarning("Error", "Please select an option.")
        return

    _, pos, neg = QUESTIONS[current_q]

    if val > 0:
        scores[pos] += val
    elif val < 0:
        scores[neg] += abs(val)

    current_q += 1

    if current_q < len(QUESTIONS):
        show_q()
    else:
        show_result()

def show_result():
    res, base = get_result()
    save_result(res)

    for w in frame_opts.winfo_children():
        w.destroy()

    label_q.config(text="Your Result")
    label_stmt.config(text=res)

    tk.Label(frame_opts, text=TYPE_DESCRIPTIONS.get(base,""), font=("Arial",13), bg="#f5ecff").pack(pady=10)

    tk.Label(frame_opts, text="Recommended Careers:", font=("Arial",14,"bold"), bg="#f5ecff").pack(pady=5)

    for c in CAREERS.get(base, []):
        tk.Label(frame_opts, text="• "+c, bg="#f5ecff", font=("Arial",12)).pack()

    btn_next.config(state="disabled")
    btn_restart.pack(pady=10)

def restart():
    reset()
    btn_next.config(state="normal")
    btn_restart.pack_forget()
    show_q()

# ================= UI =================
root = tk.Tk()
root.title("Advanced MBTI Tester")
root.geometry("700x600")
root.configure(bg="#f5ecff")

header = tk.Frame(root, bg="#7b1fa2", height=80)
header.pack(fill="x")

tk.Label(header, text="Advanced MBTI-Style Tester", fg="white", bg="#7b1fa2", font=("Arial",20,"bold")).pack(pady=10)

main = tk.Frame(root, bg="#f5ecff")
main.pack(fill="both", expand=True, padx=20, pady=20)

label_q = tk.Label(main, font=("Arial",14,"bold"), bg="#f5ecff")
label_q.pack(anchor="w")

label_stmt = tk.Label(main, font=("Arial",18), wraplength=650, bg="#f5ecff")
label_stmt.pack(pady=10)

progress_label = tk.Label(main, bg="#f5ecff")
progress_label.pack(anchor="w")

progress_bar = tk.Frame(main, bg="#d1c4e9", height=15, width=500)
progress_bar.pack(anchor="w", pady=5)
progress_bar.pack_propagate(False)

progress_fill = tk.Frame(progress_bar, bg="#7b1fa2", width=0)
progress_fill.pack(fill="y", side="left")

frame_opts = tk.Frame(main, bg="#f5ecff")
frame_opts.pack(fill="both", expand=True)

btn_next = tk.Button(root, text="Next", bg="#7b1fa2", fg="white", command=next_q)
btn_next.pack(pady=25)

btn_restart = tk.Button(root, text="Restart", command=restart)

show_q()
root.mainloop()
