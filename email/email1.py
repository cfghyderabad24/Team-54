import tkinter as tk
import webbrowser
import urllib.parse
import openpyxl

class EmailSenderApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Statewise Expenditure Email Sender")
        self.button = tk.Button(root, text="Send Next Email", command=self.send_next_email)
        self.button.pack()

        # Path to your Excel file
        self.excel_file_path = r'C:\Users\Yukta Punj\Desktop\code_for_good_2024\email\DynamicCSRReport.xlsx'  # Update with your file path

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
            subject = f"Statewise Expenditure Update: {state}"
            body = f"Dear Sir/Madam,\n\n" \
                   f"The highest expenditure for {state} occurred in {max_fy}, amounting to {max_expenditure} INR Cr.\n\n" \
                   f"Given this significant expenditure, we are seeking additional funding to support our ongoing projects and initiatives in the state.\n\n" \
                   \
                   f"---\n\n" \
                   f"Subject: Request for CSR Partnership and Support for Jeldara Foundation\n\n" \
                   \
                   f"I hope this email finds you well.\n\n" \
                   f"I am writing to you on behalf of Jeldara Foundation, a non-governmental organization dedicated to providing education and healthcare support to underprivileged children in rural India.\n\n" \
                   f"We are reaching out to explore the possibility of a partnership through your esteemed CSR initiative. As a leading financial institution, JPMorgan has consistently demonstrated its commitment to social responsibility and community development. We believe that our goals and objectives align closely with your CSR mission, and together, we can make a substantial impact on the lives of those in need.\n\n" \
                   f"At Jeldara Foundation, we have successfully implemented several projects aimed at improving literacy rates, providing clean drinking water, and healthcare services in underserved communities. However, to continue and expand our efforts, we require additional funding and resources.\n\n" \
                   f"We kindly request your support in the form of donations to help us achieve the following objectives:\n\n" \
                   f"1. Expand Educational Programs: Enhance our educational initiatives by building more schools, providing scholarships, and training teachers.\n" \
                   f"2. Improve Healthcare Services: Establish more health camps, provide essential medical supplies, and support healthcare infrastructure in remote areas.\n" \
                   f"3. Sustainable Development Projects: Implement sustainable solutions for clean water, sanitation, and renewable energy in the communities we serve.\n\n" \
                   f"Your contribution will not only help us achieve these goals but will also create a lasting impact on the lives of thousands of individuals. We are confident that with JPMorgan Asset Management India's support, we can significantly improve the quality of life for the people we serve.\n\n" \
                   f"Please find attached a detailed proposal outlining our current projects and the specific areas where your support can make a difference. We would be honored to discuss this further and explore how we can work together to bring about positive change.\n\n" \
                   f"Thank you for considering our request. We look forward to the possibility of partnering with JPMorgan Asset Management India to make a meaningful difference.\n\n" \
                   f"Best regards,\n\n" \
                   f"JALDHAARA ORGANIZATION,\n"

            # Encode subject and body for URL
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
app = EmailSenderApp()
root.mainloop()