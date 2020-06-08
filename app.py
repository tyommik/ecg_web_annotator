from app import create_app

if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 5000
    app = create_app()
    app.run(host=IP, port=PORT, debug=True, use_reloader=False)