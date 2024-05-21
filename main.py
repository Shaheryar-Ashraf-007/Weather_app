import requests
from tkinter import *
import tkinter as tk
from opencage.geocoder import OpenCageGeocode
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

root = Tk()
root.title("Weather APP")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Your OpenWeatherMap API Key
API_KEY = '7c1957e24aa5680acde3629724a80605'
# Your OpenCage API Key
OPENCAGE_API_KEY = '0d2bec57a03c48068d6142d50b1d2342'  

def getWeather():
    city = textfield.get()
    print(f"City: {city}")  # Print the city name to the terminal
    
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    result = geocoder.geocode(city)
    
    if not result:
        print("City not found")  
        messagebox.showerror("Error", "City not found")
        return

    location = result[0]
    latitude = location['geometry']['lat']
    longitude = location['geometry']['lng']
    print(f"Latitude: {latitude}, Longitude: {longitude}")  

    obj = TimezoneFinder()
    timezone_result = obj.timezone_at(lng=longitude, lat=latitude)
    print(timezone_result)# Print the timezone result to the terminal
    
    home = pytz.timezone(timezone_result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    Clock.config(text=current_time)
    name.config(text="CURRENT WEATHER")
    

    # Fetch weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    
    # Print the JSON response for debugging
    print("Weather Data:", weather_data)
    
    if response.status_code == 200:
        # Ensure 'weather' key exists in the JSON data
        if 'weather' in weather_data and len(weather_data['weather']) > 0:
            try:
                # Extracting necessary data
                condition = weather_data['weather'][0]['main']
                description = weather_data['weather'][0]['description']
                temp = int(weather_data['main']['temp'])
                pressure = weather_data['main']['pressure']
                humidity = weather_data['main']['humidity']
                wind = weather_data['wind']['speed']
                
                # Update labels
                t.config(text=(temp, "°"))
                c.config(text=(condition, "|", "FEELS LIKE", temp, "°"))
                w.config(text=f"{wind} m/s")
                h.config(text=f"{humidity}%")
                d.config(text=description)
                p.config(text=f"{pressure} hPa")
            except KeyError as e:
                print(f"KeyError: {e}")
                messagebox.showerror("Error", f"Key not found in the response: {e}")
        else:
            print("Weather data not found in the response")
            messagebox.showerror("Error", "Weather data not found in the response")
    else:
        print("Failed to retrieve data from OpenWeatherMap")
        messagebox.showerror("Error", "Failed to retrieve data from OpenWeatherMap")

# Search box
Search_image = PhotoImage(file="G:\\weather app\\images\\search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=0)
textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=70, y=20)
textfield.focus()

Search_icon = PhotoImage(file="G:\\weather app\\images\\search_img.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=12)

# Logo image
logo_image = PhotoImage(file="G:\\weather app\\images\\logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Button
frame_image = PhotoImage(file="G:\\weather app\\images\\box.png")
frame = Label(image=frame_image)
frame.pack(padx=5, pady=5, side=BOTTOM)

#time 
name = Label(root, font=("arial", 15 , "bold"))
name.place(x=30,y=100)
Clock = Label(root, font=("Helvetica", 20))
Clock.place(x=30, y=130)


# Labels
Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef").place(x=120, y=400)
Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef").place(x=225, y=400)
Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef").place(x=430, y=400)
Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef").place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(text="....", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
