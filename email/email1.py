import tkinter as tk
import webbrowser
import urllib.parse
import openpyxl
import google.generativeai as genai
import os

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statewise Expenditure Email Sender")
        self.button = tk.Button(root, text="Send Next Email", command=self.send_next_email)
        self.button.pack()

        # Path to your Excel file
        self.excel_file_path = r'/Users/sakethreddy/harshi/github/Team-54/email/StateWiseReport.xlsx'  # Update with your file path

        # Load data from Excel file
        self.wb = openpyxl.load_workbook(self.excel_file_path)
        self.sheet = self.wb.active

        # Initialize row index (start after the header row)
        self.current_row = 2

    def send_next_email(self):
        if self.current_row <= self.sheet.max_row:
            row = [cell.value for cell in self.sheet[self.current_row]]

            state = row[1]
            email = row[-1]  # Assuming email is in the last column
            fy_spent = row[1:-1]  # Financial year expenditure values

            # Find the highest expenditure
            max_expenditure = max(fy_spent)
            max_index = fy_spent.index(max_expenditure)
            max_fy = f"FY {2014 + max_index}-{2015 + max_index}"  # Example: FY 2014-15, FY 2015-16, etc.

            # Construct email subject and body
            GOOGLE_API_KEY = os.environ.("API_KEY")
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"Generate Mail content to {state} with expenditure {max_expenditure} spent indexing {max_index} for the year {max_fy}  it should be requesting donations for Jaldhaara Foundation,convincing for working towards drinking water improvement")
            generated = res.text.replace('.',' *')
            subject = f"Statewise Expenditure Update: {state}"
            body = generated
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)

            # Construct mailto link for Gmail
            mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject_encoded}&body={body_encoded}"

            # Open Gmail compose window with pre-filled data
            webbrowser.open(mailto_link)

            # Move to the next row for the next button press
            self.current_row += 1
        else:
            print("All emails have been sent.")

root = tk.Tk()
app = EmailSenderApp(root)
root.mainloop()
