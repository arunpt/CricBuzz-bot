from pycricbuzz import Cricbuzz
from telegram import InlineKeyboardMarkup ,InlineKeyboardButton
from datetime import datetime, timedelta
import time, json

class Cricket:
    def __init__(self):
        self.cb = Cricbuzz()
        self.all_matches = self.cb.matches()
        self.run = True
        
    def live_matches(self):
        msg = "*  🏏 All live matches  *\n\n"
        for match in self.all_matches:
            if match['mchstate'] == 'inprogress':
                msg += match["team1"]["name"]+" v/s " + match["team2"]["name"]+ "," \
                     + match["srs"] + " - " + match["mnum"] + "\n\n"
            else:
                msg += "No live matches"
        return msg
            
    def commentary(self, match_id):
        commentary = self.cb.commentary(match_id)
        msg = f"Live commentary - {match_id}\n\n"
        for com in commentary["commentary"]:
            msg += com['comm'].replace("<b>","").replace("</b>","").replace("<br/>","\n") + "\n"
        return msg
                    
        
    def score_card(self, match_id):
        match = self.cb.matchinfo(match_id)
        score = self.cb.scorecard(match_id)
        msg = f"<code>{match['team1']['name']} v/s {match['team2']['name']}-Scorecard</code>\n"
        for scr in reversed(score["scorecard"]):
            batcard = "".join([f"Name: {batcard['name']}\n Runs: {batcard['runs']}\n Balls: {batcard['balls']}\n Fours: {batcard['fours']}\n Six: {batcard['six']}\n Dismissal: {batcard['dismissal']}\n" for batcard in scr['batcard']])
            bowlcard = "".join([f"Name: {bowlcard['name']}\n Overs: {bowlcard['overs']}\n Maidens: {bowlcard['maidens']}\n Runs: {bowlcard['runs']}\n Six: {bowlcard['wickets']}\n Wides: {bowlcard['wides']}\n No Balls: {bowlcard['nballs']}\n" for bowlcard in scr['bowlcard']])
            msg += f"INN: {scr['inng_num']}\n" \
                   f" Batteam: {scr['batteam']}\n" \
                   f" {scr['runs']}/{scr['wickets']} in {scr['overs']} overs\n" \
                   f" Bowlteam: {scr['bowlteam']}\n" \
                   "\n\n"
        return msg
                   
    def players(self, match_id):
        match = self.cb.matchinfo(match_id)
        msg = f'Team 1: {match["team1"]["name"]}\n'
        msg += "Squad:\n " + " ".join([squad + "\n" for squad in match["team1"]["squad"]])
        msg += f'\n\nTeam 2: {match["team2"]["name"]}\n'
        msg += "Squad:\n " + " ".join([squad + "\n" for squad in match["team2"]["squad"]])
        return msg
            
            
                             
    def match_info(self, match_id):
        match = self.cb.matchinfo(match_id)
        msg = "*Series:* _" + match["srs"] + "_\n" \
              "*Match No:* _" + match["mnum"] + "_\n" \
              "*Type:* _" + match["type"] + "_\n" \
              "*State:* _" + match["mchstate"] + "_\n" \
              "*Status:* _" + match["status"] +"_\n" \
              "*Venue:* _" + match["venue_name"] + " " + match["venue_location"] + "_\n" \
              "*Toss:* _" + match["toss"] + "_\n" \
              "*Team 1:* _" + match["team1"]["name"] + "_\n" \
              "*Team 2:* _" + match["team2"]["name"] + "_\n" \
              f"*Officials:*\n _umpire 1: {match['official']['umpire1']['name']}\n umpire 2: {match['official']['umpire2']['name']}\n umpire 3: {match['official']['umpire3']['name']}\n referee: {match['official']['referee']['name']}_\n" \
              "*Start Time:* _" + match["start_time"] + "_\n" \
              "*Team 1:* _" + match["team1"]["name"] + "_\n" \
              "*Team 2:* _" +  match["team2"]["name"] + "_\n"              
        return msg
        
    def live_score(self, message, match_id):
        then = time.time()
        while self.run:
            elapsed = time.time() - then
            if elapsed > 10800:
                message.delete()
                break
            match_info = self.cb.matchinfo(match_id)
            live_score = self.cb.livescore(match_id)
            last_updated = datetime.utcnow() + timedelta(minutes=30, hours=5)
            batting, bowling = live_score["batting"], live_score["bowling"]
            msg = ''
            msg += match_info['srs'] + '\n' + match_info['status'] + '\n\n'
            msg += batting['team'] + "\n"
            for score in batting['score']:
                msg += f" INN: {score['inning_num']} {score['runs']}/{score['wickets']} in {score['overs']} overs\n"
                
            for bts in batting['batsman']:
                msg += f" {bts['name']} : {bts['runs']}({bts['balls']}) \n"
            
            msg += bowling['team'] + "\n"
            for score in bowling['score']:
                msg += f" INN: {score['inning_num']} {score['runs']}/{score['wickets']} in {score['overs']} overs\n"
                
            for balls in bowling['bowler']:
                msg += f" {balls['name'].strip('*')} : {balls['wickets']}/{balls['runs']} \n"
            msg += f"\n_Last updated: {last_updated.strftime('%I:%M:%S %P')} [IST]_"
            try:
                message.edit_text(
                   text = msg,
                   parse_mode="markdown",
                   reply_markup = InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text=f"Stop",callback_data=f"stop"),
                      InlineKeyboardButton(text=f"Force Refresh",callback_data=f"force_ref-{match_id}")
                     ]
                  ])
                )
            except:
                pass
            time.sleep(60)
            
        else:   
            self.run = True
            message.edit_text("Terminating...")
            time.sleep(2)
            message.delete()
            
    def list_matches_buttons(self, cb_data):        
        btns = []
        for match in self.all_matches:
            btns.append([InlineKeyboardButton(text=f" {match['team1']['name']} v/s {match['team2']['name']} ",callback_data=f"{cb_data}-{match['id']}")])
        btns.append([ InlineKeyboardButton(text=f"<<< Go back to home",callback_data=f"back_to_home")])
        return btns


cric = Cricket()        