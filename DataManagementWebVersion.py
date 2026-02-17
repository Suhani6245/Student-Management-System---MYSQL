import streamlit as st     #python library for web app design
import mysql.connector as mys          #library to create python-MYSQL interface 
import pandas as pd    #for visual data view like table  

#table name - students
#database - project

# Database Connection
mycon = mys.connect(
    host='localhost',
    user='root',
    passwd='<your_password_here>',
    database='project'
)

cursor = mycon.cursor()


#Web App design 
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
    cls = st.number_input("Enter class", min_value=1, max_value=12,step=1)
    rollno = st.number_input("Enter roll number", min_value=1, step=1)
    marks = st.number_input("Enter marks", min_value=1,max_value=100, step=1)

    if st.button("Add Student"):

        # Check if entered roll number already exists in same class
        cursor.execute("SELECT * FROM students WHERE Class=%s AND RollNo=%s",(cls, rollno))
        conflict = cursor.fetchone()

        if conflict:
            st.error("Roll number already exists in this class!")
        else:
            cursor.execute("INSERT INTO students (name, class, rollno, marks) VALUES (%s,%s,%s,%s)",(name, cls, rollno, marks))
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
        new_value = st.number_input("Enter new class", min_value=1, max_value=12, step=1)

    elif field == "Roll Number":
        new_value = st.number_input("Enter new roll number", min_value=1, step=1)

    elif field == "Marks":
        new_value = st.number_input("Enter new marks", min_value=1, max_value=100,step=1)

    if st.button("Update"):

        #Checking if student exists
        cursor.execute("SELECT * FROM students WHERE Admn_No=%s", (admNo,))
        student = cursor.fetchone()

        if not student:
            st.error("Student not found!")
        
        else:

            if field == "Name":
                cursor.execute("UPDATE students SET Name=%s WHERE Admn_No=%s",(new_value, admNo))
                mycon.commit()
                st.success("Name updated successfully!")

            elif field == "Class":

                cursor.execute("SELECT RollNo FROM students WHERE Admn_No=%s",(admNo,))
                roll_data = cursor.fetchone()

                if roll_data:
                    current_roll = roll_data[0]

                    cursor.execute("SELECT * FROM students WHERE Class=%s AND RollNo=%s AND Admn_No!=%s",(new_value, current_roll, admNo))
                    conflict = cursor.fetchone()

                    if conflict:
                        st.error("Roll number already exists in that class!")
                    else:
                        cursor.execute("UPDATE students SET Class=%s WHERE Admn_No=%s",(new_value, admNo))
                        mycon.commit()
                        st.success("Class updated successfully!")


            elif field == "Roll Number":

                # Get current class
                cursor.execute(
                    "SELECT Class FROM students WHERE Admn_No=%s",
                    (admNo,)
                )
                class_data = cursor.fetchone()
                if class_data:
                    current_class = class_data[0]

                    cursor.execute("SELECT * FROM students WHERE Class=%s AND RollNo=%s AND Admn_No!=%s",(current_class, new_value, admNo))
                    conflict = cursor.fetchone()

                    if conflict:
                        st.error("Roll number already exists in this class!")
                    else:
                        cursor.execute("UPDATE students SET RollNo=%s WHERE Admn_No=%s",(new_value, admNo))
                        mycon.commit()
                        st.success("Roll number updated successfully!")


# ---------------- DELETE DATA ----------------
elif menu == "Delete Data":
    st.subheader("Delete Student Data")

    admNo = st.number_input("Enter admission number of student", min_value=1, step=1)

    if st.button("Delete"):
        #checking if the Admission number exists
        cursor.execute("SELECT * FROM students WHERE Admn_No=%s", (admNo,))
        conflict = cursor.fetchone()
        if conflict:
            cursor.execute("DELETE FROM students WHERE Admn_No=%s", (admNo,))
            mycon.commit()
            st.warning("Student deleted successfully!")
        else:
            st.error("Admission number does not exist!")

# ---------------- DISPLAY DATA ----------------
elif menu == "Display Data":
    st.subheader("Display Student Data")

    option = st.radio("Choose option", ["Class-wise", "Specific (By Admission No)", "All Existing Students"])

    # ---------------- CLASS WISE ----------------
    if option == "Class-wise":

        # Get available classes as options from database
        cursor.execute("SELECT DISTINCT class FROM students ORDER BY class")
        classes = cursor.fetchall()

        class_list = [c[0] for c in classes]

        selected_class = st.selectbox("Select Class", class_list)

        if selected_class:
            cursor.execute("SELECT * FROM students WHERE class=%s",(selected_class,))
            data = cursor.fetchall()

            columns = [col[0] for col in cursor.description]

            df = pd.DataFrame(data, columns=columns)
            df.index = df.index + 1

            st.dataframe(df, use_container_width=True)

    # ---------------- SPECIFIC BY ADMNO ----------------
    elif option == "Specific (By Admission No)":
        admNo = st.number_input("Enter Admission Number", min_value=1, step=1)

        if st.button("Search"):
            cursor.execute("SELECT * FROM students WHERE Admn_No=%s",(admNo,))
            data = cursor.fetchone()

            if data:
                columns = [col[0] for col in cursor.description]
                df = pd.DataFrame([data], columns=columns)
                df.index = df.index + 1
                st.dataframe(df)
            else:
                st.error("No student found!")

    else:
        cursor.execute("SELECT * FROM students") 
        data = cursor.fetchall() 
        columns = [col[0] for col in cursor.description] 
        df = pd.DataFrame(data, columns=columns) 
        df.index = df.index + 1 
        st.dataframe(df)

