from app import app

# When python runs a program directly, the module name
# is __main__
if __name__ == '__main__':
    app.run(debug=True)
