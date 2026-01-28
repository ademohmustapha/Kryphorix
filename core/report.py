from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime
import os
import json

def generate_pdf(findings, logo_path="assets/kryphorix_logo.png", filename=None, targets=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/Kryphorix_Report_{timestamp}.pdf"

    os.makedirs("reports", exist_ok=True)
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    header_style = ParagraphStyle('Header', fontSize=14, spaceAfter=12, textColor=colors.HexColor("#2E86C1"))

    # -------------------------
    # Cover Page
    # -------------------------
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=150, height=150))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("Kryphorix Security Assessment Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    if targets:
        elements.append(Paragraph(f"Scan Target(s): {', '.join(targets)}", normal_style))
    elements.append(PageBreak())

    # -------------------------
    # Module & Severity Summary
    # -------------------------
    module_counts = {}
    severity_counts = {}
    for f in findings:
        module_counts[f.module] = module_counts.get(f.module, 0) + 1
        severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

    # Module summary table
    elements.append(Paragraph("Module Summary", header_style))
    data = [["Module", "Findings Count"]]
    for module, count in module_counts.items():
        data.append([module, str(count)])
    table = Table(data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2E86C1")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('BOTTOMPADDING',(0,0),(-1,0),6),
        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1,12))

    # Severity summary table
    elements.append(Paragraph("Severity Summary", header_style))
    data = [["Severity", "Count"]]
    for sev, count in severity_counts.items():
        data.append([sev, str(count)])
    table = Table(data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2E86C1")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('BOTTOMPADDING',(0,0),(-1,0),6),
        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
    ]))
    elements.append(table)
    elements.append(PageBreak())

    # -------------------------
    # Detailed Findings Table
    # -------------------------
    elements.append(Paragraph("Detailed Findings", header_style))
    data = [["Module","Title", "Severity", "Description", "Fix / Recommendation"]]
    severity_colors = {
        "Info": colors.blue,
        "Low": colors.green,
        "Medium": colors.orange,
        "High": colors.red,
        "Critical": colors.darkred
    }
    for f in findings:
        data.append([f.module, f.title, f.severity, f.desc, f.fix])

    table = Table(data, colWidths=[100,120,60,200,150], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2E86C1")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),10),
        ('BOTTOMPADDING',(0,0),(-1,0),6),
        ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
    ]))
    for i, f in enumerate(findings, start=1):
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (2,i), (2,i), severity_colors.get(f.severity, colors.black))
        ]))
    elements.append(table)

    doc.build(elements)
    print(f"[+] PDF report saved: {filename}")


# -------------------------
# JSON Export
# -------------------------
def export_json(findings):
    os.makedirs("reports", exist_ok=True)
    data = [f.to_dict() for f in findings]
    filename = f"reports/Kryphorix_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[+] JSON report saved: {filename}")

