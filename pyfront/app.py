from application import createApp

app = createApp()

if __name__ == "__main__":  # хм это же мейн
    app.run(host="0.0.0.0", debug=True)
