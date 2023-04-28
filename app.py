from App import app,db 

if __name__ == "__main__":
    app.run(debug=True,host='172.17.0.1', port=8000, threaded=True)