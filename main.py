import datetime as dt
import json  # Лишний импорт, нужно удалить.

#Ошибки в форматирование, между классами пропуск две строки, между функциями пропуск одна строка.

class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Лучше вынести в отдельный метод. Например. self.date = self._get_date(date=date)
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Имя переменной всегда с маленькой буквы. Избегаем похожие имена в одном проекте.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (today - record.date).days < 7 and (today - record.date).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    #При работе с ценами, лучше использовать тип Decimal
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    #Аргументы функции всегда строчными, usd_rate=USD_RATE
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ошибка в выражение. Так как курс рубля к рублю == 1, то можно указать cash_remained = cash_remained
            # Но так как мы значение этой переменной не меняем, то эту строчку можно удалить.
            # cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # В f-строках применяется только подстановка переменных и нет логических или арифметических операций,
            # вызовов функций и подобной динамики.
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Консистентность. Лучше придерживаться одного или f строки, или метод format.
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    def get_week_stats(self):
        # Лишний метод, удалить.
        super().get_week_stats()
