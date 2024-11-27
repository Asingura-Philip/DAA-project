from datetime import datetime, timedelta
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt



# Task class definition
class Task:
    def __init__(self, name, task_type, deadline, priority, duration):
        self.name = name
        self.task_type = task_type  # "personal" or "academic"
        self.deadline = deadline  # datetime object
        self.priority = priority  # Integer priority level (lower number means higher priority)
        self.duration = duration  # Duration in minutes

    def __repr__(self):
        return f"{self.name} ({self.task_type}) - Priority: {self.priority}, Due: {self.deadline.strftime('%Y-%m-%d %H:%M')}, Duration: {self.duration} min"

# TaskManager class with scheduling, reminder, and retrieval methods
class TaskManager:
    def __init__(self):
        self.tasks = []  # Min-heap for priority-based task sorting
        self.schedule = []  # List of scheduled tasks
        self.reminders = []  # List of reminders for upcoming/missed tasks

    def add_task(self, task):
        print(f"Adding task: {task.name}")  # Debugging line to confirm task is added
        heappush(self.tasks, (task.priority, task.deadline, task))

    def get_upcoming_tasks(self):
        """Retrieve tasks sorted by deadline."""
        return [task for _, _, task in sorted(self.tasks, key=lambda x: x[1])]

    def track_reminders(self):
        """Tracks upcoming and missed tasks and generates reminders."""
        current_time = datetime.now()
        self.reminders = []
        
        for _, _, task in self.tasks:
            # Check if the task is overdue
            if task.deadline < current_time:
                self.reminders.append(f"Missed Task: {task.name} - Due: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
            elif task.deadline <= current_time + timedelta(minutes=30):
                # Remind if task is due within the next 30 minutes
                self.reminders.append(f"Upcoming Task: {task.name} - Due: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
        
        return self.reminders

    def schedule_tasks_dp(self):
        """Use dynamic programming to optimize task scheduling."""
        task_objects = [task[2] for task in self.tasks]
        task_objects.sort(key=lambda x: x.deadline)

        n = len(task_objects)
        dp = [0] * (n + 1)  # dp[i] stores the max number of tasks that can be scheduled up to the i-th task
        schedule = [None] * (n + 1)  # To track the scheduled tasks

        for i in range(1, n + 1):
            task = task_objects[i - 1]
            current_time = datetime.now()

            if current_time + timedelta(minutes=task.duration) <= task.deadline:
                max_prev_task = 0
                for j in range(i - 1, 0, -1):
                    prev_task = task_objects[j - 1]
                    if prev_task.deadline <= task.deadline - timedelta(minutes=task.duration):
                        max_prev_task = dp[j]
                        break

                dp[i] = max(dp[i - 1], max_prev_task + 1)
                if dp[i] > dp[i - 1]:
                    schedule[i] = task

        scheduled_tasks = []
        i = n
        while i > 0:
            if schedule[i] is not None:
                scheduled_tasks.append(schedule[i])
            i -= 1

        self.schedule = scheduled_tasks
        return self.schedule

    def sort_tasks_by_priority(self):
        """Sort tasks by priority (highest priority first)."""
        return sorted(self.tasks, key=lambda x: x[0])

    def search_task_by_name(self, task_name):
        """Search for a task by its name."""
        return [task for _, _, task in self.tasks if task.name.lower() == task_name.lower()]

# Function to analyze task density
def analyze_task_density(tasks, interval_minutes=60):
    """Analyze time intervals to see where task density is highest."""
    tasks = [task if isinstance(task, Task) else task[2] for task in tasks]

    if not tasks:
        print("No tasks available for density analysis.")
        return {}

    intervals = {}
    start_time = min(task.deadline for task in tasks)
    end_time = max(task.deadline for task in tasks)
    interval = timedelta(minutes=interval_minutes)
    
    while start_time <= end_time:
        count = sum(1 for task in tasks if start_time <= task.deadline < start_time + interval)
        intervals[start_time.strftime('%Y-%m-%d %H:%M')] = count
        start_time += interval
    
    return intervals

# Function to plot Gantt chart
# def plot_gantt_chart(tasks):
#     """Plots a Gantt chart for scheduled tasks."""
#     if not tasks:
#         print("No tasks to plot on the Gantt chart.")
#         return

#     fig, gnt = plt.subplots()
#     gnt.set_ylim(0, 50)
#     gnt.set_xlim(min(task.deadline for task in tasks), max(task.deadline for task in tasks) + timedelta(minutes=60))
#     gnt.set_yticks([15, 25])
#     gnt.set_yticklabels(['Academic', 'Personal'])
#     gnt.set_xlabel('Time')
#     gnt.set_title('Task Schedule Gantt Chart')
    
#     for task in tasks:
#         start = task.deadline - timedelta(minutes=task.duration)
#         gnt.broken_barh([(start, timedelta(minutes=task.duration))], (15 if task.task_type == "academic" else 25, 9),
#                         facecolors=('tab:blue' if task.task_type == "academic" else 'tab:orange'))
    
#     plt.show()


def plot_gantt_chart(tasks):
    """Plots a Gantt chart for scheduled tasks."""
    if not tasks:
        print("No tasks to plot on the Gantt chart.")
        return

    # Prepare data for plotting
    fig, gnt = plt.subplots()
    
    # Set the limits for x and y axis
    gnt.set_xlim(min(task.deadline - timedelta(minutes=task.duration) for task in tasks), 
                 max(task.deadline for task in tasks) + timedelta(minutes=60))
    
    # Set the y-axis limits and labels for different task types
    gnt.set_ylim(0, 50)
    gnt.set_yticks([15, 25])
    gnt.set_yticklabels(['Academic', 'Personal'])
    gnt.set_xlabel('Time')
    gnt.set_title('Task Schedule Gantt Chart')

    # Plot the tasks
    for task in tasks:
        start_time = task.deadline - timedelta(minutes=task.duration)
        duration = timedelta(minutes=task.duration)
        
        # Define color based on task type
        color = 'tab:blue' if task.task_type == "academic" else 'tab:orange'

        # Add a horizontal bar for each task
        gnt.broken_barh([(start_time, duration)], (15 if task.task_type == "academic" else 25, 9),
                        facecolors=color)

    # Show the plot
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




# Function to plot density Gantt chart
def plot_density_gantt_chart(density_analysis):
    """Plots a Gantt chart for task density intervals."""
    if not density_analysis:
        print("No density data to visualize.")
        return

    fig, gnt = plt.subplots()
    gnt.set_ylim(0, len(density_analysis) * 10)
    gnt.set_xlim(datetime.strptime(list(density_analysis.keys())[0], '%Y-%m-%d %H:%M'),
                 datetime.strptime(list(density_analysis.keys())[-1], '%Y-%m-%d %H:%M') + timedelta(minutes=60))
    gnt.set_xlabel('Time')
    gnt.set_title('Task Density Gantt Chart')

    interval_start_times = list(density_analysis.keys())
    for i, time_slot in enumerate(interval_start_times):
        count = density_analysis[time_slot]
        start = datetime.strptime(time_slot, '%Y-%m-%d %H:%M')
        gnt.broken_barh([(start, timedelta(minutes=60))], (i * 10, 8),
                        facecolors=('tab:green' if count > 0 else 'tab:gray'))

    gnt.set_yticks([i * 10 + 4 for i in range(len(interval_start_times))])
    gnt.set_yticklabels(interval_start_times)
    plt.show()

# Function to get user input for tasks
def get_user_input(manager):
    """Prompts user to input tasks."""
    print("Enter your tasks. Type 'done' when finished.")
    
    while True:
        name = input("Task name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break

        task_type = input("Task type (academic/personal): ").strip().lower()
        while task_type not in ['academic', 'personal']:
            task_type = input("Please enter a valid task type (academic/personal): ").strip().lower()

        while True:
            deadline_str = input("Deadline (YYYY-MM-DD HH:MM): ")
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                break
            except ValueError:
                print("Invalid format. Please enter the deadline in the format YYYY-MM-DD HH:MM")

        priority = int(input("Priority (1 for highest priority): "))
        duration = int(input("Duration in minutes: "))

        task = Task(name, task_type, deadline, priority, duration)
        manager.add_task(task)
        print(f"Task '{name}' added.\n")

# Main function to run the scheduling assistant
def main():
    """Runs the scheduling assistant."""
    manager = TaskManager()
    while True:
        print("\n--- Personal Scheduling Assistant ---")
        print("1. Add Task")
        print("2. View Upcoming Tasks")
        print("3. Schedule Tasks")
        print("4. Analyze Task Density")
        print("5. Track Reminders")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            get_user_input(manager)
        elif choice == '2':
            upcoming_tasks = manager.get_upcoming_tasks()
            if upcoming_tasks:
                for task in upcoming_tasks:
                    print(task)
            else:
                print("No upcoming tasks available.")
        elif choice == '3':
            scheduled_tasks = manager.schedule_tasks_dp()
            print("Scheduled Tasks:")
            for task in scheduled_tasks:
                print(task)
            plot_gantt_chart(scheduled_tasks)
        elif choice == '4':
            density_analysis = analyze_task_density(manager.tasks)
            print("Task Density Analysis:")
            for interval, count in density_analysis.items():
                print(f"{interval}: {count} tasks")
            plot_density_gantt_chart(density_analysis)
        elif choice == '5':
            reminders = manager.track_reminders()
            print("\nReminders:")
            for reminder in reminders:
                print(reminder)
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
