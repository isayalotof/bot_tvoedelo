import sqlite3

from datetime import datetime, timedelta

from cfg import config as cf



class ListOfTime:
    def __init__(self, service_duration, target_date, wds = cf.working_day_start, wde = cf.working_day_end ):
        self.db_path = 'data/data.db'
        self.working_day_start = wds
        self.working_day_end = wde
        self.service_duration = service_duration
        self.target_date = target_date
        self.busy_intervals = self.load_busy_intervals()
        self.available_intervals = self.generate_time_slots()

    def load_busy_intervals(self):
        """
        Загружает занятые интервалы из базы данных для заданной даты и возвращает
        их в виде списка кортежей (start, end).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Запрос только для записей с совпадающей датой
        cursor.execute("SELECT time_start, duration FROM bookings WHERE date = ?", (self.target_date,))
        bookings = cursor.fetchall()
        conn.close()

        busy_intervals = []
        for time_start, duration in bookings:
            # Предполагаем, что время начала в базе хранится как "HH:MM"
            start_time = datetime.strptime(f"{self.target_date} {time_start}", "%d-%m-%Y %H:%M")
            end_time = start_time + timedelta(minutes=duration)
            busy_intervals.append((start_time, end_time))
        return busy_intervals

    def generate_time_slots(self):
        """
        Создает все возможные интервалы в течение рабочего дня с шагом в 20 минут.
        """
        timeslots = []
        current_time = datetime.strptime(f"{self.target_date} {self.working_day_start.strftime('%H:%M')}", "%d-%m-%Y %H:%M")

        # Генерируем интервалы с шагом в 20 минут, пока не достигнем конца рабочего дня
        while current_time + timedelta(minutes=self.service_duration) <= datetime.strptime(f"{self.target_date} {self.working_day_end.strftime('%H:%M')}", "%Y-%m-%d %H:%M"):
            timeslots.append(current_time)
            current_time += timedelta(minutes=20)

        return timeslots

    def is_slot_free(self, slot_start):
        """
        Проверяет, свободен ли данный интервал, проверяя на пересечения с занятыми интервалами.
        """
        slot_end = slot_start + timedelta(minutes=self.service_duration)
        for busy_start, busy_end in self.busy_intervals:
            if not (slot_end <= busy_start or slot_start >= busy_end):
                return False
        return True

    def get_free_intervals(self):
        """
        Возвращает список всех свободных временных интервалов.
        """
        return [slot.strftime("%H:%M") for slot in self.available_intervals if self.is_slot_free(slot)]


def get_weekday(date_str):
    # Парсим дату из строки
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Получаем номер дня недели (0 = Понедельник, 6 = Воскресенье)
    weekday_number = date_obj.weekday()
    # Список дней недели
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    # Возвращаем название дня недели
    return days[weekday_number]


def get_next_two_weeks_dates():
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(15)]
    return dates









