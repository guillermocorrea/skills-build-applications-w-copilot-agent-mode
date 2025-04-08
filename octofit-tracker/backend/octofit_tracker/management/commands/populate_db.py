import logging
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        try:
            # Connect to MongoDB
            logging.info('Connecting to MongoDB...')
            client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
            db = client[settings.DATABASES['default']['NAME']]

            # Drop existing collections
            logging.info('Dropping existing collections...')
            try:
                db.users.drop()
                logging.debug('Dropped users collection.')
                db.teams.drop()
                logging.debug('Dropped teams collection.')
                db.activity.drop()
                logging.debug('Dropped activity collection.')
                db.leaderboard.drop()
                logging.debug('Dropped leaderboard collection.')
                db.workouts.drop()
                logging.debug('Dropped workouts collection.')
            except Exception as e:
                logging.error(f'Error dropping collections: {e}')
                raise

            # Create users
            logging.info('Creating users...')
            try:
                users = [
                    User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
                    User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
                    User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
                    User(_id=ObjectId(), username='crashoverride', email='crashoverride@hmhigh.edu', password='crashoverridepassword'),
                    User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
                ]
                User.objects.bulk_create(users)
                logging.debug('Created users successfully.')
            except Exception as e:
                logging.error(f'Error creating users: {e}')
                raise

            # Create teams
            logging.info('Creating teams...')
            try:
                team = Team(_id=ObjectId(), name='Blue Team')
                team.save()
                logging.debug('Created team successfully.')
                for user in users:
                    team.members.add(user)
                    logging.debug(f'Added user {user.username} to team.')
            except Exception as e:
                logging.error(f'Error creating teams: {e}')
                raise

            # Create activities
            logging.info('Creating activities...')
            try:
                activities = [
                    Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
                    Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
                    Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
                    Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
                    Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
                ]
                Activity.objects.bulk_create(activities)
                logging.debug('Created activities successfully.')
            except Exception as e:
                logging.error(f'Error creating activities: {e}')
                raise

            # Create leaderboard entries
            logging.info('Creating leaderboard entries...')
            try:
                leaderboard_entries = [
                    Leaderboard(_id=ObjectId(), user=users[0], score=100),
                    Leaderboard(_id=ObjectId(), user=users[1], score=90),
                    Leaderboard(_id=ObjectId(), user=users[2], score=95),
                    Leaderboard(_id=ObjectId(), user=users[3], score=85),
                    Leaderboard(_id=ObjectId(), user=users[4], score=80),
                ]
                Leaderboard.objects.bulk_create(leaderboard_entries)
                logging.debug('Created leaderboard entries successfully.')
            except Exception as e:
                logging.error(f'Error creating leaderboard entries: {e}')
                raise

            # Create workouts
            logging.info('Creating workouts...')
            try:
                workouts = [
                    Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
                    Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
                    Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
                    Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
                    Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
                ]
                Workout.objects.bulk_create(workouts)
                logging.debug('Created workouts successfully.')
            except Exception as e:
                logging.error(f'Error creating workouts: {e}')
                raise

            logging.info('Successfully populated the database with test data.')
            self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
        except Exception as e:
            logging.error(f'Error occurred: {e}')
            raise
