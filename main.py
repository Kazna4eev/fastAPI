from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# создаем модель, объекты которой будут храниться в бд
Base = declarative_base()


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )


# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

# создаем объект Person для добавления в бд
tom = Person(name="Tom", age=38)
db.add(tom)  # добавляем в бд
db.commit()  # сохраняем изменения
db.refresh(tom)  # обновляем состояние объекта
print(tom.id)  # можно получить установленный id

alice = Person(name="Alice", age=33)
kate = Person(name="Kate", age=28)
db.add_all([alice, kate])
db.commit()

# получение всех объектов
people = db.query(Person).all()
for p in people:
    print(f"{p.id}.{p.name} ({p.age})")

# получение одного объекта по id
first_person = db.get(Person, 1)
print(f"{first_person.name} - {first_person.age}")
# Tom - 38

people = db.query(Person).filter(Person.age > 30).all()
for p in people:
    print(f"{p.id}.{p.name} ({p.age})")

first = db.query(Person).filter(Person.id==1).first()
print(f"{first.name} ({first.age})")

# Обновление
# получаем один объект, у которого имя - Tom
tom = db.query(Person).filter(Person.id == 1).first()
print(f"{tom.id}.{tom.name} ({tom.age})")
# 1.Tom (38)

# изменениям значения
tom.name = "Tomas"
tom.age = 22

db.commit()  # сохраняем изменения

# проверяем, что изменения применены в бд - получаем один объект, у которого имя - Tomas
tomas = db.query(Person).filter(Person.id == 1).first()
print(f"{tomas.id}.{tomas.name} ({tomas.age})")
# 1.Tomas (22)

# Удаление
bob = db.query(Person).filter(Person.id==2).first()
db.delete(bob)  # удаляем объект
db.commit()     # сохраняем изменения

# приложение, которое ничего не делает
app = FastAPI()
