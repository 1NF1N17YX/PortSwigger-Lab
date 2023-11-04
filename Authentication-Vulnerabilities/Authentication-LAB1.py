print("############## The following are the usernames:###############")

for i in range(150):
    if i % 3:
        print("wiener")
    else:
        print("carlos")

print("############## The following are the passwords:#############")
with open('passwords.txt') as f:
    lines = f.readlines()

i = 0

for line in lines:
    if i % 3:
        print(line.strip('\n'))
    else:
        print("peter")
        print(line.strip('\n'))
        i += 1
    i += 1
