import json
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def fetch_post_by_id(post_id):
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)
            for post in posts:
                if post['id'] == post_id:
                    return post
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return None


@app.route('/')
def index():
    """display all blog posts. function (for instance/ index()) to render the index.html template."""
    # Here you would typically fetch blog posts from a database or a file.
    # For demonstration, we will use a static JSON file.
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    except json.JSONDecodeError:
        posts = []
    # Pass the posts to the template
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Formulardaten auslesen
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Datei einlesen
        try:
            with open('posts.json', 'r') as file:
                blog_posts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            blog_posts = []

        # ID generieren
        new_id = max([post["id"] for post in blog_posts], default=0) + 1

        # neuen Beitrag erstellen
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # Beitrag zur Liste hinzufügen
        blog_posts.append(new_post)

        # Liste zurück in JSON-Datei speichern
        with open('posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=2)

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    try:
        with open('posts.json', 'r') as file:
            blog_posts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        blog_posts = []

    # Filtere den Blogpost mit der passenden ID raus
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Speichere die neue Liste wieder zurück
    with open('posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=2)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    # Post finden
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Neue Werte aus dem Formular
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        # Überschreiben in der Liste
        for i, p in enumerate(posts):
            if p["id"] == post_id:
                posts[i] = post

        # Speichern
        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=2)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)