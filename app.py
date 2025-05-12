from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_commented = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    author = db.relationship('User', backref=db.backref('comments', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <meta charset="UTF-8">
        <title>Educație pentru Viitor</title>
    </head>
    <body>
        <header>
            <h1>🎓 Educație pentru Viitor</h1>
            <nav>
                <a href="{{ url_for('index') }}">Acasă</a>
                {% if current_user.is_authenticated %}
                    <a href="{{ url_for('create_post') }}">Scrie un articol</a>
                    <a href="{{ url_for('logout') }}">Logout</a>
                {% else %}
                    <a href="{{ url_for('login') }}">Login</a>
                    <a href="{{ url_for('register') }}">Înregistrare</a>
                {% endif %}
            </nav>
        </header>
        <main>
            <section>
                <h2>📊 Evoluția promovabilității la Evaluarea Națională și Bacalaureat (1980 - 2020)</h2>
                <p><strong>1980:</strong> Promovabilitatea la clasa a VIII-a era de aproximativ <strong>92%</strong>, iar la Bacalaureat în jur de <strong>87%</strong>. Învățământul era structurat rigid, cu accent pe memorare și performanță în științele exacte.</p>
                <p><strong>2000:</strong> Promovabilitatea la Evaluarea Națională (în formatul nou) era în jur de <strong>75%</strong>, iar la Bacalaureat <strong>80%</strong>. Reforma curriculară introdusă în anii '90 a adus schimbări în evaluare, introducând competențele cheie și testarea standardizată.</p>
                <p><strong>2020:</strong> Promovabilitatea la Evaluarea Națională a fost de <strong>76.1%</strong>, iar la Bacalaureat de <strong>64.5%</strong> (cu variații în funcție de pandemie și zonă). Sistemul educațional a început să pună accent pe competențe digitale, gândire critică și evaluări online, dar cu probleme de echitate și acces.</p>
                <h3>📘 Programele Ministerului Educației</h3>
                <ul>
                    <li><strong>1980:</strong> Programa națională era centralizată, cu accent pe ideologie, matematică și științe. Nu existau alternative curriculare.</li>
                    <li><strong>2000:</strong> A apărut trunchiul comun + curriculum la decizia școlii (CDS), se introduc competențele cheie.</li>
                    <li><strong>2020:</strong> Se revizuiesc programele pe baza competențelor europene, apar platformele digitale și testarea standardizată online (pilot).</li>
                </ul>
                <p>🔍 <em>Analiza arată o scădere a promovabilității în paralel cu diversificarea curriculei și schimbările sociale. Necesitatea reformei reale în educație devine evidentă.</em></p>
            </section>
        </main>
        <footer>
            <p>&copy; {{ current_year }} Educație pentru Viitor</p>
        </footer>
    </body>
    </html>
    <h2>📉 Situația economică și impactul asupra educației</h2>
<p><strong>1980:</strong> Deși sistemul era gratuit, multe familii din mediul rural nu își permiteau să susțină copiii în orașe (transport, rechizite, cazare). Criza alimentară și raționalizarea afectau nivelul de trai și concentrarea elevilor.</p>
<p><strong>2000:</strong> Tranziția post-comunistă a dus la șomaj, inflație ridicată și migrația părinților în străinătate. Abandonul școlar a crescut în zonele defavorizate. Programele de sprijin (ex: „Bani de liceu”) nu acopereau nevoile reale.</p>
<p><strong>2020:</strong> Pandemia a accentuat decalajele. Mulți elevi nu aveau acces la internet sau dispozitive pentru școala online. Sărăcia extremă, mai ales în rural, a forțat elevii să muncească sau să abandoneze școala.</p>
<p>🔗 <em>Educația și economia sunt profund interconectate: lipsa resurselor reduce șansele la educație de calitate, iar educația slabă perpetuează sărăcia. Un cerc vicios care trebuie întrerupt prin politici sociale eficiente.</em></p>    
<h2>🎒 Educația vs. Nevoia de a munci – realitatea tinerilor români</h2>
<p>În ultimele decenii, mii de tineri au fost nevoiți să renunțe la studii pentru a munci, fie în țară, fie în străinătate, pentru a-și sprijini familia sau a supraviețui economic.</p>

<ul>
  <li><strong>1980:</strong> Aproximativ <strong>10-15%</strong> dintre elevii de liceu din mediul rural nu își continuau studiile din cauza muncii în gospodărie sau agricultură.</li>
  <li><strong>2000:</strong> Peste <strong>25%</strong> dintre tineri între 16 și 19 ani au intrat pe piața muncii imediat după gimnaziu, conform INS. Migrația economică a început să ia amploare.</li>
  <li><strong>2020:</strong> În jur de <strong>35%</strong> dintre tinerii între 18 și 24 de ani riscau să nu aibă niciun fel de formare sau job stabil ("NEET" - Not in Employment, Education or Training). Mulți au plecat în străinătate pentru muncă sezonieră sau necalificată.</li>
</ul>

<p>📌 <em>Deși unii dintre acești tineri au avut rezultate bune la învățătură, realitatea economică i-a forțat să renunțe la visuri și să aleagă supraviețuirea.</em></p> 
                                  <h2>🌍 Comparație educațională România vs. alte state europene</h2>
<p>În ciuda eforturilor de reformă, România a rămas în urmă față de media UE în mai mulți indicatori cheie ai sistemului educațional.</p>

<table border="1" cellpadding="10">
  <tr>
    <th>Indicator</th>
    <th>România (2020)</th>
    <th>Media UE (2020)</th>
    <th>Țări de referință (Germania / Franța / Polonia)</th>
  </tr>
  <tr>
    <td>📉 Rata de abandon școlar timpuriu (16–24 ani)</td>
    <td><strong>15.3%</strong></td>
    <td><strong>9.9%</strong></td>
    <td>🇩🇪 10.1% / 🇫🇷 8.0% / 🇵🇱 5.4%</td>
  </tr>
  <tr>
    <td>🎓 Procent tineri cu studii superioare (25–34 ani)</td>
    <td><strong>25%</strong></td>
    <td><strong>41%</strong></td>
    <td>🇩🇪 35% / 🇫🇷 46% / 🇵🇱 40%</td>
  </tr>
  <tr>
    <td>📚 Investiție în educație (% din PIB)</td>
    <td><strong>3.2%</strong></td>
    <td><strong>4.7%</strong></td>
    <td>🇩🇪 5.0% / 🇫🇷 5.2% / 🇵🇱 4.6%</td>
  </tr>
  <tr>
    <td>👨‍🏫 Număr elevi/profesor (gimnaziu)</td>
    <td><strong>17.4</strong></td>
    <td><strong>12.8</strong></td>
    <td>🇩🇪 13.5 / 🇫🇷 12.0 / 🇵🇱 10.8</td>
  </tr>
</table>
<h2>🚌 Transportul elevilor – o criză ignorată</h2>
<p>În multe localități din România, elevii sunt nevoiți să parcurgă zilnic kilometri întregi pentru a ajunge la școală. Lipsa transportului gratuit, condițiile insalubre ale mijloacelor existente sau orarul incoerent duc la:</p>
<ul>
  <li>❌ <strong>Abandon școlar</strong> – copiii din sate izolate renunță la școală din cauza imposibilității de a face naveta zilnic.</li>
  <li>⏱️ <strong>Oboseală cronică</strong> – naveta de 2–3 ore zilnic scade randamentul școlar și afectează sănătatea elevilor.</li>
  <li>🚫 <strong>Lipsă de siguranță</strong> – transportul ilegal sau improvizat pune în pericol viața elevilor.</li>
  <li>📉 <strong>Dezavantaj pentru profesorii navetiști</strong> – mulți profesori refuză posturi în zone izolate din cauza cheltuielilor și a lipsei infrastructurii.</li>
</ul>
<p><em>Un sistem educațional nu poate funcționa dacă elevul nu poate ajunge fizic la școală.</em></p>

<h3>📌 Soluții propuse:</h3>
<ul>
  <li>✅ Autobuze școlare dedicate – operate de primării sau consilii județene cu fonduri europene și guvernamentale.</li>
  <li>✅ Subvenționarea transportului public local pentru elevi și profesori navetiști.</li>
  <li>✅ Crearea unui orar sincronizat cu programul școlar.</li>
  <li>✅ Aplicații digitale pentru gestionarea traseelor și monitorizarea prezenței.</li>
</ul>

<p><strong>📣 Mesaj pentru decidenți:</strong> Dacă vrem o Românie educată, trebuie să începem prin a aduce elevii la școală în siguranță, zi de zi.</p>

<p>📌 <em>România are una dintre cele mai scăzute investiții în educație din UE și cea mai mare rată de abandon școlar. Deși progresul este vizibil în unele zone, decalajele persistă.</em></p> 
<h2>🛠️ Soluții în lucru pentru combaterea abandonului școlar</h2>
<ul>
  <li>✅ <strong>Programul Național „Masa caldă”</strong> – implementat în peste 1.300 de școli, oferă o masă caldă pe zi elevilor din zone defavorizate.</li>
  <li>✅ <strong>Programul „Școala după Școală”</strong> – sprijin educațional gratuit după ore, pentru copiii care nu primesc ajutor acasă.</li>
  <li>✅ <strong>Vouchere educaționale</strong> – tichete pentru rechizite și haine oferite familiilor cu venituri mici.</li>
  <li>✅ <strong>Creșterea numărului de consilieri școlari</strong> – pentru sprijin psihologic și identificarea timpurie a riscurilor de abandon.</li>
  <li>✅ <strong>Digitalizare parțială</strong> – tablete, internet și platforme educaționale oferite elevilor din medii rurale.</li>
</ul>
  <h1>🚍 Transportul Educațional în România: Deficiențe Critice</h1>

  <h2>Situația actuală vs. Nevoi reale (2024–2025)</h2>
  <table>
    <thead>
      <tr>
        <th>Indicator</th>
        <th>Valoare Actuală</th>
        <th>Necesar Minim</th>
        <th>Deficit</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Elevi navetiști</td>
        <td>~400.000</td>
        <td>–</td>
        <td>–</td>
      </tr>
      <tr>
        <td>Autobuze școlare funcționale</td>
        <td>~4.100</td>
        <td>≥12.000</td>
        <td><strong>~7.900 lipsă</strong></td>
      </tr>
      <tr>
        <td>Localități fără transport școlar</td>
        <td>~2.000</td>
        <td>0</td>
        <td><strong>100% deficit</strong></td>
      </tr>
      <tr>
        <td>Buget anual alocat</td>
        <td>~300 mil. lei</td>
        <td>≥900 mil. lei</td>
        <td><strong>~600 mil. lei lipsă/an</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="highlight">
    <strong>Ce înseamnă „parametri normali”:</strong>
    <ul>
      <li>Microbuz în fiecare zonă rurală sau izolat urban</li>
      <li>Program adaptat orelor de curs</li>
      <li>Gratuitate totală pentru elevi, decont integral pentru profesori</li>
      <li>Vehicule sigure, curate, monitorizate GPS</li>
    </ul>
  </div>

  <h2>Consecințe ale subfinanțării</h2>
  <ul>
    <li>Aproximativ 35.000 de elevi abandonează anual școala</li>
    <li>1 din 3 profesori refuză posturi în mediul rural</li>
    <li>Crestere a infracționalității și a analfabetismului funcțional</li>
  </ul>
<h2>🔮 Planuri viitoare (2025–2030)</h2>
<ul>
  <li>📌 <strong>Extinderea programului „Masa caldă” la nivel național</strong> – țintă: 3.000+ școli până în 2027.</li>
  <li>📌 <strong>Modernizarea infrastructurii școlare</strong> – reabilitarea a 2.500 școli și dotare cu laboratoare funcționale.</li>
  <li>📌 <strong>Formarea și stabilizarea profesorilor în zonele defavorizate</strong> – prin salarii motivate și locuințe de serviciu.</li>
  <li>📌 <strong>Înființarea centrelor educaționale rurale</strong> – sprijin comunitar integrat: educație + consiliere + formare profesională.</li>
  <li>📌 <strong>Legea „zero taxe ascunse” în școli</strong> – eliminarea costurilor neoficiale care descurajează părinții să-și trimită copiii la școală.</li>
</ul>

<h3>🎯 Obiectiv național până în 2030:</h3>
<ul>
  <li>🔽 <strong>Reducerea abandonului școlar sub 9%</strong> (de la 15.3% în prezent)</li>
  <li>🎓 <strong>Cresterea promovabilității Bacalaureatului la peste 80%</strong></li>
  <li>🌍 <strong>Reducerea decalajului rural-urban în educație cu 50%</strong></li>
</ul>

<p><em>Toate aceste măsuri fac parte din Planul Național de Redresare și Reziliență (PNRR) – Componenta Educație și din Strategia națională pentru reducerea abandonului școlar 2022–2030.</em></p>                                                           
    """, current_year=datetime.now().year)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed.', 'danger')
    return render_template_string("""
    <h2>Login</h2>
    <form method="POST">
        <label>Email:</label><input type="email" name="email" required><br>
        <label>Password:</label><input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="{{ url_for('register') }}">Nu ai cont? Înregistrează-te aici.</a></p>
    """)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created!', 'success')
        return redirect(url_for('index'))
    return render_template_string("""
    <h2>Înregistrare</h2>
    <form method="POST">
        <label>Username:</label><input type="text" name="username" required><br>
        <label>Email:</label><input type="email" name="email" required><br>
        <label>Password:</label><input type="password" name="password" required><br>
        <button type="submit">Înregistrare</button>
    </form>
    <p><a href="{{ url_for('login') }}">Ai deja cont? Autentifică-te.</a></p>
    """)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ai fost delogat.', 'info')
    return redirect(url_for('index'))


@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return f"<h2>{post.title}</h2><p>{post.content}</p>"


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Postare creată!", "success")
        return redirect(url_for('index'))
    return render_template_string("""
    <h2>Scrie un articol</h2>
    <form method="POST">
        <label>Titlu:</label><input type="text" name="title" required><br>
        <label>Conținut:</label><textarea name="content" required></textarea><br>
        <button type="submit">Publică</button>
    </form>
    """)


# Initialize DB
with app.app_context():
    db.create_all()
    print("Database and tables created.")


if __name__ == '__main__':
    app.run(debug=True)
