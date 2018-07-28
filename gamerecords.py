from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Game
 
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



#FPS Category
category1 = Category(name = "First Person Shooter (FPS)")

session.add(category1)
session.commit()


game1 = Game(name = "Counter Strike Global Offensive", description = "Strategy FPS Game", price = "$2.99", category = category1)

session.add(game1)
session.commit()

game2 = Game(name = "Battlefield 1", description = "First World War FPS Game", price = "$5.50", category = category1)

session.add(game2)
session.commit()


#MOBA Category
category2 = Category(name = "MOBA")

session.add(category2)
session.commit()


game1 = Game(name = "DOTA", description = "Strategy Game", price = "$7.99", category = category2)

session.add(game1)
session.commit()


#2D Platform Category
category1 = Category(name = "2D Platform")

session.add(category1)
session.commit()


game1 = Game(name = "Hollow Knight", description = "2D platform game.", price = "", category = category1)

session.add(game1)
session.commit()

game2 = Game(name = "Cuphead", description = "2D platform game.", price = "", category = category1)

session.add(game2)
session.commit()

print "Games added!"

