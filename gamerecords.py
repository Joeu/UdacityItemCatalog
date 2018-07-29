from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Game, User
 
engine = create_engine('sqlite:///gamecategory.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Initial User
user1 = User(name = "Padre Quevedo", email = "pdrqvd@email.com", picture = "")

session.add(user1)
session.commit()


#FPS Category
category1 = Category(name = "First Person Shooter (FPS)", user_id = 1)

session.add(category1)
session.commit()


game1 = Game(name = "Counter Strike Global Offensive", description = "Counter-Strike (CS) is a series of multiplayer first-person shooter video games, in which teams of terrorists battle to perpetrate an act of terror (bombing, hostage-taking) and counter-terrorists try to prevent it (bomb defusal, hostage rescue).", category = category1, user_id = 1)

session.add(game1)
session.commit()

game2 = Game(name = "Battlefield 1", description = "Battlefield is a series of first-person shooter video games that started out on Microsoft Windows and OS X with Battlefield 1942, which was released in 2002. The series is developed by Swedish company EA DICE and is published by American company Electronic Arts.", category = category1, user_id = 1)

session.add(game2)
session.commit()


#MOBA Category
category2 = Category(name = "MOBA", user_id = 1)

session.add(category2)
session.commit()


game1 = Game(name = "DOTA", description = "Defense of the Ancients (DotA) is a multiplayer online battle arena (MOBA) mod for the video game Warcraft III: Reign of Chaos and its expansion, Warcraft III: The Frozen Throne.", category = category2, user_id = 1)

session.add(game1)
session.commit()


#2D Platform Category
category3 = Category(name = "2D Platform", user_id = 1)

session.add(category3)
session.commit()


game1 = Game(name = "Hollow Knight", description = "Hollow Knight is a Metroidvania video game developed and published by Australian studio Team Cherry.", category = category3, user_id = 1)

session.add(game1)
session.commit()

game2 = Game(name = "Cuphead", description = "Cuphead is a run and gun indie video game developed and published by StudioMDHR.", category = category3, user_id = 1)

session.add(game2)
session.commit()

print "Games added!"

