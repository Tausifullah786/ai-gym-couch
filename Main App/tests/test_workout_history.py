import importlib
import os
import tempfile
import unittest


class WorkoutHistoryPersistenceTest(unittest.TestCase):
    def test_save_workout_summary_persists_history_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["AI_GYM_COACH_DB_PATH"] = os.path.join(tmpdir, "test_data.db")

            import services.persistence.exercise_repository as repo
            repo = importlib.reload(repo)

            repo.init_db()
            user = repo.get_or_create_user("history-test")

            repo.save_workout_summary(user["id"], "Squats", 12, 2, 55)
            rows = repo.get_users_exercises(user["id"])

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["exercise_name"], "Squats")
            self.assertEqual(rows[0]["reps"], 12)
            self.assertEqual(rows[0]["sets"], 2)
            self.assertEqual(rows[0]["time"], 55)


if __name__ == "__main__":
    unittest.main()
