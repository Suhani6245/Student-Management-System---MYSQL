import streamlit as st
import mysql.connector as mys
import pandas as pd

#table name - students
#database - project

# Database Connection
mycon = mys.connect(
    host='localhost',
    user='root',
    passwd='5871@lpu',
    database='project'
)

cursor = mycon.cursor()

st.title("🎓Student Management System")

# Sidebar
menu = st.sidebar.radio(
    "Select Operation",
    ["Add Data", "Update Data", "Delete Data", "Display Data"]
)



# ---------------- ADD DATA ----------------
if menu == "Add Data":
    st.subheader("Add Student Data")

    name = st.text_input("Enter student name")
    cls = st.number_input("Enter class", min_value=1, step=1)
    rollno = st.number_input("Enter roll number", min_value=1, step=1)
    marks = st.number_input("Enter marks", min_value=1, step=1)

    if st.button("Add Student"):
        cursor.execute(
            "INSERT INTO students (name, class, rollno, marks) VALUES (%s,%s,%s,%s)",
            (name, cls, rollno, marks)
        )
        mycon.commit()
        st.success("Student added successfully!")

# ---------------- UPDATE DATA ----------------
elif menu == "Update Data":
    st.subheader("Update Student Data")

    admNo = st.number_input("Enter admission number of student", min_value=1, step=1)

    field = st.selectbox("Select field to update", ["Name", "Class", "Roll Number","Marks"])

    if field == "Name":
        new_value = st.text_input("Enter new name")

    elif field == "Class":
        new_value = st.number_input("Enter new class", min_value=1, step=1)

    elif field == "Roll Number":
        new_value = st.number_input("Enter new roll number", min_value=1, step=1)

    elif field == "Marks":
        new_value = st.number_input("Enter new marks", min_value=1, step=1)

    if st.button("Update"):
        if field == "Name":
            cursor.execute("UPDATE students SET Name=%s WHERE Admn_No=%s",
                           (new_value, admNo))
        elif field == "Class":
            cursor.execute("UPDATE students SET Class=%s WHERE Admn_No=%s",
                           (new_value, admNo))
        elif field == "Roll Number":
            cursor.execute("UPDATE students SET RollNo=%s WHERE Admn_No=%s",
                           (new_value, admNo))
        
        elif field == "Marks":
            cursor.execute("UPDATE students SET Marks=%s WHERE Admn_No=%s",
                           (new_value, admNo))

        mycon.commit()
        st.success("Data updated successfully!")

# ---------------- DELETE DATA ----------------
elif menu == "Delete Data":
    st.subheader("Delete Student Data")

    admNo = st.number_input("Enter admission number of student", min_value=1, step=1)

    if st.button("Delete"):
        cursor.execute("DELETE FROM students WHERE Admn_No=%s", (admNo,))
        mycon.commit()
        st.warning("Student deleted successfully!")

# ---------------- DISPLAY DATA ----------------
elif menu == "Display Data":
    st.subheader("Display Student Data")

    option = st.radio("Choose option", ["All", "Specific"])

    if option == "All":
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

        columns = [col[0] for col in cursor.description]

        df = pd.DataFrame(data, columns=columns)
        df.index = df.index + 1
        st.dataframe(df)

    else:
        admNo = st.number_input("Enter admission number to update", min_value=1, step=1)
        if st.button("Search"):
            cursor.execute("SELECT * FROM students WHERE Admn_No=%s", (admNo,))
            data = cursor.fetchone()
            if data:
                st.write(data)
            else:
                st.error("No student found!")
