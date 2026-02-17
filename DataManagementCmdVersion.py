#database=project
#table- students_data
import mysql.connector as mys
mycon= mys.connect(host='localhost',user='root',passwd='your_password_here',database= 'project')
cursor=mycon.cursor()

if mycon.is_connected():
    print('~~~~~~~~~~~~~~~CONNECTION ESTABLISHED~~~~~~~~~~~~~~~~~~')
else:
    print('TRY AGAIN :(')

def add():
    n=int(input('enter how many students data to add:: '))
    for a in range(n):
        nm=input('enter name of student- ')
        cls=int(input('enter class of student- '))
        rollno=int(input('enter roll no of student- '))
        cursor.execute('insert into students_data values(%s,%s,%s);',(nm,cls,rollno))
        mycon.commit()
    print('data entry done')
def update():
    m=int(input('enter how many data to update- '))
    for i in range(m):
        rollno=int(input('enter the roll number of student whose data is to be updated- '))
        cursor.execute('select * from students_data where ROLL_NO=%s;',(rollno,))
        data=cursor.fetchall()
        for i in data:
            if i[2]== rollno:
                ch=int(input('''enter what to change:
1)name
2)class
3)roll number
enter 1/2/3: '''))
                if ch==1:
                    nm=input('enter new name- ')
                    cursor.execute('update students_data set NAME=%s where ROLL_NO=%s;',(nm,rollno))
                    mycon.commit()
                    print('name updated')
                elif ch==2:
                    cls= int(input('enter class of student - '))
                    cursor.execute('update students_data set CLASS=%s where ROLL_NO=%s;',(cls,rollno))
                    mycon.commit()
                    print('class updated')
                elif ch==3:
                    rn=int(input('enter new roll number of student - '))
                    cursor.execute('update students_data set ROLL_NUMBER=%s where ROLL_NO=%s;',(rn,rollno))
                    mycon.commit()
                    print('roll number updated')
            else:
                print('--enter correct input--')
                    
def delete():
    n=int(input('enter roll number of student whose data is to be deleted- '))
    cursor.execute('delete from students_data where ROLL_NO=%s;'%(n,))
    mycon.commit()
    print('data deleted')
def display():
    n=input('''do you want to display all data or specific data?
enter 'a for all and s for specific display of data- ''')
    if n=='a' or 'A':
        cursor.execute('select * from students_data')
        d=cursor.fetchall()
        for i in d:
            print(i)
    if n=='s' or 'S':
        p=int(input('enter roll number of student to display his/her data- '))
        cursor.execute('select * from students_data where ROLL_NO=%s;'%(p,))
        dt=cursor.fetchone()
        for i in dt:
            print(i)
#main menu
print('----------------------MAIN MENU------------------------')
print('''1)ADD DATA
2)UPDATE DATA
3)DELETE DATA
4)DISPLAY DATA''')
q= int(input('''enter your choice:
                    1/2/3/4:'''))
if q==1:
    add()
elif q==2:
    update()
elif q==3:
    delete()
elif q==4:
    display()
else:
    print('-Enter correct input-')
print('WORK DONE!')
