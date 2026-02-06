from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import validator, ValidationError
import re
from datetime import datetime

class Person(SQLModel):
    fname: str = Field(max_length=10)
    lname: str = Field(max_length=10)
    id: str = Field(max_length=10, min_length=10)
    born_city: str
    birth: str
    address: str = Field(max_length=100)
    postal_code: str = Field(max_length=10, min_length=10)
    hphone: str
    cphone: str
    department: str
    major: str

    class Config:
        validate_assignment = True
        extra = "forbid"
        strict = True

    @validator("fname", pre=True)
    def validate_fname(cls, v):
        if not isinstance(v, str) or not re.match(r'^[\u0600-\u06FF\s]+$', v) or len(v) > 10:
            raise ValueError("نام باید فقط حاوی کاراکترهای فارسی باشد و حداکثر ۱۰ کاراکتر داشته باشد")
        return v

    @validator("lname", pre=True)
    def validate_lname(cls, v):
        if not isinstance(v, str) or not re.match(r'^[\u0600-\u06FF\s]+$', v) or len(v) > 10:
            raise ValueError("نام خانوادگی باید فقط حاوی کاراکترهای فارسی باشد و حداکثر ۱۰ کاراکتر داشته باشد")
        return v

    @validator("id", pre=True)
    def validate_id(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 10):
            raise ValueError("کد ملی باید عدد ۱۰ رقمی باشد")
        return v

    @validator("born_city", pre=True)
    def validate_born_city(cls, v):
        cities = [
            "تهران", "مشهد", "اصفهان", "کرج", "شیراز", "تبریز", "قم", "اهواز", "کرمانشاه",
            "ارومیه", "رشت", "زاهدان", "همدان", "کرمان", "یزد", "اردبیل", "بندرعباس",
            "اراک", "اسلامشهر", "زنجان", "سنندج", "قزوین", "خرم‌آباد", "گرگان",
            "ساری", "بجنورد", "بوشهر", "بیرجند", "ایلام", "شهرکرد", "یاسوج"
        ]
        if not isinstance(v, str) or v not in cities:
            raise ValueError("شهر باید یکی از مراکز استان باشد")
        return v

    @validator("birth", pre=True)
    def validate_birth(cls, v):
        if not isinstance(v, str):
            raise ValueError("تاریخ تولد باید رشته باشد")
        try:
            year, month, day = map(int, v.split("/"))
            if not (1300 <= year <= 1400 and 1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("سال باید بین ۱۳۰۰ تا ۱۴۰۰، ماه بین ۱ تا ۱۲ و روز بین ۱ تا ۳۱ باشد")
        except:
            raise ValueError("فرمت تاریخ باید به صورت شمسی YYYY/MM/DD باشد")
        return v

    @validator("address", pre=True)
    def validate_address(cls, v):
        if not isinstance(v, str) or len(v) > 100:
            raise ValueError("آدرس باید حداکثر ۱۰۰ کاراکتر باشد")
        return v

    @validator("postal_code", pre=True)
    def validate_postal_code(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 10):
            raise ValueError("کد پستی باید عدد ۱۰ رقمی باشد")
        return v

    @validator("cphone", pre=True)
    def validate_cphone(cls, v):
        if not isinstance(v, str) or not re.match(r'^09\d{9}$', v):
            raise ValueError("تلفن همراه باید مطابق استاندارد ایران باشد (مثال: ۰۹۱۲۳۴۵۶۷۸۹)")
        return v

    @validator("hphone", pre=True)
    def validate_hphone(cls, v):
        if not isinstance(v, str) or not re.match(r'^0\d{2,3}\d{7}$', v):
            raise ValueError("تلفن ثابت باید مطابق استاندارد ایران باشد (مثال: ۰۲۱۱۲۳۴۵۶۷۸)")
        return v

    @validator("department", pre=True)
    def validate_department(cls, v):
        departments = ["فنی مهندسی", "علوم پایه", "اقتصاد"]
        if not isinstance(v, str) or v not in departments:
            raise ValueError("دانشکده باید یکی از فنی مهندسی، علوم پایه یا اقتصاد باشد")
        return v

    @validator("major", pre=True)
    def validate_major(cls, v):
        majors = {
            "فنی مهندسی": [
                "مهندسی کامپیوتر", "مهندسی برق", "مهندسی مکانیک", "مهندسی عمران",
                "مهندسی صنایع", "مهندسی شیمی", "مهندسی مواد", "مهندسی هوافضا",
                "مهندسی نفت", "مهندسی معماری"
            ],
            "علوم پایه": [
                "ریاضی", "فیزیک", "شیمی", "زیست‌شناسی", "زمین‌شناسی",
                "آمار", "علوم کامپیوتر", "بیوشیمی", "میکروبیولوژی", "ژنتیک"
            ],
            "اقتصاد": [
                "اقتصاد", "مدیریت بازرگانی", "حسابداری", "مدیریت مالی",
                "مدیریت صنعتی", "اقتصاد کشاورزی", "اقتصاد بین‌الملل",
                "بانکداری", "بیمه", "مدیریت دولتی"
            ]
        }
        if not isinstance(v, str):
            raise ValueError("رشته تحصیلی باید رشته باشد")
        for dept, major_list in majors.items():
            if v in major_list:
                return v
        raise ValueError("رشته تحصیلی باید یکی از رشته‌های مرتبط با دانشکده باشد")

class Course(SQLModel, table=True):
    cid: str = Field(primary_key=True, max_length=5, min_length=5)
    Cname: str = Field(max_length=25)
    department: str
    credit: int

    class Config:
        validate_assignment = True
        extra = "forbid"
        strict = True

    @validator("cid", pre=True)
    def validate_cid(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 5):
            raise ValueError("کد درس باید عدد ۵ رقمی باشد")
        return v

    @validator("Cname", pre=True)
    def validate_Cname(cls, v):
        if not isinstance(v, str) or not re.match(r'^[\u0600-\u06FF\s]+$', v) or len(v) > 25:
            raise ValueError("نام درس باید فقط حاوی کاراکترهای فارسی باشد و حداکثر ۲۵ کاراکتر داشته باشد")
        return v

    @validator("department", pre=True)
    def validate_department(cls, v):
        departments = ["فنی مهندسی", "علوم پایه", "اقتصاد"]
        if not isinstance(v, str) or v not in departments:
            raise ValueError("دانشکده باید یکی از فنی مهندسی، علوم پایه یا اقتصاد باشد")
        return v

    @validator("credit", pre=True)
    def validate_credit(cls, v):
        if not isinstance(v, int) or v < 1 or v > 4:
            raise ValueError("تعداد واحد باید بین ۱ تا ۴ باشد")
        return v

class Professor(Person, table=True):
    lid: str = Field(primary_key=True, max_length=6, min_length=6)
    lcourse_ids: Optional[str] = None

    @validator("lid", pre=True)
    def validate_lid(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 6):
            raise ValueError("کد استاد باید عدد ۶ رقمی باشد")
        return v

    @validator("lcourse_ids", pre=True)
    def validate_lcourse_ids(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("کد دروس باید رشته باشد")
        return v

class Student(Person, table=True):
    stid: str = Field(primary_key=True)
    father: str
    ids_number: str = Field(max_length=6, min_length=6)
    ids_letter: str = Field(max_length=1)
    ids_code: str = Field(max_length=2, min_length=2)
    married: str
    scourse_ids: Optional[str] = None
    lids: Optional[str] = None

    @validator("stid", pre=True)
    def validate_stid(cls, v):
        if not isinstance(v, str) or len(v) != 11 or not v.isdigit():
            raise ValueError("شماره دانشجویی باید یک رشته 11 رقمی باشد")
        year_part = v[:3]
        fixed_part = v[3:9]
        unique_part = v[9:]
        if not (385 <= int(year_part) <= 403):
            raise ValueError("سال ورود باید بین *385* تا *403* باشد (بدون احتساب 1000، مثلاً 403 برای سال 1403)")
        if fixed_part != "114150":
            raise ValueError("بخش میانی شماره دانشجویی باید *114150* باشد")
        if len(unique_part) != 2:
            raise ValueError("بخش منحصر به فرد باید *2 رقم* باشد")
        return v

    @validator("father", pre=True)
    def validate_father(cls, v):
        if not isinstance(v, str) or not re.match(r'^[\u0600-\u06FF\s]+$', v) or len(v) > 10:
            raise ValueError("نام پدر باید فقط حاوی کاراکترهای فارسی و فاصله باشد و حداکثر ۱۰ کاراکتر داشته باشد")
        return v

    @validator("ids_number", pre=True)
    def validate_ids_number(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 6):
            raise ValueError("سریال شناسنامه باید عدد ۶ رقمی باشد")
        return v

    @validator("ids_letter", pre=True)
    def validate_ids_letter(cls, v):
        persian_letters = "الفبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
        if not isinstance(v, str) or v not in persian_letters:
            raise ValueError("حرف سریال شناسنامه باید یکی از حروف الفبای فارسی باشد")
        return v

    @validator("ids_code", pre=True)
    def validate_ids_code(cls, v):
        if not isinstance(v, str) or not (v.isdigit() and len(v) == 2):
            raise ValueError("کد سریال شناسنامه باید عدد ۲ رقمی باشد")
        return v

    @validator("married", pre=True)
    def validate_married(cls, v):
        if not isinstance(v, str) or v not in ["مجرد", "متاهل"]:
            raise ValueError("وضعیت تاهل باید مجرد یا متاهل باشد")
        return v

    @validator("scourse_ids", pre=True)
    def validate_scourse_ids(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("کد دروس باید رشته باشد")
        return v

    @validator("lids", pre=True)
    def validate_lids(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("کد اساتید باید رشته باشد")
        return v

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/students/")
def create_student(student: Student, session: SessionDep) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.get("/students/")
def read_students(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Student]:
    students = session.exec(select(Student).offset(offset).limit(limit)).all()
    return students

@app.get("/students/{stid}")
def read_student(stid: str, session: SessionDep) -> Student:
    student = session.get(Student, stid)
    if not student:
        raise HTTPException(status_code=404, detail="دانشجو یافت نشد")
    return student

@app.put("/students/{stid}")
def update_student(stid: str, student: Student, session: SessionDep) -> Student:
    db_student = session.get(Student, stid)
    if not db_student:
        raise HTTPException(status_code=404, detail="دانشجو یافت نشد")
    student_data = student.dict(exclude_unset=True)
    for key, value in student_data.items():
        setattr(db_student, key, value)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.delete("/students/{stid}")

def delete_student(stid: str, session: SessionDep):
    student = session.get(Student, stid)
    if not student:
        raise HTTPException(status_code=404, detail="دانشجو یافت نشد")
    session.delete(student)
    session.commit()
    return {"ok": True}

@app.post("/professors/")
def create_professor(professor: Professor, session: SessionDep) -> Professor:
    session.add(professor)
    session.commit()
    session.refresh(professor)
    return professor

@app.get("/professors/")
def read_professors(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Professor]:
    professors = session.exec(select(Professor).offset(offset).limit(limit)).all()
    return professors

@app.get("/professors/{lid}")
def read_professor(lid: str, session: SessionDep) -> Professor:
    professor = session.get(Professor, lid)
    if not professor:
        raise HTTPException(status_code=404, detail="استاد یافت نشد")
    return professor

@app.put("/professors/{lid}")
def update_professor(lid: str, professor: Professor, session: SessionDep) -> Professor:
    db_professor = session.get(Professor, lid)
    if not db_professor:
        raise HTTPException(status_code=404, detail="متاسفانه اسنادی یا این مشخصات یافت نسد")
    professor_data = professor.dict(exclude_unset=True)
    for key, value in professor_data.items():
        setattr(db_professor, key, value)
    session.add(db_professor)
    session.commit()
    session.refresh(db_professor)
    return db_professor

@app.delete("/professors/{lid}")
def delete_professor(lid: str, session: SessionDep):
    professor = session.get(Professor, lid)
    if not professor:
        raise HTTPException(status_code=404, detail="استاد یافت نشد")
    session.delete(professor)
    session.commit()
    return {"ok": True}

@app.post("/courses/")
def create_course(course: Course, session: SessionDep) -> Course:
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

@app.get("/courses/")
def read_courses(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Course]:
    courses = session.exec(select(Course).offset(offset).limit(limit)).all()
    return courses

@app.get("/courses/{cid}")
def read_course(cid: str, session: SessionDep) -> Course:
    course = session.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="درس یافت نشد")
    return course

@app.put("/courses/{cid}")
def update_course(cid: str, course: Course, session: SessionDep) -> Course:
    db_course = session.get(Course, cid)
    if not db_course:
        raise HTTPException(status_code=404, detail="درس یافت نشد")
    course_data = course.dict(exclude_unset=True)
    for key, value in course_data.items():
        setattr(db_course, key, value)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@app.delete("/courses/{cid}")
def delete_course(cid: str, session: SessionDep):
    course = session.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="درس یافت نشد")
    session.delete(course)
    session.commit()
    return {"ok": True}