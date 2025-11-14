"""
Basic REST API using Flask

Run with: python -m api_development.basic_api
Access at: http://localhost:5000
"""
from flask import Flask, jsonify, request
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

app = Flask(__name__)


@dataclass
class Task:
    """Task model."""
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


# In-memory storage
tasks: Dict[int, Task] = {}
task_id_counter = 1


@app.route('/')
def home():
    """API home endpoint."""
    return jsonify({
        'message': 'Task Management API',
        'version': '1.0',
        'endpoints': {
            'GET /tasks': 'List all tasks',
            'GET /tasks/<id>': 'Get a specific task',
            'POST /tasks': 'Create a new task',
            'PUT /tasks/<id>': 'Update a task',
            'DELETE /tasks/<id>': 'Delete a task',
        }
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks.

    Query params:
        completed: Filter by completion status (true/false)

    Returns:
        JSON list of tasks
    """
    completed_filter = request.args.get('completed')

    task_list = list(tasks.values())

    if completed_filter is not None:
        is_completed = completed_filter.lower() == 'true'
        task_list = [t for t in task_list if t.completed == is_completed]

    return jsonify({
        'tasks': [asdict(task) for task in task_list],
        'count': len(task_list)
    })


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int):
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID

    Returns:
        JSON task object or 404
    """
    task = tasks.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify(asdict(task))


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task.

    Request body:
        {
            "title": "Task title",
            "description": "Task description"
        }

    Returns:
        JSON created task object
    """
    global task_id_counter

    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(
        id=task_id_counter,
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )

    tasks[task_id_counter] = task
    task_id_counter += 1

    return jsonify(asdict(task)), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """
    Update an existing task.

    Args:
        task_id: Task ID

    Request body:
        {
            "title": "Updated title",
            "description": "Updated description",
            "completed": true
        }

    Returns:
        JSON updated task object or 404
    """
    task = tasks.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']

    return jsonify(asdict(task))


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """
    Delete a task.

    Args:
        task_id: Task ID

    Returns:
        JSON success message or 404
    """
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404

    del tasks[task_id]

    return jsonify({'message': 'Task deleted successfully'})


@app.route('/tasks/stats', methods=['GET'])
def get_stats():
    """
    Get task statistics.

    Returns:
        JSON statistics object
    """
    total = len(tasks)
    completed = sum(1 for task in tasks.values() if task.completed)
    pending = total - completed

    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': (completed / total * 100) if total > 0 else 0
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Add some sample data
    tasks[1] = Task(1, "Learn Python", "Study Python fundamentals", False)
    tasks[2] = Task(2, "Build API", "Create REST API with Flask", True)
    task_id_counter = 3

    app.run(debug=True, port=5000)
