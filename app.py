from flask import Flask, render_template, jsonify
import pygame
import random
import json
import os

app = Flask(__name__)

# Инициализация pygame для воспроизведения звука
pygame.mixer.init()

# Файл для сохранения счётчика
COUNTER_FILE = "counter.json"

def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            return json.load(file).get("counter", 0)
    return 0

def save_counter(value):
    with open(COUNTER_FILE, "w") as file:
        json.dump({"counter": value}, file)

# Загружаем сохранённое значение счётчика
counter = load_counter()

def play_sound():
    sound = f"static/sounds/Mococo_BauBau_{random.randrange(1,17)}.mp3"
    sound_channel = pygame.mixer.find_channel(True)  # Находим свободный канал
    if sound_channel:
        sound_channel.play(pygame.mixer.Sound(sound))  # Воспроизводим звук на отдельном канале

@app.route("/")
def index():
    return render_template("index.html", baus=counter)

@app.route("/play")
def play():
    global counter
    counter += 1
    save_counter(counter)  # Сохраняем счётчик
    play_sound()
    return jsonify({"baus": counter, "toggle": True})

if __name__ == "__main__":
    pygame.mixer.set_num_channels(16)  # Устанавливаем количество каналов для одновременного воспроизведения
    app.run(host='0.0.0.0', port=5000, debug=True)
