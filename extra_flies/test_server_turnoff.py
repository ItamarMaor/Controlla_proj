import subprocess

remote_computer_name = "127.0.0.1"
# remote_username = "USERNAME"  # If required for authentication
# remote_password = "PASSWORD"  # If required for authentication

shutdown_command = ["shutdown", "/s", "/m", f"\\\\{remote_computer_name}"]

# if remote_username and remote_password:
#     shutdown_command.extend(["/u", remote_username, "/p", remote_password])

subprocess.run(shutdown_command)
