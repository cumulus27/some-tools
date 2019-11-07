#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Simulate the interest of Wechat.
"""


class WeChat(object):
    def __init__(self, rate):
        self.rate = rate

        self.balance_yesterday = 0
        self.balance_today = 0

        self.today = 1
        self.interest_today = 0

        self.put_in_time = []
        self.put_in_money = {}

    def calculate_interest_today(self):
        self.interest_today = self.balance_yesterday*self.rate/10000

    def calculate_balance_today(self):
        self.balance_yesterday = self.balance_today
        self.balance_today = self.balance_today + self.interest_today

    def put_money_in(self, money):
        self.balance_today += money

    def calculate_put_plan(self, plan):
        for time, money in plan:
            self.put_in_time.append(time)
            self.put_in_money.update({time:money})

    def main_simulate(self):
        target_time = 365 * 30
        # put_plan = [(1,10000), (366, 10000), (731, 10000),
        #         (1096, 10000), (1461, 10000)]
        put_plan = [(1, 100000)]

        self.calculate_put_plan(put_plan)

        for d in range(target_time):
            self.calculate_interest_today()
            self.calculate_balance_today()

            if d in self.put_in_time:
                print(f"Put {self.put_in_money[d]} in {self.balance_today} on day{d}")
                self.put_money_in(self.put_in_money[d])
                print(f"Now we have {self.balance_today}")

            if d%10 == 0:
                print(f"Date: {d}, Balance: {self.balance_today}")


if __name__ == "__main__":

    interest_rate = 0.6371

    simulation = WeChat(interest_rate)
    simulation.main_simulate()

    print(simulation.balance_today)
