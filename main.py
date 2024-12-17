from pyscript import document
import numpy as np
from statsmodels.stats.power import NormalIndPower
import statsmodels.api as sm


def get_data(event):
    # Получение данных из полей ввода
    baseline = float(document.querySelector("#baseline").value)
    mde = float(document.querySelector("#mde").value)
    ratio = float(document.querySelector("#ratio").value)
    power = float(document.querySelector("#power").value)
    alpha = float(document.querySelector("#level").value)

    # Создание объекта для анализа мощности
    analysis = NormalIndPower()
    effect_size = sm.stats.proportion_effectsize(baseline, baseline + mde)

    # Вычисление размера выборки
    result = analysis.solve_power(effect_size=effect_size, power=power, alpha=alpha, ratio=ratio, alternative='two-sided')
    sample_size = int(np.ceil(result))

    # Запись результатов в HTML-элементы
    document.querySelector("#control-group").innerText = str(round(sample_size))
    document.querySelector("#test-group").innerText = str(round(sample_size * ratio))


from statsmodels.stats.proportion import proportions_ztest

def evaluate_experiment(event):
    # Получение данных из HTML
    alpha = float(document.querySelector("#level").value)

    actual_cgs = float(document.querySelector("#actual-cgs").value)
    conversions_c = float(document.querySelector("#converstions-c").value)
    actual_tgs = float(document.querySelector("#actual-tgs").value)
    conversions_t = float(document.querySelector("#converstions-t").value)

    # Проведение Z-теста
    _, p_value = proportions_ztest([conversions_c, conversions_t], [actual_cgs, actual_tgs], alternative='two-sided')
    
    # Конверсии и разница
    cr_c = conversions_c / actual_cgs
    cr_t = conversions_t / actual_tgs
    difference = cr_t - cr_c

    # Решение по результатам теста
    decision = "Positive" if p_value < alpha else "Negative"

    # Запись результатов в HTML-элементы
    document.querySelector("#cgs").innerText = str(round(actual_cgs))
    document.querySelector("#tgs").innerText = str(round(actual_tgs))

    document.querySelector("#cntr-c").innerText = str(round(conversions_c))
    document.querySelector("#test-c").innerText = str(round(conversions_t))

    document.querySelector("#cr-c").innerText = str(round(cr_c, 4))
    document.querySelector("#cr-t").innerText = str(round(cr_t, 4))

    document.querySelector("#diff").innerText = str(round(difference, 4))
    document.querySelector("#pvalue").innerText = str(round(p_value, 5))

    document.querySelector("#decision").innerText = decision
    document.querySelector("#stat-sig").innerText = str(alpha)