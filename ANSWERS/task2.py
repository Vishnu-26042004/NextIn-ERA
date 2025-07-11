import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
import requests
from bs4 import BeautifulSoup
import PyPDF2
import docx

def extract_emails(text):
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

def extract_from_url():
    url = url_entry.get()
    if not url.startswith("http"):
        messagebox.showerror("Error", "Please enter a valid URL (starting with http/https).")
        return

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        emails = extract_emails(text)
        show_emails(set(emails))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch URL: {e}")

def extract_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("Word Documents", "*.docx")])
    if not file_path:
        return

    try:
        if file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        elif file_path.endswith(".pdf"):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                content = ''
                for page in reader.pages:
                    content += page.extract_text()

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            content = '\n'.join([para.text for para in doc.paragraphs])

        else:
            messagebox.showerror("Unsupported File", "Only .txt, .pdf, and .docx are supported.")
            return

        emails = extract_emails(content)
        show_emails(set(emails))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")

def show_emails(emails):
    output_text.delete("1.0", tk.END)
    if not emails:
        output_text.insert(tk.END, "No emails found.")
    else:
        for email in sorted(emails):
            output_text.insert(tk.END, email + "\n")

def save_output():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("Empty", "No content to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
    if save_path:
        with open(save_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Emails saved to {save_path}")

# GUI Setup
root = tk.Tk()
root.title("Email Extractor Tool")
root.geometry("750x550")

tk.Label(root, text="Enter URL:").pack(pady=5)
url_entry = tk.Entry(root, width=80)
url_entry.pack(pady=5)

tk.Button(root, text="Extract from URL", command=extract_from_url, width=25).pack(pady=5)
tk.Button(root, text="Upload File", command=extract_from_file, width=25).pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=20, font=("Arial", 10))
output_text.pack(pady=10)

tk.Button(root, text="Save Emails to File", command=save_output, width=25).pack(pady=5)

root.mainloop()
