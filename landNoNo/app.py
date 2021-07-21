from flask import render_template, request, redirect, session
import model as vo

@app.route('/')
def root():
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
