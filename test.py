from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_game_board(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            with client.session_transaction() as sess:
             
                sess["highscore"] = 0
                sess["nplays"] = 0
                sess["board"] = []
            response = client.get("/")
            self.assertIn('board', sess)
            self.assertEqual(sess.get('highscore'),0)
            self.assertEqual(sess.get('nplays'),0)
            self.assertIn('<p>High Score:', response.get_data(as_text=True))
           
           
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.status_code,200)

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['response'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['response'], 'not-word')