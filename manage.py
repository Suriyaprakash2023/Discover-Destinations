from app import create_app, db

app = create_app()


if __name__ == '__main__':
    app.run(debug=True,port=8989)
    # app.run(port=8080) 