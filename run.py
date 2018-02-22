from app.app import create_app

app = create_app(queue_size=3)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, ssl_context=('certificate/cert.pem', 'certificate/key.pem'))
