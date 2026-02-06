from database import Base, engine

print("Creating tables in the database...")

Base.metadata.create_all(bind=engine)
print("Tables successfully created!")