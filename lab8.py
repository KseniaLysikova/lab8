from datetime import date
import datetime
import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget,
                             QAbstractScrollArea, QVBoxLayout,
                             QHBoxLayout, QTableWidget,
                             QGroupBox, QTableWidgetItem,
                             QPushButton, QMessageBox)

curr_date = date.today()
current_date_string = curr_date.strftime('%m,%d,%y')
curr_week = datetime.date(int(current_date_string[6:8]), int(current_date_string[3:5]),
                          int(current_date_string[0:2])).isocalendar().week


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()
        self._create_timetable_tab()
        self._create_subject_tab()
        self._create_teacher_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="bot",
                                     user="postgres",
                                     password="123456",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_schedule_tab(self):
        self.shedule_tab = QWidget()

        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)
        self.shbox1.addWidget(self.saturday_gbox)
        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()
        self._create_saturday_table()
        self.update_schedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_contents)
        self.shedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()

        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_monday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()

        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tuesday_table.setColumnCount(4)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_tuesday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()

        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.wednesday_table.setColumnCount(4)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_wednesday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()

        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.thursday_table.setColumnCount(4)
        self.thursday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_thursday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table(self):
        self.friday_table = QTableWidget()

        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.friday_table.setColumnCount(4)
        self.friday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_friday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _create_saturday_table(self):
        self.saturday_table = QTableWidget()

        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.saturday_table.setColumnCount(4)
        self.saturday_table.setHorizontalHeaderLabels(["Subject", "Time", "Room", "Teacher"])
        self._update_saturday_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.saturday_table)
        self.saturday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Понедельник' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.monday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))

        self.monday_table.resizeRowsToContents()

    def _update_tuesday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Вторник' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.tuesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.tuesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
        self.tuesday_table.resizeRowsToContents()

    def _update_wednesday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Среда' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.wednesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.wednesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
        self.wednesday_table.resizeRowsToContents()

    def _update_thursday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Четверг' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.thursday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.thursday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
        self.thursday_table.resizeRowsToContents()

    def _update_friday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Пятница' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.friday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.friday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
        self.friday_table.resizeRowsToContents()

    def _update_saturday_table(self):
        self.cursor.execute("SELECT s.subject_name, tt.start_time, tt.room_numb,"
                            "tr.full_name FROM subject s, timetable tt, teacher tr WHERE s.subject_id = tr.subject "
                            "AND s.subject_id = tt.subject AND day_name = 'Суббота' AND tt.week =" + str(
            (curr_week % 2) + 1))

        records = list(self.cursor.fetchall())
        records.append(["", "", "", ""])
        self.saturday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            self.saturday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.saturday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.saturday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.saturday_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
        self.saturday_table.resizeRowsToContents()

    def _create_timetable_tab(self):
        self.timetable_tab = QWidget()

        self.tabs.addTab(self.timetable_tab, "Timetable")
        self.timetable_gbox = QGroupBox("Timetable Table")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.timetable_gbox)
        self._create_timetable_table()
        self.update_timetable_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_timetable_button)
        self.update_timetable_button.clicked.connect(self._update_timetable_table)
        self.timetable_tab.setLayout(self.svbox)

    def _create_timetable_table(self):
        self.timetable_table = QTableWidget()

        self.timetable_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.timetable_table.setColumnCount(8)
        self.timetable_table.setHorizontalHeaderLabels(["Id", "Week", "Day name", "Subject", "Room", "Time"])
        self._update_timetable_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.timetable_table)
        self.timetable_gbox.setLayout(self.mvbox)

    def _update_timetable_table(self):
        self.cursor.execute("SELECT * FROM timetable")

        records = list(self.cursor.fetchall())
        records.append(["", "", "", "", "", ""])
        self.timetable_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            createButton = QPushButton("Create")
            delButton = QPushButton("Delete")
            self.timetable_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.timetable_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.timetable_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.timetable_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.timetable_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.timetable_table.setItem(i, 5, QTableWidgetItem(str(r[5])))
            self.timetable_table.setCellWidget(i, 6, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self._update_timetable_row(num))
            self.timetable_table.setCellWidget(len(records) - 1, 6, createButton)
            createButton.clicked.connect(lambda ch, num=i: self._create_timetable_row(num))
            self.timetable_table.setCellWidget(i, 7, delButton)
            delButton.clicked.connect(lambda ch, num=r[0]: self._delete_timetable_row(num))
        self.timetable_table.resizeRowsToContents()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()

        self.tabs.addTab(self.subject_tab, "Subject")
        self.subject_gbox = QGroupBox("Subject Table")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.subject_gbox)
        self._create_subject_table()
        self.update_subject_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_subject_table)
        self.subject_tab.setLayout(self.svbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()

        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["Subject id", "Subject"])
        self._update_subject_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject")

        records = list(self.cursor.fetchall())
        records.append(["", ""])
        self.subject_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            createButton = QPushButton("Create")
            delButton = QPushButton("Delete")
            self.subject_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self._update_subject_row(num))
            self.subject_table.setCellWidget(len(records) - 1, 2, createButton)
            createButton.clicked.connect(lambda ch, num=i: self._create_subject_row(num))
            self.subject_table.setCellWidget(i, 3, delButton)
            delButton.clicked.connect(lambda ch, num=r[0]: self._delete_row(num))
        self.subject_table.resizeRowsToContents()

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()

        self.tabs.addTab(self.teacher_tab, "Teacher")
        self.teacher_gbox = QGroupBox("Teacher Table")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.teacher_gbox)
        self._create_teacher_table()
        self.update_teacher_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_teacher_table)
        self.teacher_tab.setLayout(self.svbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()

        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["Teacher id", "Teacher name", "Subject id", "", ""])
        self._update_teacher_table()
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher")

        records = list(self.cursor.fetchall())
        records.append(["", "", "", "", "", ""])
        self.teacher_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            createButton = QPushButton("Create")
            delButton = QPushButton("Delete")
            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self._update_teacher_row(num))
            self.teacher_table.setCellWidget(i, 4, delButton)
            self.teacher_table.setCellWidget(len(records) - 1, 3, createButton)
            createButton.clicked.connect(lambda ch, num=i: self._create_teacher_row(num))
            delButton.clicked.connect(lambda ch, num=r[0]: self._delete_row(num))
        self.teacher_table.resizeRowsToContents()

    def _update_timetable_row(self, rowNum):
        row = list()

        for i in range(self.timetable_table.columnCount()):
            try:
                row.append(self.timetable_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(
                "UPDATE timetable SET (week, day_name, subject, room_numb, start_time) =" + "(" + str(row[1]) + ", " +
                "'" + str(row[2]) + "'" + ", " + str(row[3]) + ", " + str(row[4]) + ", " + "'" + str(row[5]) + "'" + ")"
                + "WHERE id = " + str(row[0])
            )

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_timetable_row(self, rowNum):
        row = list()

        for i in range(self.timetable_table.columnCount()):
            try:
                row.append(self.timetable_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(
                "INSERT INTO timetable VALUES" + "(" + str(row[0]) + ", " + str(row[1]) + ", " +
                "'" + str(row[2]) + "'" + ", " + str(row[3]) + ", " + str(row[4]) + ", " + "'" + str(row[5])
                + "'" + ")"
            )

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_subject_row(self, rowNum):
        row = list()
        row1 = list()

        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)

        row1.append(int(row[0]))
        row1.append(row[1])
        try:
            self.cursor.execute(
                "UPDATE subject SET subject_name =" + "'" + str(row1[1]) + "'" + "WHERE subject_id =" + str(row1[0]))

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_subject_row(self, rowNum):
        row = list()
        row1 = list()

        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)

        row1.append(int(row[0]))
        row1.append(row[1])
        try:
            self.cursor.execute(
                "INSERT INTO subject VALUES" + "(" + str(row1[0]) + ", " + "'" + str(row1[1]) + "'" + ")")

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_teacher_row(self, rowNum):
        row = list()
        row1 = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        row1.append(int(row[0]))
        row1.append(row[1])
        row1.append(int(row[2]))
        try:
            self.cursor.execute(
                "UPDATE teacher SET (full_name, subject) =" + "(" + "'" + str(row1[1]) + "'" + ", " + str(row[2]) + ")"
                + "WHERE subject =" + str(row1[0])
            )

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_teacher_row(self, rowNum):
        row = list()
        row1 = list()

        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)

        row1.append(int(row[0]))
        row1.append(row[1])
        row1.append(int(row[2]))
        try:
            self.cursor.execute(
                "INSERT INTO teacher VALUES" + "(" + str(row1[0]) + ", " + "'" + str(row1[1]) + "'" + ", " +
                str(row1[2]) + ")")

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_row(self, rowNum):
        self.cursor.execute("DELETE FROM subject WHERE subject_id=" + str(rowNum))
        self.conn.commit()
        self._update_contents()

    def _delete_timetable_row(self, rowNum):
        self.cursor.execute("DELETE FROM timetable WHERE id=" + str(rowNum))
        self.conn.commit()
        self._update_contents()

    def _update_contents(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_friday_table()
        self._update_saturday_table()
        self._update_timetable_table()
        self._update_teacher_table()
        self._update_subject_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
