from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

# When python runs a program directly, the module name
# is __main__
if __name__ == "__main__":
    app.run(debug=True)
