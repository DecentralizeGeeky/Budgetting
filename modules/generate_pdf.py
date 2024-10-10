import sqlite3
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas

def generate_pdf(self):
    records = self.db.fetch_all_records()
    
    if records:
        # Ask where to save the PDF file
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        
        if file_path:
            pdf = canvas.Canvas(file_path)
            pdf.setTitle("Event Budget Records")
            
            # Define a function to draw a table for each event's records
            def draw_table(pdf, event, items, y):
                # Calculate the total cost for this event
                total_cost = sum(item[5] for item in items)
                
                # Event title with the total sum for the event
                pdf.drawString(100, y, f"Event: {event} (Total: ₦{total_cost:.2f})")
                y -= 20
                
                # Table headers
                pdf.drawString(100, y, "Item Name")
                pdf.drawString(200, y, "Unit Price")
                pdf.drawString(300, y, "Quantity")
                pdf.drawString(400, y, "Total Price")
                pdf.drawString(500, y, "Date")
                y -= 20
                
                # Draw a line to separate the headers from the rows
                pdf.line(100, y, 550, y)
                y -= 10
                
                # Table rows with records for this event
                for item in items:
                    pdf.drawString(100, y, item[2])  # Item name
                    pdf.drawString(200, y, f"₦{item[3]:.2f}")  # Unit price
                    pdf.drawString(300, y, str(item[4]))  # Quantity
                    pdf.drawString(400, y, f"₦{item[5]:.2f}")  # Total price
                    pdf.drawString(500, y, item[6])  # Date
                    y -= 20
                    if y < 50:  # Start a new page if the current page is full
                        pdf.showPage()
                        y = 750
                pdf.line(100, y + 10, 550, y + 10)  # Line after the event's records
                
                return y
            
            # Group records by event
            event_dict = {}
            for record in records:
                event_name = record[1]
                if event_name not in event_dict:
                    event_dict[event_name] = []
                event_dict[event_name].append(record)
            
            y = 780
            pdf.drawString(100, y, "Event Budget Report")
            pdf.drawString(100, y - 20, "====================")
            y -= 40
            
            # Loop through each event and create a table
            for event, items in event_dict.items():
                y = draw_table(pdf, event, items, y)
                y -= 30  # Add some space before the next event
                
            pdf.save()
            messagebox.showinfo("Success", "PDF generated successfully!")
    else:
        messagebox.showinfo("Info", "No records available to generate a PDF.")
