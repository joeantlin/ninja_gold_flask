from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

@app.route('/')
def index():
    print('*'*80)
    print('I am Home')
    session.clear() # clears all keys
    return render_template('index.html')

@app.route('/user', methods=['POST'])
def user():
    print('*'*80)
    print('User Created')
    session['user'] = request.form['username']
    return redirect('/game')

@app.route('/game')
def game():
    print('*'*80)
    print(f"{session['user']}'s game")
    if 'gold' not in session:
        session['gold'] = 0
        session['tries'] = 0
        session['log'] = "<p class='blue'>Your search for Gold has begun</p>"
    print(f"My gold: {session['gold']}")
    print(f"My tries: {session['tries']}")
    return render_template('game.html')

@app.route('/process_gold', methods=['POST'])
def process_gold():
    counter = request.form['property']
    import random
    session['tries'] += 1
    if counter == 'farm':
        farm = random.randint(0, 30)
        session['gold'] += farm
        print(f"You've found {farm} more Gold!")
        session['log'] = f"<p>Working on the farm has earned you {farm} more Gold!</p>" + session['log']
    elif counter == 'cave':
        cave = random.randint(10, 20)
        session['gold'] += cave
        print(f"You've found {cave} more Gold!")
        session['log'] = f"<p>Exploring through the cave, you found {cave} more Gold!</p>" + session['log']
    elif counter == 'house':
        house = 15
        session['gold'] += house
        print(f"You've found {house} more Gold!")
        session['log'] = f"<p>While scavenging through the house, you found {house} more Gold!<p/>" + session['log']
    elif counter == 'casino':
        casino = random.randint(0, 50)
        gamble = random.randint(0, 1)
        if gamble > 0:
            session['gold'] += casino
            print(f"You've Won {casino} more Gold!")
            session['log'] = f"<p>You placed your bets and Won {casino} more Gold!</p>" + session['log']
        else:
            session['gold'] -= casino
            print(f"You've Lost {casino} more Gold!")
            session['log'] = f"<p class='red'>You placed your bets and Lost {casino} Gold!</p>" + session['log']
    if session['tries'] >= 15 and session['gold'] < 500:
        session['log'] = f"<p class='red'><b>You only earned {session['gold']} gold, you Lose!</b></p>" + session['log']
        session['gold'] = 0
        session['tries'] = 0
        session['log'] = f"<p class='blue'>{session['user']}'s search for gold begins again!</p>" + session['log']
    if session['gold'] >= 500:
        session['log'] = f"<p class='yellow'><b>You earned {session['gold']} gold, you Win!</b></p>" + session['log']
        session['gold'] = 0
        session['tries'] = 0
        session['log'] = f"<p class='blue'>{session['user']}'s search for gold begins again!</p>" + session['log']
    return redirect('/game')

#Restart for button
# @app.route('/newgame')
# def newgame():
#     session['gold'] = 0
#     session['tries'] = 0
#     session['log'] = f"<p class='blue'>{session['user']}'s search for gold begins again!</p>"
#     return redirect('/game')

@app.route('/end')
def endsession():
    session.clear() # clears all keyss
    #session.pop('count') # clears a specific key
    return redirect('/')


if __name__ =='__main__':
    app.run(debug=True)