from mec_energia import settings
from datetime import date

class CnpjValidator:
    '''
    https://blog.dbins.com.br/como-funciona-a-logica-da-validacao-do-cnpj
    https://www.macoratti.net/alg_cnpj.htm
    '''
    multipliers_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    multipliers_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    @classmethod
    def validate(cls, cnpj: str):
        if not cnpj.isdecimal() or len(cnpj) != 14:
            raise Exception('CNPJ must contain exactly 14 numerical digits')

        cnpj_digits = [int(d) for d in cnpj]
        cnpj_base = cnpj_digits[:13]
        expected_verified_digits = cnpj_digits[12:]

        verifier_digit_1 = cls._verify_digit(cls.multipliers_1, cnpj_base)
        verifier_digit_2 = cls._verify_digit(
            cls.multipliers_2, [*cnpj_base, verifier_digit_1])

        if [verifier_digit_1, verifier_digit_2] != expected_verified_digits:
            raise Exception('Invalid CNPJ')

    @staticmethod
    def _verify_digit(multipliers: list[int], base_digits: list[int]) -> int:
        multiplication_results = []
        for mult, cnpj_base_digit in zip(multipliers, base_digits):
            multiplication_results.append(mult * cnpj_base_digit)
        sum_result = sum(multiplication_results)

        sum_mod_11 = sum_result % 11
        if sum_mod_11 < 2:
            verifier_digit = 0
        else:
            verifier_digit = 11 - sum_mod_11

        return verifier_digit


class EnergyBillsDates:

    @classmethod
    def generate_dates_of_consumer_unit(cls, consumer_unit_date):
        energy_bills_list = []

        consumer_unit_month = consumer_unit_date.month
        consumer_unit_year = consumer_unit_date.year

        month = date.today().month
        year = date.today().year

        while (month != consumer_unit_month or year != consumer_unit_year):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @classmethod
    def generate_latest_dates_for_recommendation(cls):
        energy_bills_list = []

        month = date.today().month
        year = date.today().year

        for i in range(settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION):
            energy_bill, month, year = cls._create_energy_bill_date(month, year)
            energy_bills_list.append(energy_bill)

        return energy_bills_list

    @staticmethod
    def _create_energy_bill_date(month, year):
        month, year = (month - 1, year) if month != 1 else (12, year - 1)

        energy_bill = {
            'month': month,
            'year': year,
        }

        return (energy_bill, month, year)