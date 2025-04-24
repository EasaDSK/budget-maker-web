import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Page config
st.set_page_config(page_title="Budget Maker", layout="centered", initial_sidebar_state="expanded")

# Dark theme styling
st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        color: white;
    }
    .stApp {
        background-color: #1e1e1e;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("💰 Budget Maker Web App")

# Budget Entry Section
st.header("➕ Add Expense / Income")
category = st.text_input("Category")
amount = st.number_input("Amount", step=0.01, format="%.2f")
type_ = st.selectbox("Type", ["Expense", "Income"])
date = st.date_input("Date")

if "data" not in st.session_state:
    st.session_state.data = []

if st.button("Add"):
    if category and amount:
        st.session_state.data.append({"Category": category, "Amount": amount, "Type": type_, "Date": date})
        st.success("Added successfully!")

# View Data
st.header("📊 Budget Overview")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    # Show table
    st.dataframe(df)

    # Chart
    st.subheader("📈 Chart Summary")
    fig, ax = plt.subplots()
    df.groupby("Type")["Amount"].sum().plot(kind="bar", ax=ax, color=["red", "green"])
    ax.set_title("Total Income vs Expense")
    st.pyplot(fig)

    # Export to Excel
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Budget')
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    excel_data = to_excel(df)
    st.download_button("⬇️ Download Excel", excel_data, "budget.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Export to PDF
    def create_pdf(df):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)
        text = c.beginText(40, 750)
        text.textLine("Budget Report")
        text.textLine("")

        for i, row in df.iterrows():
            text.textLine(f"{row['Date']} - {row['Type']}: {row['Category']} - ${row['Amount']:.2f}")

        c.drawText(text)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf_data = create_pdf(df)
    st.download_button("⬇️ Download PDF", pdf_data, file_name="budget_report.pdf", mime="application/pdf")

else:
    st.info("No data available yet. Add your first record!")

# Footer
st.markdown("---")
st.markdown("🧠 Made by **You** using Streamlit ✨")
