import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

API_KEY = "01e3fe4b3debbcb25fdb98c33dae94e3"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    # URLs for current weather and forecast
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        current_data = requests.get(current_url).json()
        forecast_data = requests.get(forecast_url).json()

        # Check if city found
        if current_data.get('cod') != 200:
            messagebox.showerror("Error", f"City not found: {city}")
            return

        # Display current weather
        temp = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        description = current_data['weather'][0]['description'].title()
        icon_code = current_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        weather_result.config(text=f"Temperature: {temp}°C\nHumidity: {humidity}%\nCondition: {description}")

        # Load and display weather icon
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_img = ImageTk.PhotoImage(icon_image)
        weather_icon.config(image=icon_img)
        weather_icon.image = icon_img

        # Prepare data for forecast graph
        temps = []
        times = []

        for entry in forecast_data['list']:
            dt_txt = entry['dt_txt']
            temp = entry['main']['temp']
            dt_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            times.append(dt_obj)
            temps.append(temp)

        # Plot forecast graph
        ax.clear()
        ax.plot(times, temps, marker='o', color='blue')
        ax.set_title(f"5-Day Forecast: {city}")
        ax.set_ylabel("Temperature (°C)")
        ax.set_xlabel("Date-Time")
        ax.grid(True)
        fig.autofmt_xdate()
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data.\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Weather Forecasting Dashboard")
root.geometry("800x600")

tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=5)
city_entry = tk.Entry(root, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather).pack(pady=10)

weather_result = tk.Label(root, text="", font=("Arial", 12), justify="left")
weather_result.pack(pady=10)

weather_icon = tk.Label(root)
weather_icon.pack()

fig, ax = plt.subplots(figsize=(7, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()