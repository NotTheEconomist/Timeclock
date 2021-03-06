from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey,\
                       ForeignKeyConstraint, Numeric
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, backref

from decimal import Decimal  # Job.rate

Base = declarative_base()

__all__ = ['Clocktime', 'Employee', 'Job']

class Clocktime(Base):
    """Table for clockin/clockout values

    ForeignKeys exist for Job and Employee
    many to one -> employee
    many to one -> job
    """

    __tablename__ = "clocktimes"
    id = Column(Integer, primary_key=True)
    time_in = Column(DateTime)
    time_out = Column(DateTime)
    employee_id = Column(Integer,ForeignKey('employees.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    # employee = many to one relationship with Employee
    # job = many to one relationship with Job

    @property
    def timeworked(self):
        return self.time_out - self.time_in

    def __str__(self):
        formatter="Employee: {employee.name}, "\
                  "Job: {job.abbr}, "\
                  "Start: {self.time_in}, "\
                  "End: {self.time_out}, "\
                  "Hours Worked: {self.timeworked}, "\
                  "ID# {self.id}"
        return formatter.format(employee=self.employee, job=self.job, self=self)

class Employee(Base):
    """Table for employees
    
    one to many -> clocktimes
    """

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    clocktimes = relationship('Clocktime', backref='employee')
    
    @property
    def name(self):
        return self.firstname + " " + self.lastname

    def __str__(self):
        return "{name:<70}{id:>10}".format(name=self.name,
                                           id="ID# " + str(self.id))

class Job(Base):
    """Table for jobs
    
    one to many -> clocktimes
    note that rate is cents/hr"""

    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    abbr = Column(String(16))
    rate = Column(Integer)  # cents/hr
    clocktimes = relationship('Clocktime', backref='job')

    def __str__(self):
        formatter = "Name: {name:<50} {abbr:>23}\n" \
                    "Rate: ${rate:<7.2f}/hr {id:>62}"
        return formatter.format(name=self.name,
                                abbr="Abbr: " + str(self.abbr),
                                rate=self.rate/100.0,
                                id="ID# " + str(self.id))
