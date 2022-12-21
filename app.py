
from flask import Flask,request,render_template,jsonify,session
from boggle import Boggle

app=Flask(__name__)
app.config["SECRET_KEY"]='secretsecret'

boggle_game = Boggle()



@app.route("/")
def show_game_board():
    """show game board"""
    board=boggle_game.make_board()
    session['board']=board
    highscore=session.get("highscore",0)
    nplays=session.get("nplays",0)
    
    return render_template("showboard.html",board=board,highscore=highscore,nplays=nplays)

@app.route("/check-word")
def check_word():
    """check see if answer is in the dictionary"""
    word=request.args['word']
    board=session['board']
    response_string=boggle_game.check_valid_word(board,word)

    return jsonify({'response': response_string})


@app.route('/end-game',methods=["POST"])
def end_game():
    
    score=request.json["score"]
    highscore=session.get("highscore",0)
    nplays=session.get("nplays",0)

    session["highscore"]=max(score,highscore)
    session["nplays"]=nplays+1

    return "game over"
