class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    def __init__(self, student_id, first_name, last_name, faculty, grade):
        super().__init__(first_name, last_name)
        self.student_id = student_id
        self.faculty = faculty
        self.grade = grade
    
    def display_info(self):
        print("\nსტუდენტის ინფორმაცია")
        print("-" * 50)
        print(f"სახელი: {self.first_name}")
        print(f"გვარი: {self.last_name}")
        print(f"ქულა: {self.grade}")
        print(f"ფაკულტეტი: {self.faculty}")
        print(f"პირადი ID: {self.student_id}")
        print("-" * 50)


class Lecturer(Person):
    def __init__(self, first_name, last_name, course):
        super().__init__(first_name, last_name)
        self.course = course
    
    def display_info(self):
        print("\nლექტორის ინფორმაცია")
        print("-" * 50)
        print(f"სახელი: {self.first_name}")
        print(f"გვარი: {self.last_name}")
        print(f"კურსი: {self.course}")
        print("-" * 50)


class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.lecturers = []
        self.load_data()
    
    def load_data(self):
        try:
            with open('students.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 5:
                        student = Student(
                            student_id=parts[0].strip(),
                            first_name=parts[1].strip(),
                            last_name=parts[2].strip(),
                            faculty=parts[3].strip(),
                            grade=parts[4].strip()
                        )
                        self.students.append(student)
        except FileNotFoundError:
            print("students.txt ფაილი ვერ მოიძებნა. შეიქმნება პირველი სტუდენტის დამატებისას.")
        except Exception as e:
            print(f"შეცდომა students.txt-ის წაკითხვისას: {e}")
        
        try:
            with open('lecturers.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if ', ' in line:
                        name_part, course = line.rsplit(', ', 1)
                        name_parts = name_part.split()
                        
                        if len(name_parts) >= 2:
                            if name_parts[0].endswith('.'):
                                first_name = name_parts[1] if len(name_parts) > 1 else name_parts[0]
                                last_name = name_parts[2] if len(name_parts) > 2 else ""
                            else:
                                first_name = name_parts[0]
                                last_name = name_parts[1] if len(name_parts) > 1 else ""
                            
                            lecturer = Lecturer(
                                first_name=first_name,
                                last_name=last_name,
                                course=course.strip()
                            )
                            self.lecturers.append(lecturer)
        except FileNotFoundError:
            print("lecturers.txt ფაილი ვერ მოიძებნა.")
        except Exception as e:
            print(f"შეცდომა lecturers.txt-ის წაკითხვისას: {e}")
    
    def save_students(self):
        try:
            with open('students.txt', 'w', encoding='utf-8') as f:
                for student in self.students:
                    f.write(f"{student.student_id},{student.first_name},{student.last_name},{student.faculty},{student.grade}\n")
        except Exception as e:
            print(f"შეცდომა ფაილის შენახვისას: {e}")
    
    def authenticate(self, email, password):
        if not email.endswith('@nuga.edu.ge'):
            return None, None
        
        if password != '1':
            return None, None
        
        username = email.replace('@nuga.edu.ge', '').lower().strip()
        
        for lecturer in self.lecturers:
            full_name_no_space = f"{lecturer.first_name}{lecturer.last_name}".lower()
            if (username == lecturer.first_name.lower() or 
                username == lecturer.last_name.lower() or
                username == full_name_no_space):
                return 'lecturer', lecturer
        
        matching_students = []
        for student in self.students:
            full_name_no_space = f"{student.first_name}{student.last_name}".lower()
            if username == student.student_id.lower():
                return 'student', student
            elif (username == student.first_name.lower() or 
                  username == student.last_name.lower() or
                  username == full_name_no_space):
                matching_students.append(student)
        
        if len(matching_students) > 1:
            print("\nრამდენიმე სტუდენტი მოიძებნა ამ ინფორმაციით:")
            for i, student in enumerate(matching_students, 1):
                print(f"{i}. {student.get_full_name()} (ID: {student.student_id}, ფაკულტეტი: {student.faculty})")
            
            try:
                choice = int(input("\nაირჩიეთ ნომერი: ").strip())
                if 1 <= choice <= len(matching_students):
                    return 'student', matching_students[choice - 1]
            except (ValueError, IndexError):
                pass
            return None, None
        elif len(matching_students) == 1:
            return 'student', matching_students[0]
        
        return None, None
    
    def add_student(self):
        print("\nახალი სტუდენტის დამატება")
        print("-" * 50)
        
        student_id = input("პირადი ID: ").strip()
        if not student_id:
            print("ID არ შეიძლება იყოს ცარიელი!")
            return
        
        # Check for duplicate ID
        for student in self.students:
            if student.student_id == student_id:
                print("ამ ID-ით სტუდენტი უკვე არსებობს!")
                return
        
        first_name = input("სახელი: ").strip()
        last_name = input("გვარი: ").strip()
        faculty = input("ფაკულტეტი: ").strip()
        grade = input("ქულა: ").strip()
        
        if not all([first_name, last_name, faculty, grade]):
            print("ყველა ველი უნდა იყოს შევსებული!")
            return
        
        student = Student(student_id, first_name, last_name, faculty, grade)
        self.students.append(student)
        self.save_students()
        print("✓ სტუდენტი წარმატებით დაემატა!")
    
    def remove_student(self):
        print("\nსტუდენტის წაშლა")
        print("-" * 50)
        student_id = input("შეიყვანეთ სტუდენტის ID: ").strip()
        
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                confirm = input(f"დარწმუნებული ხართ, რომ გსურთ {student.get_full_name()}-ის წაშლა? (y/n): ")
                if confirm.lower() == 'y':
                    self.students.pop(i)
                    self.save_students()
                    print("✓ სტუდენტი წარმატებით წაიშალა!")
                else:
                    print("ოპერაცია გაუქმდა.")
                return
        
        print("✗ სტუდენტი ვერ მოიძებნა!")
    
    def list_students_by_faculty(self, faculty):
        print(f"\nსტუდენტები - {faculty}")
        print("-" * 60)
        print(f"{'ID':<10} {'სახელი':<15} {'გვარი':<15} {'ქულა':<10}")
        print("-" * 60)
        
        found = False
        for student in self.students:
            if student.faculty.lower() == faculty.lower():
                print(f"{student.student_id:<10} {student.first_name:<15} {student.last_name:<15} {student.grade:<10}")
                found = True
        
        if not found:
            print("სტუდენტები არ მოიძებნა ამ ფაკულტეტზე")
        print("-" * 60)
    
    def list_all_students(self):
        if not self.students:
            print("\nსტუდენტები არ არიან სისტემაში.")
            return
        
        print("\nყველა სტუდენტი")
        print("-" * 70)
        print(f"{'ID':<10} {'სახელი':<15} {'გვარი':<15} {'ფაკულტეტი':<15} {'ქულა':<10}")
        print("-" * 70)
        
        for student in self.students:
            print(f"{student.student_id:<10} {student.first_name:<15} {student.last_name:<15} {student.faculty:<15} {student.grade:<10}")
        print("-" * 70)
    
    def update_student_grade(self):
        print("\nსტუდენტის ქულის განახლება")
        print("-" * 50)
        student_id = input("შეიყვანეთ სტუდენტის ID: ").strip()
        
        for student in self.students:
            if student.student_id == student_id:
                print(f"სტუდენტი: {student.get_full_name()}")
                new_grade = input(f"ახალი ქულა (მიმდინარე: {student.grade}): ").strip()
                
                if not new_grade:
                    print("ქულა არ შეიძლება იყოს ცარიელი!")
                    return
                
                student.grade = new_grade
                self.save_students()
                print("✓ ქულა წარმატებით განახლდა!")
                return
        
        print("სტუდენტი ვერ მოიძებნა!")
    
    def student_portal(self, student):
        while True:
            student.display_info()
            print("\n1. გასვლა")
            choice = input("აირჩიეთ: ").strip()
            
            if choice == '1':
                print("მომხმარებელი სისტემიდან გასულია!")
                break
    
    def lecturer_portal(self, lecturer):
        while True:
            print("\nლექტორის პორტალი")
            print("-" * 50)
            lecturer.display_info()
            print("\nმენიუ")
            print("-" * 50)
            print("1. ახალი სტუდენტის დამატება")
            print("2. სტუდენტის წაშლა")
            print("3. ჩემი კურსის სტუდენტები")
            print("4. ყველა სტუდენტის სია")
            print("5. სტუდენტის ქულის განახლება")
            print("6. გასვლა")
            
            choice = input("\nაირჩიეთ ოპცია (1-6): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.remove_student()
            elif choice == '3':
                self.list_students_by_faculty(lecturer.course)
            elif choice == '4':
                self.list_all_students()
            elif choice == '5':
                self.update_student_grade()
            elif choice == '6':
                print("მომხმარებელი სისტემიდან გასულია!")
                break
            else:
                print("არასწორი არჩევანი! გთხოვთ აირჩიოთ 1-დან 6-მდე.")
            
            input("\nდააჭირეთ Enter-ს ოპერაციების გასაგრძელებლად...")
    
    def run(self):
        print("სტუდენტების მართვის სისტემა")
        print("-" * 50)
        
        while True:
            print("\nავტორიზაცია")
            print("-" * 50)
            email = input("მეილი (@nuga.edu.ge): ").strip()
            password = input("პაროლი: ").strip()
            
            user_type, user = self.authenticate(email, password)
            
            if user_type == 'student':
                print(f"\nმოგესალმებით, {user.get_full_name()}!")
                self.student_portal(user)
                break
            elif user_type == 'lecturer':
                print(f"\nმოგესალმებით, {user.get_full_name()}!")
                self.lecturer_portal(user)
                break
            else:
                print("არასწორი მეილი ან პაროლი!")
                retry = input("გსურთ ხელახლა ცდა? (y/n): ").strip().lower()
                if retry != 'y':
                    print("მომხმარებელი სისტემიდან გასულია!")
                    break


if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()
