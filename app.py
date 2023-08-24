import argparse
from app import app
from db.init_db import init_db

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app and perform database operations.')
    parser.add_argument('--run', action='store_true', help='Run the Flask app')
    parser.add_argument('--migrate', action='store_true', help='Perform database migration')

    args = parser.parse_args()

    if args.migrate:
        init_db()
        print('Database migration completed.')

    if args.run:
        app.run(debug=True)
