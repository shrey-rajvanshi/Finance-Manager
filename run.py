from fmapp import app

if __name__ == '__main__':
    app.secret_key = 'super secret keyjkhogh08923epuoij'
    app.run(debug=True, host='0.0.0.0')
