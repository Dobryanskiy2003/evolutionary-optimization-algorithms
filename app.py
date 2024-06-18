import streamlit as st
import numpy as np
import random

def read_data(uploaded_file):
    lines = uploaded_file.getvalue().decode().splitlines()
    n = int(lines[0])
    data = []
    for line in lines[1:n+1]:
        if line:
            try:
                x, y = map(int, line.split(','))
                data.append((x, y))
            except ValueError:
                st.error(f"Невозможно преобразовать данные в строке: {line}")
    return data

def calculate_distance(data):
    n = len(data)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i, j] = np.sqrt((data[i][0] - data[j][0])**2 + (data[i][1] - data[j][1])**2)
    return dist

def calculate_total_distance(order, distance_matrix):
    total = 0
    for i in range(len(order) - 1):
        total += distance_matrix[order[i]][order[i+1]]
    total += distance_matrix[order[-1]][order[0]]
    return total

def tabu_search(data, tabu_size, max_iter):
    n = len(data)
    distance_matrix = calculate_distance(data)
    best_order = list(range(n))
    random.shuffle(best_order)
    best_total_distance = calculate_total_distance(best_order, distance_matrix)
    tabu_list = [best_order]

    for _ in range(max_iter):
        current_order = best_order.copy()
        i, j = random.sample(range(n), 2)
        current_order[i], current_order[j] = current_order[j], current_order[i]
        current_total_distance = calculate_total_distance(current_order, distance_matrix)

        if (current_total_distance < best_total_distance) and (current_order not in tabu_list):
            best_order = current_order
            best_total_distance = current_total_distance
            tabu_list.append(best_order)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

    return best_order, best_total_distance

st.markdown("""
# Алгоритмы эволюционной оптимизации
Лабораторная работа 1 \n
Выполнил студент группы **ФИТ-212 Добрянский Андрей**
""")

st.markdown("""
# Алгоритм табуированного поиска
Алгоритм табуированного поиска - это метаэвристический алгоритм поиска, используемый для решения комбинаторных задач оптимизации. Он итеративно исследует пространство решений, чтобы найти наилучшее решение. Алгоритм использует табу-список для хранения истории поиска и предотвращения циклического повторения решений.
""")

uploaded_file = st.file_uploader("Загрузите файл с координатами городов", type=['txt'])

if uploaded_file is not None:
    data = read_data(uploaded_file)

    tabu_size = st.slider('Размер табу-списка', min_value=1, max_value=400, value=10)
    max_iter = st.slider('Максимальное количество итераций', min_value=100, max_value=100000, value=1000)

    if st.button('Запустить алгоритм табуированного поиска'):
        best_order, best_total_distance = tabu_search(data, tabu_size, max_iter)
        st.write('Лучший порядок:', best_order)
        st.write('Лучшее общее расстояние:', best_total_distance)
