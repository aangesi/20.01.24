import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Загрузка данных
data = pd.read_csv("shapes_data.csv")  # Укажи свой путь к файлу
X = data[['площадь', 'периметр']].values
y = data['метка'].values

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Нормализация данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Создание модели
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(2,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # Выходной слой для бинарной классификации
])

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Оценка точности
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Точность модели: {test_acc * 100:.2f}%")

# Функция предсказания
def predict_shape(area, perimeter):
    features = scaler.transform([[area, perimeter]])
    prediction = model.predict(features)[0][0]
    return "Круг" if prediction > 0.5 else "Квадрат"

# Пример работы
area_input = float(input("Введите площадь: "))
perimeter_input = float(input("Введите периметр: "))
print(f"Это {predict_shape(area_input, perimeter_input)}")
