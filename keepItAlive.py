from flask import Flask
from threading import Thread

#KEEPS THE BOT ALIVE 
app = Flask('')

@app.route('/')
def home():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keepAlive():
  server = Thread(target=run)
  server.start()
