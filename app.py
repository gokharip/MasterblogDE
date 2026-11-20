"""Flask blog app that stores posts in a JSON file."""
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = "blog_posts.json"


@app.route('/')
def index():
    """Show all blog posts."""
    return render_template('index.html', posts=load_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Show the add form (GET) and save the new post (POST)."""
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not author or not title or not content:
            return render_template('add.html', error='Please fill in all fields.'), 400

        posts = load_posts()
        posts.append({
            'id': max((post['id'] for post in posts), default=0) + 1,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0,
        })
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete the post with the given id."""
    posts = load_posts()
    found_post = fetch_post_by_id(post_id, posts)
    if found_post is None:
        return "Post not found", 404

    posts.remove(found_post)
    save_posts(posts)
    return redirect(url_for("index"))


@app.route('/like/<int:post_id>')
def like(post_id):
    """Add a like for the post with the given id."""
    posts = load_posts()
    found_post = fetch_post_by_id(post_id, posts)
    if found_post is None:
        return "Post not found", 404

    found_post['likes'] += 1
    save_posts(posts)
    return redirect(url_for("index"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Show the edit form (GET) or save the changes to a post (POST)."""
    posts = load_posts()
    found_post = fetch_post_by_id(post_id, posts)
    if found_post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not author or not title or not content:
            return render_template(
                'update.html',
                post=found_post,
                error='Please fill in all fields.'), 400
        found_post['author'] = author
        found_post['title'] = title
        found_post['content'] = content
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=found_post)


def fetch_post_by_id(post_id, posts):
    """Return the post with the given ID, or None if it does not exist."""
    return next((post for post in posts if post["id"] == post_id), None)


def load_posts():
    """Load all posts from DATA_FILE; return an empty list if the file does not exist."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save posts to JSON file (DATA_FILE)."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
