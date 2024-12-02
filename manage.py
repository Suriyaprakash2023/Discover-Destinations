from app import create_app, db

app = create_app()


if __name__ == '__main__':
    app.run(debug=True,port=8080)
    # app.run(port=8080) 