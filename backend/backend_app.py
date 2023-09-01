from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
def sort_f(my_list, field, direction):
    sorted_list = sorted(my_list, key=lambda x: x[field], reverse=direction)
    return sorted_list


@app.route('/api/posts', methods=['GET'])
def get_posts():
    global POSTS
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort and direction:
        if direction == 'desc':
            order = True
        else:
            order = False
        POSTS = sort_f(POSTS, sort, order)
        return jsonify(POSTS)
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    global POSTS
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if title is not None and content is not None:
        new_id = max(POSTS, key=lambda item: item['id'])['id'] + 1
        new_post = {
            'id': new_id,
            'title': title,
            'content': content
        }
        POSTS.append(new_post)
        return jsonify({'message': 'Post added successfully'}), 201
    return jsonify({'message': 'Incorrect data'}), 400


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def del_post(id):
    global POSTS
    if any(int(post.get('id')) == id for post in POSTS):
        new_data = [item for item in POSTS if int(item['id']) != id]
        POSTS = new_data
        return jsonify({'message': 'Post deleted successfully'}), 201
    return jsonify({'message': 'Post with this id not found'}), 400


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    global POSTS

    request_data = request.json  # Get the JSON data from the request body
    title = request_data.get('title')
    content = request_data.get('content')

    # Find the index of the post with the given ID
    post_index = next((index for index, post in enumerate(POSTS) if int(post['id']) == id), None)

    if post_index is not None:
        if title is not None and content is not None:
            POSTS[post_index]['title'] = title
            POSTS[post_index]['content'] = content
            return jsonify({'message': 'Post was successfully updated'}), 200
        return jsonify({'message': 'Incorrect data'}), 400
    return jsonify({'message': 'Post with this ID not found'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    title = request.args.get('title')
    content = request.args.get('content')
    search_result = []
    if title or content:
        for post in POSTS:
            if title is not None:
                if title.lower() in post['title'].lower():
                    search_result.append(post)
                elif content is not None:
                    if content.lower() in post['content'].lower():
                        search_result.append(post)
            elif content is not None:
                if content.lower() in post['content'].lower():
                    search_result.append(post)
        if search_result:
            return jsonify(search_result), 200
        else:
            return jsonify({'message': 'No matching posts found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
