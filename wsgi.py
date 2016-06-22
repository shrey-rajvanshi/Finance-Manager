from fmapp import app as application

if __name__ == "__main__":
    application.secret_key = 'super secret keyjkhogh08923epuoij'
    application.run(debug=True,host='0.0.0.0')
