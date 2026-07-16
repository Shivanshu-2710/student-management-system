import json
from abc import ABC,abstractmethod
from pathlib import Path

database="school_data.json"
data = {"students":[],"teachers":[]}

if Path(database).exists():
    with open(database,'r') as f:
        content =f.read()
        if content:
            data =json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)  

class Person(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False

class student(Person):
    def get_roles(self):
        return "student"
    def show_details(self):
        roll_no=int(input("Enter Your Roll NO : "))
        for i in data["students"]:
            if i["roll_no"]==roll_no:
                grades=i["grades"]
                avg=sum(grades.values())/len(grades) if grades else 0
                print(f"Name : {i["name"]}")
                print(f"Roll NO : {i["roll_no"]}")
                print(f"Grades : {i["grades"]}")
                print(f"Average : {avg}")

    def register(self):
        name=input('Enter Name : ')
        age=int(input('Enter your age : '))
        email=input('Tell your mail : ')
        roll_no=int(input("Enter your roll number : "))

        if not Person.validate_email(email):
            print("invalid email")
            return
        
        for i in data['students']:
            if i['roll_no']==roll_no:
                print('student already exists')
                return
        
        data['students'].append({
            "name":name,
            "age":age,
            "email":email,
            "roll_no":roll_no,
            "grades":{}
        })
        save()
        print(f"Student {name} registered")

    def add_grades(self):
        roll_no=int(input("Enter Your Roll NO : "))
        subject=input("Enter Subject : ")
        marks=float(input("Enter Marks : "))

        for i in data['students']:
                if i["roll_no"]==roll_no:
                    i["grades"][subject]=marks
                    save()
                    print("grade added succesfully")
                    return
        print('Student Not Found')



class teacher(Person):
    def get_roles(self):
        return "teacher"
    def show_details(self):
        emp_id=int(input("Enter Your Employee Id : "))
        for i in data["teachers"]:
            if i["emp_id"]==emp_id:
                print(f"Name : {i["name"]}")
                print(f"Employee ID : {i["emp_id"]}")
                print(f"Subject : {i["subject"]}")
                print(f"Age : {i["age"]}")
    def register(self):
        name=input('Enter Name : ')
        age=int(input('Enter your age : '))
        email=input('Tell your mail : ')
        subject=input("Enter Subject : ")
        emp_id=int(input("Enter your employee id : "))

        if not Person.validate_email(email):
            print("invalid email")
            return
        
        for i in data['teachers']:
            if i['emp_id']==emp_id:
                print('teacher already exists')
                return
        
        data['teachers'].append({
            "name":name,
            "age":age,
            "email":email,
            "emp_id":emp_id,
            "subject":subject
        })
        save()
        print(f"Teacher {name} registered")

stud=student()
teach=teacher()
print('press 1 to register student : ')
print('press 2 to register teacher : ')
print('press 3 to add grades : ')
print('press 4 to show a student detail : ')
print('press 5 to show a teacher detail : ')
choice=int(input('please tell your choice : '))
if choice ==1:
    stud.register()
elif choice ==2:
    teach.register()
elif choice ==3:
    stud.add_grades()
elif choice ==4:
    stud.show_details()
elif choice==5:
    teach.show_details()