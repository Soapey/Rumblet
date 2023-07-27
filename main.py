from rumblet.classes.db.SQLiteSchema import SQLiteSchema
from rumblet.classes.game.Game import Game


def main():
    SQLiteSchema.initialise()
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
