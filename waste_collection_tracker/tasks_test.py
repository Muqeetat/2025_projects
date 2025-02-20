# import requests


# print("Root path:")
# print(requests.get("http://127.0.0.1:8000/").json())
# print()



# print("Fetching all tasks:")
# print(requests.get("http://127.0.0.1:8000/tasks").json())
# print()



# print("Fetching a task using ID:")
# print(requests.get("http://127.0.0.1:8000/tasks/42").json())
# print()


# print("Adding a Task:")
# response = requests.post(
#     "http://127.0.0.1:8000/tasks",  
#     json={
#         "title": "Washing Rice",
#         "description": "Cooking Rice",
#         "category": "Chores",
#         "status": "in-progress",
#         "due_date": "2025-02-20 12:00:00"
#     },
# )
# print(response.json())



# print("Updating an item:")
# response = requests.put(
#     "http://127.0.0.1:8000/tasks/42",
#     json={
#         "title": "Learning Japanese",
#         "description": "Language"
# 		}
# )
# print(response.json())
# print()

 

# print("Deleting an item:")
# response = requests.delete("http://127.0.0.1:8000/tasks/42")
# if response.status_code == 204:  # No Content
#     print("Task deleted successfully.")
# else:
#     print(response.json())


