from django.core.management.base import BaseCommand
import sched
import time
from myapp.models import BookedEvent
class Command(BaseCommand):
    help = 'Runs a command every 5 minutes to delete unpaid events'

    def handle(self, *args, **options):
        # Create a scheduler
        s = sched.scheduler(time.time, time.sleep)

    
        def run_command():
            filtered_objects = BookedEvent.objects.filter(status='created')  

            if filtered_objects.exists():
                for obj in filtered_objects:
                    print(obj)
                    obj.delete()
                    print("deleted")
            else:
                print("No objects found to delete.")

            s.enter(300, 1, run_command)

        # Schedule the initial execution
        s.enter(0, 1, run_command)

        # Start the scheduler
        s.run()
