import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SECTION 1: Core Python Logic
st.title("🎓 Student Performance Analyzer")

st.header("📌 Simulate One Student Entry")
name = st.text_input("Enter student name:")
roll = st.text_input("Enter roll number:")
math = st.number_input("Mathematics mark", min_value=0.0, max_value=100.0, step=1.0)
science = st.number_input("Science mark", min_value=0.0, max_value=100.0, step=1.0)
english = st.number_input("English mark", min_value=0.0, max_value=100.0, step=1.0)

if st.button("Analyze This Student"):
    total = math + science + english
    percent = total / 3
    if percent >= 90:
        grade = "A"
    elif percent >= 80:
        grade = "B"
    elif percent >= 70:
        grade = "C"
    elif percent >= 60:
        grade = "D"
    else:
        grade = "F"

    st.write(f"**Name:** {name} | **Roll:** {roll}")
    st.write(f"**Total:** {total} / 300")
    st.write(f"**Percentage:** {percent:.2f}%")
    st.write(f"**Grade:** {grade}")
    
    if grade in ["A", "B"]:
        st.success("🎉 Congratulations on your excellent performance!")
    elif grade == "F":
        st.error("⚠️ Warning: You have failed. Please consult your instructor.")

# SECTION 2: Data Handling
st.header("📊 Analyze Full Dataset")
uploaded = "students_raw.csv"
df = pd.read_csv(uploaded)

# Clean data
df[['Mathematics', 'Science', 'English']] = df[['Mathematics', 'Science', 'English']].apply(pd.to_numeric, errors='coerce')
df.fillna(0, inplace=True)

# Compute new columns
df["Total"] = df[['Mathematics', 'Science', 'English']].sum(axis=1)
df["Percentage"] = df["Total"] / 3
conditions = [
    (df["Percentage"] >= 90),
    (df["Percentage"] >= 80),
    (df["Percentage"] >= 70),
    (df["Percentage"] >= 60),
    (df["Percentage"] < 60)
]
grades = ['A', 'B', 'C', 'D', 'F']
df["Grade"] = np.select(conditions, grades)

# Save cleaned CSV
# df.to_csv("students_cleaned.csv", index=False)

csv_file = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Cleaned CSV",
    data=csv_file,
    file_name="students_cleaned.csv",
    mime='text/csv'
)


# st.dataframe(df.head())
st.dataframe(df)

# NumPy Stats
st.subheader("📈 Basic Statistics")
marks_np = df[['Mathematics', 'Science', 'English']].to_numpy()
avg = np.mean(marks_np, axis=0)
std_dev = np.std(marks_np, axis=0)
min_marks = np.min(marks_np, axis=0)
max_marks = np.max(marks_np, axis=0)

stats_df = pd.DataFrame({
    "Subject": ["Mathematics", "Science", "English"],
    "Average": avg,
    "Std Dev": std_dev,
    "Min": min_marks,
    "Max": max_marks
})
st.table(stats_df)

# High Performers
threshold = st.slider("Total marks threshold (out of 300)", 0, 300, 250)
high_performers = df[df["Total"] > threshold]
st.write(f"🎯 Number of high performers (> {threshold}):", high_performers.shape[0])

# SECTION 3: Visualization
st.header("📉 Visualizations")

# Line Plot - Avg marks trend
avg_marks = df[['Mathematics', 'Science', 'English']].mean()
fig1, ax1 = plt.subplots()
avg_marks.plot(kind='line', marker='o', ax=ax1)
ax1.set_title("Average Marks in Each Subject")
ax1.set_ylabel("Marks")
ax1.set_xlabel("Subject")
plt.grid(True)
st.pyplot(fig1)

# Bar Chart - Grade distribution
grade_counts = df["Grade"].value_counts().sort_index()
fig2, ax2 = plt.subplots()
grade_counts.plot(kind='bar', color='skyblue', ax=ax2)
ax2.set_title("Number of Students per Grade")
ax2.set_ylabel("Count")
ax2.set_xlabel("Grade")
st.pyplot(fig2)

# Scatter Plot - Percentage vs Total
fig3, ax3 = plt.subplots()
colors = df["Grade"].map({"A":"green", "B":"blue", "C":"orange", "D":"purple", "F":"red"})
ax3.scatter(df["Total"], df["Percentage"], c=colors)
ax3.set_title("Percentage vs Total Marks")
ax3.set_xlabel("Total Marks")
ax3.set_ylabel("Percentage")
ax3.grid(True)
st.pyplot(fig3)

st.success("✅ Analysis complete. You can find 'students_cleaned.csv' and saved plots in your app directory.")
