
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, PasswordField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate



import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    semestre = db.Column(db.String(20))

    def __repr__(self):
        return f'<Disciplina {self.nome} - {self.semestre}>'



class DisciplinaForm(FlaskForm):
    nome = StringField('Nome da disciplina:', validators=[DataRequired()])
    semestre = RadioField(
        'Semestre:',
        choices=[
            ("1º semestre", "1º semestre"),
            ("2º semestre", "2º semestre"),
            ("3º semestre", "3º semestre"),
            ("4º semestre", "4º semestre"),
            ("5º semestre", "5º semestre"),
            ("6º semestre", "6º semestre"),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Cadastrar')



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Disciplina=Disciplina)


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/professores')
def professores():
    return render_template('professores.html', current_time=datetime.utcnow())

@app.route('/alunos')
def alunos():
    return render_template('alunos.html', current_time=datetime.utcnow())

@app.route('/cursos')
def cursos():
    return render_template('cursos.html', current_time=datetime.utcnow())

@app.route('/ocorrencias')
def ocorrencias():
    return render_template('ocorrencias.html', current_time=datetime.utcnow())


# rota prova
@app.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    form = DisciplinaForm()

    if form.validate_on_submit():
        disc = Disciplina.query.filter_by(nome=form.nome.data).first()

        if disc is None:
            disc = Disciplina(
                nome=form.nome.data,
                semestre=form.semestre.data
            )
            db.session.add(disc)
            db.session.commit()
            flash("Disciplina cadastrada com sucesso!", "success")
        else:
            flash("Essa disciplina já existe.", "warning")

        return redirect(url_for('disciplinas'))

    lista = Disciplina.query.order_by(Disciplina.semestre, Disciplina.nome).all()

    return render_template('disciplinas.html', form=form, disciplinas=lista)


if __name__ == "__main__":
    app.run(debug=True)