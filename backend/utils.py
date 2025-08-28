# utils.py
def student_to_text(student: dict) -> str:
    # student expected to have keys name,dob,address,hobby,interest,skill
    parts = [
        f"Name: {student.get('name','')}",
        f"DOB: {student.get('dob','')}",
        f"Address: {student.get('address','')}",
        f"Hobby: {student.get('hobby','')}",
        f"Interest: {student.get('interest','')}",
        f"Skill: {student.get('skill','')}"
    ]
    return ". ".join([p for p in parts if p]) + "."
