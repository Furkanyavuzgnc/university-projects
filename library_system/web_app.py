from flask import Flask, request, render_template_string
from library_system import Library, Book

app = Flask(__name__)
library = Library()

HTML = """
<!doctype html>
<title>Kütüphane Yönetim Sistemi</title>

<h2>Kütüphane Yönetim Sistemi (Flask)</h2>

<hr>

<h3>📘 Kitap Ekle</h3>
<form method="post" action="/add">
    <input name="name" placeholder="Kitap Adı" required>
    <input name="author" placeholder="Yazar" required>
    <input name="year" placeholder="Yıl" required>
    <button type="submit">Ekle</button>
</form>

<hr>

<h3>❌ Kitap Sil</h3>
<form method="post" action="/remove">
    <input name="name" placeholder="Silinecek Kitap Adı" required>
    <button type="submit">Sil</button>
</form>

<hr>

<h3>🔍 İsme Göre Ara</h3>
<form method="get" action="/search/name">
    <input name="q" placeholder="Kitap adı">
    <button type="submit">Ara</button>
</form>

<h3>🔍 Yazara Göre Ara</h3>
<form method="get" action="/search/author">
    <input name="q" placeholder="Yazar adı">
    <button type="submit">Ara</button>
</form>

<hr>

<h3>📚 Tüm Kitaplar</h3>
<ul>
{% for book in books %}
    <li>{{ book }}</li>
{% else %}
    <li>Kütüphanede kitap yok.</li>
{% endfor %}
</ul>

<hr>
<p><b>{{ message }}</b></p>
"""

@app.route("/")
def index():
    return render_template_string(
        HTML,
        books=library.list_books(),
        message=""
    )

@app.route("/add", methods=["POST"])
def add_book():
    name = request.form["name"]
    author = request.form["author"]
    year = request.form["year"]

    if not year.isdigit():
        msg = "Yayın yılı sayı olmalıdır."
    else:
        book = Book(name, author, int(year))
        msg = library.add_book(book)

    return render_template_string(
        HTML,
        books=library.list_books(),
        message=msg
    )

@app.route("/remove", methods=["POST"])
def remove_book():
    name = request.form["name"]
    msg = library.remove_book(name)

    return render_template_string(
        HTML,
        books=library.list_books(),
        message=msg
    )

@app.route("/search/name")
def search_by_name():
    q = request.args.get("q", "")
    results = library.search_by_name(q)

    return render_template_string(
        HTML,
        books=results,
        message=f"'{q}' için arama sonucu"
    )

@app.route("/search/author")
def search_by_author():
    q = request.args.get("q", "")
    results = library.search_by_author(q)

    return render_template_string(
        HTML,
        books=results,
        message=f"'{q}' yazarı için arama sonucu"
    )


if __name__ == "__main__":
    app.run(debug=True)
