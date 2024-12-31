from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from datetime import datetime  # Import datetime for time calculations


app = Flask(__name__)




# Replace with your actual Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7643200755:AAEnY79hQQ98ovHCmOp-IOcscwvDGqUbEMM'
CHAT_ID = '6214817938'

def send_to_telegram(name, birthday, phonenumber, location, mood, gender, knowledge, meeting, beef, reason, opinion, isgood, isbad, song):
    message = f"New Questionnaire Submission:\nName 🙂: {name}\nBirthday 🎆: {birthday}\nPhonenumber ☎: {phonenumber}\nLocation 🌍 🌎 🌏: {location}\nGender 👭: {gender}\nMood 😉: {mood}\nDo you know SVJ?: {knowledge}\nHave you ever met him?: {meeting}\nAre you mad at him?: {beef}\nPlease provide a reason: \n{reason}\nHow was 2024?: {opinion}\nWhat was the best thing of 2024?: {isgood}\nWhat was the worst thing of 2024?: {isbad}\nSong Genre🎶: {song}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        print("Message sent to Telegram successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")



# Home route to display the questionnaire
@app.route('/', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'POST':
        # Process the form data
        name = request.form.get('name')
        phonenumber = request.form.get('phonenumber')
        birthday = request.form.get('birthday')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        gender = request.form.get('gender')
        mood = request.form.get('mood')
        timezone = request.form.get('location')
        knowledge = request.form.get('knowledge')
        meeting = request.form.get('meeting')
        beef = request.form.get('beef')
        reason = request.form.get('reason')
        opinion = request.form.get('opinion')
        isgood = request.form.get('isgood')
        isbad = request.form.get('isbad')
        song_genre = request.form.get('song')
        
         # Create a location string
        location = f"Latitude: {latitude}, Longitude: {longitude}"
        
        
        print(f"Received data: Name 🙂: {name}, \nBirthday 🎆: {birthday}, \nPhonenumber ☎: {phonenumber}, \nLocation 🌍 🌎 🌏: {timezone}, \nSong Genre🎶: {song_genre} \nGender 👭: {gender}, \nMood 😉: {mood}, \nDo you know svj: {knowledge}, \nHave you ever met him: {meeting}, \nAre you mad at him: {beef}, \nPlease provide a reason: \n{reason}, How was 2024?: {opinion}, What was the best thing of 2024?: \n{isgood}, What was the worst thing of 2024?: \n{isbad}")  # Debugging line
        
        # Send data to Telegram
        send_to_telegram(name, birthday, phonenumber, location, mood, gender, knowledge, meeting, beef, reason, opinion, isgood, isbad, song_genre)
        
        return redirect(url_for('thank_you', song_genre=song_genre, name=name))  # Redirect to happy new year page

    return render_template('new_year_page.html')
    

# Route to handle location data
@app.route('/send-location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Send location to Telegram
    location_message = f"User 's Location:\nLatitude: {latitude}\nLongitude: {longitude}"
    send_to_telegram("Location Update", "", "", location_message, "")
    
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")
    
    return jsonify({"status": "success", "message": "Location sent successfully!"})

songs = {
    
    "bongo": ["/static/images/rayvany.mp3", "Rayvany - Bongo"],
    "luo": ["/static/images/osiepe.mp3", "Osiepe - Luo"],
    "genge": ["/static/images/figa.mp3", "Figa - Genge"],
    "rhumba": ["/static/images/mamou II.mp3", "Mamou II - Rhumba"],
    "amapiano": ["/static/images/unclewaffles.mp3", "Yahyuppiyah - Amapiano"],
    "arbatone": ["/static/images/tictac.mp3", "Tic Tac remix - Arbatone"], 
    "reggae": ["/static/images/dube.mp3", "Remember me - Reggae"],
    "dancehall": ["/static/images/kartel.mp3", "Secret - Dancehall"],
    "afrobeat": ["/static/images/testedapprovedtrusted.mp3", "Tested, approved and trusted - Afrobeat"],
    "kenyan drill": ["/static/images/kichwambaya.mp3", "Kichwambaya - Kenyan Drill"],
    "coast": ["/static/images/anangalangala.mp3", "Anangalangala - Coast"],
    "kikamba": ["/static/images/pewapewa.mp3", "Pewapewa - Kikamba"],
    "riddim": ["/static/images/chronixx.mp3", "Smile jamaica - Riddim"],
    "gospel": ["/static/images/yahweh.mp3", "Yahweh - Gospel"],
    
}

@app.route('/thank_you')
def thank_you():

    name = request.args.get('name', '')
    song_genre = request.args.get('song_genre', '') 
    
    # Fetch the song data based on the selected genre
    song_data = songs.get(song_genre, None)
    
    if song_data:
        song_path, song_title = song_data
    else:
        # Default song if the genre is not found
        song_path, song_title = "/static/images/tictac.mp3", "Default Song Title"
    
    return render_template('new_year_message.html', song_path=song_path, song_title=song_title, name=name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)