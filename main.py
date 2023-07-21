from rumblet.classes.db.SQLiteConnector import initialise_db
from rumblet.classes.game.Game import Game




def main():
    initialise_db()
    game = Game()
    game.run()



if __name__ == '__main__':
    main()
