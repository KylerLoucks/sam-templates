from flask import Flask, render_template
from conncheck import postgres, mysql, redis, mongodb

app = Flask(__name__)


@app.route("/")
def status():
    _status = lambda b: "Running" if b else "Stopped"

    status_data = [
        {
            "name": "Postgres",
            "status": _status(postgres.is_postgres_accessible()),
        },
        {
            "name": "MySQL",
            "status": _status(mysql.is_mysql_accessible()),
        },
        {
            "name": "Redis",
            "status": _status(redis.is_redis_accessible()),
        },
        {
            "name": "MongoDB",
            "status": _status(mongodb.is_mongodb_accessible()),
        },
    ]
    

    return render_template("status.html", results=status_data)


if __name__ == "__main__":
    app.run(debug=True)
