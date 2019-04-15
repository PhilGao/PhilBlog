from flask import Flask,render_template,redirect

app = Flask(__name__)



@app.route('/',methods=['GET'])
@app.route('/index',methods=['GET'])
def index():
    return render_template('index.html',title='Say it again',pubdate = '2019-04-15',diagram=r'res/image/today.png')

@app.route('/tag',methods=['GET'])
def tag():
    return redirect('index')

@app.route('/about',methods=['GET'])
def about():
    return redirect('index')


@app.route('/archive',methods=['GET'])
def archive():
    return redirect('index')

@app.route('/blog',methods=['GET'])
def blog():
    return render_template('blog.html')