import os
import csv
import json

my_path = "package/messages"
chat_files = []
counter = 0
for path, subdirs, files in os.walk(my_path):
    for name in files:
        if "channel.json" in name:
            chat_files.append([]) # [[]]
            chat_files[counter].append(os.path.join(path, name)) # [["package/messages/123456789/channel.json"]]
        if "messages.csv" in name:
            chat_files[counter].append(os.path.join(path, name)) # [["package/messages/123456789/channel.json", "package/123456789/messages.csv"]]
            counter += 1


print("\n" + "Chat files loaded: " + str(len(chat_files)) + "\n")

server_dict = {} # Dict returning list of channel ids for server name
channel_dict = {} # Dict returning channel name for channel id
dm_conversations = [] # Storage for messages that are not from servers

for i in range(len(chat_files)):
    path = chat_files[i][0] # path to channel.json
    with open(path, "r", encoding='utf-8-sig') as json_file: # opening channel.json
        json_data = json.loads(json_file.read()) # decode channel.json
        try:
            server_name = json_data["guild"]["name"] # server name (string)
            channel_name = json_data["name"]         # channel name (string)
            channel_id = str(json_data["id"])        # channel id (string)
            if not server_name in server_dict:       # if there is no entry for server_name yet in server_dict
                server_dict[server_name] = [channel_id] # Create entry, returning list with single channel_id
            elif server_name in server_dict:         # if there is an entry for server_name
                server_dict[server_name].append(channel_id) # append channel_id to list in dict
            if not channel_id in channel_dict:
                channel_dict[channel_id] = channel_name
        except:
            dm_conversations.append(json_data)

# for i in server_dict:
#     print(i + ":")
#     print(server_dict[i])
#     for n in server_dict[i]:
#         print(channel_dict[n] + " (" + n + ")")
#     print("")


print("The following servers are available:")
server_list = []
for i in server_dict.items():
    server_list.append(i[0])

print(str(server_list))
print("")

user_input = input("Please enter the server name: ")
if user_input in server_list:
    print("Input: " + user_input)
    if "/" in user_input:
        new_input = user_input.split("/")
        new_input = "_".join(new_input)
    else:
        new_input = user_input

    channel_list = []
    for i in server_dict[user_input]:
        channel_list.append(channel_dict[i] + " (" + i + ")")

    print("")

    question = input("Do you want to exclude any channels? y/n: ")
    if question == "y" or question == "j":
        for i in channel_list:
            print(i)
        print("")
        exclude = input("Insert channel id here or leave blank to cancel: ")
        while exclude != "":
            server_dict[user_input].remove(exclude)
            print(channel_dict[exclude] + " will not be moved to the new directory")
            print("")
            exclude = input("Exclude another channel? Insert channel id here or leave blank to continue: ")
    print("")

    newpath = os.path.join(my_path, new_input)
    while not os.path.exists(newpath):
        os.makedirs(newpath)
        print("new path: " + newpath)
        print("")
        for i in server_dict[user_input]:
            os.replace(my_path + "/"+ i, newpath + "/" + i)
            print("moved: " + i)

        print("Done")
        quit = input("Press enter to quit")
    else:
        print("Directory already exists: " + newpath)
else:
    print("Unknown Server " + user_input)
